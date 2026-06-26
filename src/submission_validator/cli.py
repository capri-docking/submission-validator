import argparse
import logging
import sys
from pathlib import Path

from submission_validator.fixes.tidy import fix_with_tidy
from submission_validator.logging_config import configure_logging
from submission_validator.overview import get_overview
from submission_validator.result import CheckResult
from submission_validator.validator import run_tier1_checks, run_tier2_checks

logger = logging.getLogger(__name__)


def _print_tier_results(
    tier1: dict[str, CheckResult], tier2: dict[str, CheckResult]
) -> None:
    logger.info("Tier 1")
    for name, result in tier1.items():
        status = "✅" if result.passed else "❌"
        logger.info("%s %s", status, name)
        if result.message:
            logger.info("   → %s", result.message)

    logger.info("Tier 2")
    for name, result in tier2.items():
        status = "✅" if result.passed else "❌"
        logger.info("%s %s", status, name)
        if result.message:
            logger.info("   → %s", result.message)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate CAPRI submission PDB files")
    parser.add_argument("pdb_file", help="Path to the PDB file to validate")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable debug logging"
    )
    parser.add_argument(
        "--fix",
        metavar="OUTPUT",
        help="Apply pdb_tidy to repair common format issues and write to OUTPUT",
    )

    args = parser.parse_args()

    configure_logging(verbose=args.verbose)

    pdb_path = Path(args.pdb_file)

    overview = get_overview(pdb_path)
    tier1_results = run_tier1_checks(pdb_path)
    tier2_results = run_tier2_checks(pdb_path)

    logger.info("Overview")
    for key, value in overview.items():
        logger.info("  %s: %s", key, value)

    _print_tier_results(tier1_results, tier2_results)

    passed = all(tier1_results.values()) and all(tier2_results.values())

    if args.fix:
        output_path = Path(args.fix)
        if fix_with_tidy(pdb_path, output_path):
            logger.info("Fixed file written to %s", output_path)
            logger.info("Re-validating fixed file...")
            t1 = run_tier1_checks(output_path)
            t2 = run_tier2_checks(output_path)
            _print_tier_results(t1, t2)
            passed = all(t1.values()) and all(t2.values())

    if passed:
        logger.info("validation passed! ✅")
        return 0
    else:
        logger.info("validation failed! ❌")
        return 1


if __name__ == "__main__":
    sys.exit(main())
