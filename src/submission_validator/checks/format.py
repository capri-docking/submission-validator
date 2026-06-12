import logging
import os
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from pdbtools.pdb_validate import run as validate_pdb_format

logger = logging.getLogger(__name__)


def check_pdb_format(file_path: Path) -> bool:
    """
    Validate a PDB file using pdb-tools pdb_validate.

    Args:
        file_path (str): Path to the PDB file to validate

    Returns:
        bool: True if validation passes, False if errors found
    """
    try:
        with open(file_path, "r") as f:
            # Redirect stdout and stderr to suppress pdb-tools output
            with redirect_stdout(open(os.devnull, "w")), redirect_stderr(
                open(os.devnull, "w")
            ):
                result = validate_pdb_format(f)
                return result == 0  # 0 means no errors
    except Exception as e:
        logger.error("Error validating PDB file: %s", e)
        return False
