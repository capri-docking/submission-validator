import logging
from pathlib import Path

import numpy as np

from submission_validator.constants import (
    CLASH_DISTANCE,
    CONTACT_DISTANCE,
    MAX_CLASH_PERCENT,
)
from submission_validator.result import CheckResult

logger = logging.getLogger(__name__)


def _is_hydrogen(line: str) -> bool:
    """Determine whether an ATOM line refers to a hydrogen atom."""
    element = line[76:78].strip() if len(line) > 76 else ""
    if element:
        return element.upper() == "H"

    atom_name = line[12:16].strip() if len(line) > 16 else ""
    atom_name = atom_name.lstrip("0123456789")
    return atom_name.upper().startswith("H")


def _parse_heavy_atoms_by_chain(file_path: Path) -> dict[str, np.ndarray]:
    """
    Parse ATOM records, collecting heavy (non-hydrogen) atom coordinates by chain.

    Returns:
        dict mapping chain id to an (N, 3) array of x, y, z coordinates.
    """
    coords_by_chain: dict[str, list[tuple[float, float, float]]] = {}

    with open(file_path, "r") as f:
        for line in f:
            if line[:6] != "ATOM  ":
                continue
            if _is_hydrogen(line):
                continue

            chain = line[21] if len(line) > 21 else " "
            x = float(line[30:38])
            y = float(line[38:46])
            z = float(line[46:54])
            coords_by_chain.setdefault(chain, []).append((x, y, z))

    return {
        chain: np.array(coords, dtype=float)
        for chain, coords in coords_by_chain.items()
    }


def _parse_heavy_atoms_by_model(
    file_path: Path,
) -> list[dict[str, np.ndarray]]:
    """
    Parse ATOM records grouped by MODEL record, then by chain.
    Files without MODEL records are treated as a single model.

    Returns:
        list of dicts, one per model, each mapping chain id to (N, 3) coordinate array.
    """
    models: list[dict[str, list[tuple[float, float, float]]]] = []
    current: dict[str, list[tuple[float, float, float]]] = {}

    with open(file_path, "r") as f:
        for line in f:
            record = line[:6]
            if record == "MODEL ":
                current = {}
            elif record == "ENDMDL":
                if current:
                    models.append(current)
                current = {}
            elif record == "ATOM  ":
                if _is_hydrogen(line):
                    continue
                chain = line[21] if len(line) > 21 else " "
                x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
                current.setdefault(chain, []).append((x, y, z))

    if current:  # no MODEL records, or atoms after last ENDMDL
        models.append(current)

    return [
        {chain: np.array(coords, dtype=float) for chain, coords in m.items()}
        for m in models
    ]


def _pairwise_distances(coords_a: np.ndarray, coords_b: np.ndarray) -> np.ndarray:
    """Return the (N, M) matrix of distances between two sets of coordinates."""
    diff = coords_a[:, np.newaxis, :] - coords_b[np.newaxis, :, :]
    return np.linalg.norm(diff, axis=-1)


def check_chains_in_contact(file_path: Path) -> CheckResult:
    """
    Check that every chain has at least one heavy atom within CONTACT_DISTANCE
    of a heavy atom from a different chain.

    Returns:
        CheckResult: passed=True if every chain is in contact with at least one other chain
    """
    try:
        chains = _parse_heavy_atoms_by_chain(file_path)
        chain_ids = list(chains)
        if len(chain_ids) < 2:
            return CheckResult(
                passed=False,
                message="File contains only one chain; at least two chains are required",
            )

        for chain_id in chain_ids:
            others = np.concatenate(
                [chains[other_id] for other_id in chain_ids if other_id != chain_id]
            )
            distances = _pairwise_distances(chains[chain_id], others)
            if distances.size == 0 or distances.min() >= CONTACT_DISTANCE:
                return CheckResult(
                    passed=False,
                    message=f"Chain {chain_id} is not in contact with any other chain",
                )

        return CheckResult(passed=True)
    except Exception as e:
        logger.error("Error checking chain contacts: %s", e)
        return CheckResult(passed=False, message=str(e))


def _clash_percent_for_model(model: dict[str, np.ndarray]) -> float | None:
    """Return clash % for one model, or None if there are no inter-chain contacts."""
    chain_ids = list(model)
    contact_pairs = 0
    clash_pairs = 0
    for i, chain_a in enumerate(chain_ids):
        for chain_b in chain_ids[i + 1 :]:
            distances = _pairwise_distances(model[chain_a], model[chain_b])
            contact_pairs += int(np.count_nonzero(distances < CONTACT_DISTANCE))
            clash_pairs += int(np.count_nonzero(distances < CLASH_DISTANCE))
    if contact_pairs == 0:
        return None
    return clash_pairs / contact_pairs * 100


def check_clash_percentage(file_path: Path) -> CheckResult:
    """
    Check that the percentage of clashing inter-chain heavy-atom pairs (distance
    < CLASH_DISTANCE) among all contact pairs (distance < CONTACT_DISTANCE) does
    not exceed MAX_CLASH_PERCENT.

    Always reports the observed min/max clash % across all models in the message.

    Returns:
        CheckResult: passed=True if the clash percentage is within the allowed threshold
    """
    try:
        models = _parse_heavy_atoms_by_model(file_path)

        per_model: list[float] = []
        for model in models:
            pct = _clash_percent_for_model(model)
            if pct is not None:
                per_model.append(pct)

        if not per_model:
            return CheckResult(passed=False, message="No inter-chain contacts found")

        min_clash = min(per_model)
        max_clash = max(per_model)
        n = len(per_model)

        if n == 1:
            msg = (
                f"Clash percentage: {per_model[0]:.1f}% "
                f"(max allowed: {MAX_CLASH_PERCENT}%)"
            )
        else:
            msg = (
                f"Clash percentage across {n} models: "
                f"min {min_clash:.1f}%, max {max_clash:.1f}% "
                f"(max allowed: {MAX_CLASH_PERCENT}%)"
            )

        if max_clash > MAX_CLASH_PERCENT:
            return CheckResult(passed=False, message=msg)
        return CheckResult(passed=True, message=msg)
    except Exception as e:
        logger.error("Error checking clash percentage: %s", e)
        return CheckResult(passed=False, message=str(e))
