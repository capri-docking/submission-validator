from pathlib import Path

from submission_validator.checks import TIER1_CHECKS


def run_tier1_checks(file_path: Path) -> dict[str, bool]:
    """
    Run all Tier 1 checks against a PDB file individually.

    Returns:
        dict mapping check name to its pass/fail result
    """
    return {name: check(file_path) for name, check in TIER1_CHECKS}
