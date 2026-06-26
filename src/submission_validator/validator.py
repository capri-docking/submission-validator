from pathlib import Path

from submission_validator.checks import TIER1_CHECKS, TIER2_CHECKS
from submission_validator.result import CheckResult


def run_tier1_checks(file_path: Path) -> dict[str, CheckResult]:
    """
    Run all Tier 1 checks against a PDB file individually.

    Returns:
        dict mapping check name to its CheckResult
    """
    return {name: check(file_path) for name, check in TIER1_CHECKS}


def run_tier2_checks(file_path: Path) -> dict[str, CheckResult]:
    """
    Run all Tier 2 checks against a PDB file individually.

    Returns:
        dict mapping check name to its CheckResult
    """
    return {name: check(file_path) for name, check in TIER2_CHECKS}
