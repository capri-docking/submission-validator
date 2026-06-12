import pytest


def _atom_line(serial, atom_name, res_name, chain, res_seq, icode=" "):
    return (
        f"ATOM  {serial:>5} {atom_name:<4} {res_name:>3} {chain}{res_seq:>4}{icode}   "
        f"{1.0:>8.3f}{2.0:>8.3f}{3.0:>8.3f}{1.00:>6.2f}{0.00:>6.2f}      {'':<4}{'C':>2}  "
    )


@pytest.fixture
def atom_line():
    """Build an 80-column ATOM record for a single atom."""
    return _atom_line


@pytest.fixture
def write_pdb(tmp_path):
    """Write a list of PDB lines to a temporary file and return its path."""

    def _write(lines, name="test.pdb"):
        content = "\n".join(lines) + "\n" if lines else ""
        path = tmp_path / name
        path.write_text(content)
        return path

    return _write
