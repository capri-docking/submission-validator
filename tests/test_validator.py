from submission_validator.validator import run_tier1_checks


def test_run_tier1_checks_passes_for_clean_pdb(atom_line, write_pdb):
    lines = [
        atom_line(1, "N", "ALA", "A", 1),
        atom_line(2, "CA", "ALA", "A", 1),
        atom_line(3, "N", "GLY", "A", 2),
        atom_line(4, "CA", "GLY", "A", 2),
    ]
    test_file = write_pdb(lines)

    assert all(run_tier1_checks(file_path=test_file).values()) is True


def test_run_tier1_checks_fails_on_residue_overlap(atom_line, write_pdb):
    """Format is valid, but residue numbering has an overlap."""
    lines = [
        atom_line(1, "CA", "ALA", "A", 1),
        atom_line(2, "CA", "GLY", "A", 1),
    ]
    test_file = write_pdb(lines)

    assert all(run_tier1_checks(file_path=test_file).values()) is False


def test_run_tier1_checks_empty_file_passes_all_checks(write_pdb):
    test_file = write_pdb([])

    assert all(run_tier1_checks(file_path=test_file).values()) is True


def test_run_tier1_checks_reports_each_check(atom_line, write_pdb):
    lines = [
        atom_line(1, "CA", "ALA", "A", 1),
        atom_line(2, "CA", "GLY", "A", 2),
    ]
    test_file = write_pdb(lines)

    results = run_tier1_checks(file_path=test_file)
    assert set(results) == {
        "PDB format",
        "Overlapping residue numbers",
        "Repeated residues in chain",
    }
    assert all(results.values())


def test_run_tier1_checks_flags_failing_check(atom_line, write_pdb):
    """Residue 2 is repeated non-contiguously, so only that check fails."""
    lines = [
        atom_line(1, "CA", "ALA", "A", 1),
        atom_line(2, "CA", "GLY", "A", 2),
        atom_line(3, "CA", "SER", "A", 3),
        atom_line(4, "CA", "GLY", "A", 2),
    ]
    test_file = write_pdb(lines)

    results = run_tier1_checks(file_path=test_file)
    assert results["PDB format"] is True
    assert results["Overlapping residue numbers"] is True
    assert results["Repeated residues in chain"] is False
