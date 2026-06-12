import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def _parse_residues_by_chain(file_path: Path) -> dict[str, list[tuple[str, str, str]]]:
    """
    Parse ATOM records, grouping residues by chain in order of appearance.

    Consecutive atom lines belonging to the same residue (same chain,
    residue number and insertion code) are collapsed into a single entry.

    Returns:
        dict mapping chain id to an ordered list of (resSeq, iCode, resName) tuples.
    """
    chains: dict[str, list[tuple[str, str, str]]] = {}
    last_key: tuple[str, str, str, str] | None = None

    with open(file_path, "r") as f:
        for line in f:
            if line[:6] != "ATOM  ":
                last_key = None
                continue

            chain = line[21] if len(line) > 21 else " "
            res_name = line[17:20].strip() if len(line) > 20 else ""
            res_seq = line[22:26].strip() if len(line) > 26 else ""
            icode = line[26] if len(line) > 26 else " "

            # Collapse consecutive atoms of the same residue (identical chain,
            # resSeq, iCode and resName) into a single entry.
            collapse_key = (chain, res_seq, icode, res_name)
            if collapse_key != last_key:
                chains.setdefault(chain, []).append((res_seq, icode, res_name))
                last_key = collapse_key

    return chains


def check_overlapping_residue_numbers(file_path: Path) -> bool:
    """
    Check that no residue number (resSeq + iCode) is reused within a chain
    for a different residue identity.

    Returns:
        bool: True if no overlapping residue numbers found, False otherwise
    """
    try:
        chains = _parse_residues_by_chain(file_path)
        for residues in chains.values():
            seen: dict[tuple[str, str], str] = {}
            for res_seq, icode, res_name in residues:
                key = (res_seq, icode)
                if key in seen and seen[key] != res_name:
                    return False
                seen[key] = res_name
        return True
    except Exception as e:
        logger.error("Error checking overlapping residue numbers: %s", e)
        return False


def check_repeated_residues(file_path: Path) -> bool:
    """
    Check that no residue (resSeq + iCode + resName) appears in more than
    one separate block within a chain.

    Returns:
        bool: True if no repeated residues found, False otherwise
    """
    try:
        chains = _parse_residues_by_chain(file_path)
        for residues in chains.values():
            if len(residues) != len(set(residues)):
                return False
        return True
    except Exception as e:
        logger.error("Error checking repeated residues: %s", e)
        return False
