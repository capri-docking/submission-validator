import argparse
import sys

from submission_validator.logging_config import configure_logging
from submission_validator.validator import run_tier1_checks


def main():
    parser = argparse.ArgumentParser(description="Validate CAPRI submission PDB files")
    parser.add_argument("pdb_file", help="Path to the PDB file to validate")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable debug logging"
    )

    args = parser.parse_args()

    configure_logging(verbose=args.verbose)

    results = run_tier1_checks(args.pdb_file)

    for name, passed in results.items():
        status = "✅" if passed else "❌"
        print(f"{status} {name}")

    if all(results.values()):
        print("validation passed! ✅")
        return 0
    else:
        print("validation failed! ❌")
        return 1


if __name__ == "__main__":
    sys.exit(main())
