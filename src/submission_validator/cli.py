import argparse
import logging
import sys

from submission_validator.logging_config import configure_logging
from submission_validator.overview import get_overview
from submission_validator.validator import run_tier1_checks, run_tier2_checks

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Validate CAPRI submission PDB files")
    parser.add_argument("pdb_file", help="Path to the PDB file to validate")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable debug logging"
    )

    args = parser.parse_args()

    configure_logging(verbose=args.verbose)

    overview = get_overview(args.pdb_file)
    tier1_results = run_tier1_checks(args.pdb_file)
    tier2_results = run_tier2_checks(args.pdb_file)

    logger.info("Overview")
    for key, value in overview.items():
        logger.info("  %s: %s", key, value)

    logger.info("Tier 1")
    for name, result in tier1_results.items():
        status = "✅" if result.passed else "❌"
        logger.info("%s %s", status, name)
        if result.message:
            logger.info("   → %s", result.message)

    logger.info("Tier 2")
    for name, result in tier2_results.items():
        status = "✅" if result.passed else "❌"
        logger.info("%s %s", status, name)
        if result.message:
            logger.info("   → %s", result.message)

    if all(tier1_results.values()) and all(tier2_results.values()):
        logger.info("validation passed! ✅")
        return 0
    else:
        logger.info("validation failed! ❌")
        return 1


if __name__ == "__main__":
    sys.exit(main())
