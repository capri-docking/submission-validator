import argparse
import sys

from submission_validator.pdb import validate_pdb_file


def main():
    parser = argparse.ArgumentParser(description="Validate CAPRI submission PDB files")
    parser.add_argument("pdb_file", help="Path to the PDB file to validate")

    args = parser.parse_args()

    if validate_pdb_file(args.pdb_file):
        print("validation passed! ✅")
        return 0
    else:
        print("validation failed! ❌")
        return 1


if __name__ == "__main__":
    sys.exit(main())
