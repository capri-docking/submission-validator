from submission_validator.checks.structure import (
    check_chains_in_contact,
    check_clash_percentage,
)


def test_check_chains_in_contact_two_chains_in_contact(atom_line, write_pdb):
    lines = [
        atom_line(1, "CA", "ALA", "A", 1, x=0.0, y=0.0, z=0.0),
        atom_line(2, "CA", "GLY", "B", 1, x=3.0, y=0.0, z=0.0),
    ]
    test_file = write_pdb(lines)

    assert check_chains_in_contact(file_path=test_file).passed


def test_check_chains_in_contact_two_chains_far_apart(atom_line, write_pdb):
    lines = [
        atom_line(1, "CA", "ALA", "A", 1, x=0.0, y=0.0, z=0.0),
        atom_line(2, "CA", "GLY", "B", 1, x=20.0, y=0.0, z=0.0),
    ]
    test_file = write_pdb(lines)

    assert not check_chains_in_contact(file_path=test_file).passed


def test_check_chains_in_contact_isolated_chain(atom_line, write_pdb):
    lines = [
        atom_line(1, "CA", "ALA", "A", 1, x=0.0, y=0.0, z=0.0),
        atom_line(2, "CA", "GLY", "B", 1, x=3.0, y=0.0, z=0.0),
        atom_line(3, "CA", "SER", "C", 1, x=100.0, y=100.0, z=100.0),
    ]
    test_file = write_pdb(lines)

    assert not check_chains_in_contact(file_path=test_file).passed


def test_check_chains_in_contact_single_chain(atom_line, write_pdb):
    lines = [
        atom_line(1, "CA", "ALA", "A", 1, x=0.0, y=0.0, z=0.0),
        atom_line(2, "CA", "GLY", "A", 2, x=3.0, y=0.0, z=0.0),
    ]
    test_file = write_pdb(lines)

    assert not check_chains_in_contact(file_path=test_file).passed


def test_check_chains_in_contact_ignores_hydrogens(atom_line, write_pdb):
    """A hydrogen close to another chain shouldn't count as a contact."""
    lines = [
        atom_line(1, "CA", "ALA", "A", 1, x=0.0, y=0.0, z=0.0, element="C"),
        atom_line(2, "CA", "GLY", "B", 1, x=20.0, y=0.0, z=0.0, element="C"),
        atom_line(3, "H", "GLY", "B", 1, x=3.0, y=0.0, z=0.0, element="H"),
    ]
    test_file = write_pdb(lines)

    assert not check_chains_in_contact(file_path=test_file).passed


def test_check_clash_percentage_no_clashes(atom_line, write_pdb):
    lines = [
        atom_line(1, "CA", "ALA", "A", 1, x=0.0, y=0.0, z=0.0),
        atom_line(2, "CB", "ALA", "A", 1, x=0.0, y=0.0, z=1.0),
        atom_line(3, "CA", "GLY", "B", 1, x=3.0, y=0.0, z=0.0),
        atom_line(4, "CB", "GLY", "B", 1, x=3.0, y=0.0, z=1.0),
    ]
    test_file = write_pdb(lines)

    assert check_clash_percentage(file_path=test_file).passed


def test_check_clash_percentage_above_threshold(atom_line, write_pdb):
    lines = [
        atom_line(1, "CA", "ALA", "A", 1, x=0.0, y=0.0, z=0.0),
        atom_line(2, "CA", "GLY", "B", 1, x=0.5, y=0.0, z=0.0),  # clash (<2A)
        atom_line(3, "CB", "GLY", "B", 1, x=3.0, y=0.0, z=0.0),
        atom_line(4, "CG", "GLY", "B", 1, x=4.0, y=0.0, z=0.0),
        atom_line(5, "CD", "GLY", "B", 1, x=4.5, y=0.0, z=0.0),
    ]
    test_file = write_pdb(lines)

    assert not check_clash_percentage(file_path=test_file).passed


def test_check_clash_percentage_within_threshold(atom_line, write_pdb):
    """1 clash out of 20 contact pairs is exactly 5%, at the threshold."""
    lines = [atom_line(1, "CA", "ALA", "A", 1, x=0.0, y=0.0, z=0.0)]
    lines.append(atom_line(2, "CA", "GLY", "B", 1, x=1.5, y=0.0, z=0.0))  # clash (<2A)
    for i in range(19):
        lines.append(
            atom_line(3 + i, "CB", "GLY", "B", 1, x=3.0 + i * 0.01, y=0.0, z=0.0)
        )
    test_file = write_pdb(lines)

    assert check_clash_percentage(file_path=test_file).passed


def test_check_clash_percentage_no_contacts(atom_line, write_pdb):
    lines = [
        atom_line(1, "CA", "ALA", "A", 1, x=0.0, y=0.0, z=0.0),
        atom_line(2, "CA", "GLY", "B", 1, x=100.0, y=0.0, z=0.0),
    ]
    test_file = write_pdb(lines)

    assert check_clash_percentage(file_path=test_file).passed
