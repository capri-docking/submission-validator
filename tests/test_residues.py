from submission_validator.checks.residues import (
    check_overlapping_residue_numbers,
    check_repeated_residues,
)


def test_check_overlapping_residue_numbers_detects_reused_number(atom_line, write_pdb):
    """Same residue number used for two different residue identities."""
    lines = [
        atom_line(1, "CA", "ALA", "A", 1),
        atom_line(2, "CA", "GLY", "A", 2),
        atom_line(3, "CA", "SER", "A", 2),
    ]
    test_file = write_pdb(lines)

    result = check_overlapping_residue_numbers(file_path=test_file)
    assert (
        result is False
    ), "Should detect residue number reused for a different residue"


def test_check_overlapping_residue_numbers_sequential_is_ok(atom_line, write_pdb):
    """Sequential, non-overlapping residue numbering."""
    lines = [
        atom_line(1, "CA", "ALA", "A", 1),
        atom_line(2, "CA", "GLY", "A", 2),
        atom_line(3, "CA", "SER", "A", 3),
    ]
    test_file = write_pdb(lines)

    result = check_overlapping_residue_numbers(file_path=test_file)
    assert result is True, "Sequential residue numbering should pass"


def test_check_overlapping_residue_numbers_allows_insertion_codes(atom_line, write_pdb):
    """Same residue number with different insertion codes is not an overlap."""
    lines = [
        atom_line(1, "CA", "ALA", "A", 100),
        atom_line(2, "CA", "GLY", "A", 100, icode="A"),
    ]
    test_file = write_pdb(lines)

    result = check_overlapping_residue_numbers(file_path=test_file)
    assert result is True, "Distinct insertion codes should not be an overlap"


def test_check_overlapping_residue_numbers_empty_file(write_pdb):
    test_file = write_pdb([])

    result = check_overlapping_residue_numbers(file_path=test_file)
    assert result is True, "Empty file should pass (no residues)"


def test_check_repeated_residues_detects_non_contiguous_repeat(atom_line, write_pdb):
    """Same residue (number + name) appears in two separate blocks."""
    lines = [
        atom_line(1, "CA", "ALA", "A", 1),
        atom_line(2, "CA", "GLY", "A", 2),
        atom_line(3, "CA", "SER", "A", 3),
        atom_line(4, "CA", "GLY", "A", 2),  # repeated residue 2
    ]
    test_file = write_pdb(lines)

    result = check_repeated_residues(file_path=test_file)
    assert result is False, "Should detect a non-contiguous repeated residue"


def test_check_repeated_residues_normal_chain_is_ok(atom_line, write_pdb):
    lines = [
        atom_line(1, "CA", "ALA", "A", 1),
        atom_line(2, "CA", "GLY", "A", 2),
        atom_line(3, "CA", "SER", "A", 3),
    ]
    test_file = write_pdb(lines)

    result = check_repeated_residues(file_path=test_file)
    assert result is True, "Normal chain should pass"


def test_check_repeated_residues_consecutive_atoms_not_flagged(atom_line, write_pdb):
    """Multiple atom lines for the same residue must collapse, not count as a repeat."""
    lines = [
        atom_line(1, "N", "ALA", "A", 1),
        atom_line(2, "CA", "ALA", "A", 1),
        atom_line(3, "C", "ALA", "A", 1),
    ]
    test_file = write_pdb(lines)

    result = check_repeated_residues(file_path=test_file)
    assert result is True, "Consecutive atoms of the same residue are not a repeat"


def test_check_repeated_residues_empty_file(write_pdb):
    test_file = write_pdb([])

    result = check_repeated_residues(file_path=test_file)
    assert result is True, "Empty file should pass (no residues)"
