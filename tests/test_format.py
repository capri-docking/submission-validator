import os
import tempfile
from pathlib import Path

from submission_validator.pdb import validate_pdb_file


def test_validate_pdb_file_with_format_errors():
    """Test validation fails with malformed PDB file."""
    invalid_content = """HEADER    TEST FILE
ATOM      1  N   ALA A   1       1.000   2.000   3.000  1.00  0.00           N
END"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".pdb", delete=False) as f:
        f.write(invalid_content)
        test_file = f.name

    try:
        result = validate_pdb_file(file_path=Path(test_file))
        assert result is False, "Validation should fail for malformed PDB file"
    finally:
        os.unlink(test_file)


def test_validate_pdb_file_with_line_length_errors():
    """Test validation fails with incorrect line lengths."""
    # Lines that are too long
    invalid_content = """HEADER    TEST FILE with extra content that makes it too long for PDB format
ATOM      1  N   ALA A   1       1.000   2.000   3.000  1.00  0.00           N  
END with extra content"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".pdb", delete=False) as f:
        f.write(invalid_content)
        test_file = f.name

    try:
        result = validate_pdb_file(file_path=Path(test_file))
        assert result is False, (
            "Validation should fail for PDB file with line length errors"
        )
    finally:
        os.unlink(test_file)


def test_validate_pdb_file_nonexistent():
    """Test validation handles nonexistent files gracefully."""
    result = validate_pdb_file(file_path=Path("/nonexistent/path/file.pdb"))
    assert result is False, "Validation should fail for nonexistent file"


def test_validate_pdb_file_empty():
    """Test validation behavior with empty file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".pdb", delete=False) as f:
        f.write("")
        test_file = f.name

    try:
        result = validate_pdb_file(file_path=Path(test_file))
        # pdb_validate considers empty files as valid (no format errors)
        assert result is True, (
            "Validation should pass for empty PDB file (no format errors)"
        )
    finally:
        os.unlink(test_file)


def test_validate_pdb_file_with_missing_fields():
    """Test validation fails with missing required fields."""
    # ATOM line missing some fields
    invalid_content = """HEADER    TEST FILE                                                                   
ATOM      1  N   ALA A   1       1.000   2.000                                   
END                                                                                   """

    with tempfile.NamedTemporaryFile(mode="w", suffix=".pdb", delete=False) as f:
        f.write(invalid_content)
        test_file = f.name

    try:
        result = validate_pdb_file(file_path=Path(test_file))
        assert result is False, (
            "Validation should fail for PDB file with missing fields"
        )
    finally:
        os.unlink(test_file)
