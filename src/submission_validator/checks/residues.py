import logging
from pathlib import Path

from submission_validator.result import CheckResult

logger = logging.getLogger(__name__)

# Each model is a dict mapping chain id to an ordered list of (resSeq, iCode, resName).
_ModelResidues = dict[str, list[tuple[str, str, str]]]


def _parse_residues_by_model(file_path: Path) -> list[_ModelResidues]:
    """
    Parse ATOM records grouped by MODEL record, then by chain.
    Files without MODEL records are treated as a single model.

    Consecutive atom lines belonging to the same residue are collapsed into one entry.

    Returns:
        list of per-model dicts, each mapping chain id to an ordered list of
        (resSeq, iCode, resName) tuples.
    """
    models: list[_ModelResidues] = []
    current: _ModelResidues = {}
    last_key: tuple[str, str, str, str] | None = None

    with open(file_path, "r") as f:
        for line in f:
            record = line[:6]
            if record == "MODEL ":
                current = {}
                last_key = None
            elif record == "ENDMDL":
                if current:
                    models.append(current)
                current = {}
                last_key = None
            elif record == "ATOM  ":
                chain = line[21] if len(line) > 21 else " "
                res_name = line[17:20].strip() if len(line) > 20 else ""
                res_seq = line[22:26].strip() if len(line) > 26 else ""
                icode = line[26] if len(line) > 26 else " "

                collapse_key = (chain, res_seq, icode, res_name)
                if collapse_key != last_key:
                    current.setdefault(chain, []).append((res_seq, icode, res_name))
                    last_key = collapse_key
            else:
                last_key = None

    if current:  # no MODEL records, or atoms after last ENDMDL
        models.append(current)

    return models


def check_overlapping_residue_numbers(file_path: Path) -> CheckResult:
    """
    Check that no residue number (resSeq + iCode) is reused within a chain
    for a different residue identity, within any single model.

    Returns:
        CheckResult: passed=True if no overlapping residue numbers found
    """
    try:
        models = _parse_residues_by_model(file_path)
        for model_idx, chains in enumerate(models, start=1):
            label = f"Model {model_idx}, " if len(models) > 1 else ""
            for chain, residues in chains.items():
                seen: dict[tuple[str, str], str] = {}
                for res_seq, icode, res_name in residues:
                    key = (res_seq, icode)
                    if key in seen and seen[key] != res_name:
                        return CheckResult(
                            passed=False,
                            message=(
                                f"{label}Chain {chain}: position "
                                f"({res_seq}{icode.strip()}) assigned to both "
                                f"{seen[key]} and {res_name}"
                            ),
                        )
                    seen[key] = res_name
        return CheckResult(passed=True)
    except Exception as e:
        logger.error("Error checking overlapping residue numbers: %s", e)
        return CheckResult(passed=False, message=str(e))


def check_repeated_residues(file_path: Path) -> CheckResult:
    """
    Check that no residue (resSeq + iCode + resName) appears in more than one
    non-contiguous block within a chain, within any single model.

    Returns:
        CheckResult: passed=True if no repeated residues found
    """
    try:
        models = _parse_residues_by_model(file_path)
        for model_idx, chains in enumerate(models, start=1):
            label = f"Model {model_idx}, " if len(models) > 1 else ""
            for chain, residues in chains.items():
                if len(residues) != len(set(residues)):
                    seen: set[tuple[str, str, str]] = set()
                    for res_seq, icode, res_name in residues:
                        key = (res_seq, icode, res_name)
                        if key in seen:
                            return CheckResult(
                                passed=False,
                                message=(
                                    f"{label}Chain {chain}: residue {res_name} "
                                    f"({res_seq}{icode.strip()}) appears in "
                                    f"non-contiguous blocks"
                                ),
                            )
                        seen.add(key)
        return CheckResult(passed=True)
    except Exception as e:
        logger.error("Error checking repeated residues: %s", e)
        return CheckResult(passed=False, message=str(e))
