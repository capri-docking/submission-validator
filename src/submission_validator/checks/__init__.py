from submission_validator.checks.format import check_pdb_format
from submission_validator.checks.residues import (
    check_overlapping_residue_numbers,
    check_repeated_residues,
)
from submission_validator.checks.structure import (
    check_chains_in_contact,
    check_clash_percentage,
)

TIER1_CHECKS = (
    ("PDB format", check_pdb_format),
    ("Overlapping residue numbers", check_overlapping_residue_numbers),
    ("Repeated residues in chain", check_repeated_residues),
)

TIER2_CHECKS = (
    ("Chains not in contact", check_chains_in_contact),
    ("% of clashes", check_clash_percentage),
)
