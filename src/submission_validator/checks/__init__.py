from submission_validator.checks.format import check_pdb_format
from submission_validator.checks.residues import (
    check_overlapping_residue_numbers,
    check_repeated_residues,
)

TIER1_CHECKS = (
    ("PDB format", check_pdb_format),
    ("Overlapping residue numbers", check_overlapping_residue_numbers),
    ("Repeated residues in chain", check_repeated_residues),
)
