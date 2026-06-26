import io
import logging
import os
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from pdbtools.pdb_validate import run as validate_pdb_format

from submission_validator.result import CheckResult

logger = logging.getLogger(__name__)


def check_pdb_format(file_path: Path) -> CheckResult:
    """
    Validate a PDB file using pdb-tools pdb_validate.

    Args:
        file_path (str): Path to the PDB file to validate

    Returns:
        CheckResult: passed=True if validation passes, with error lines as message on failure
    """
    try:
        with open(file_path, "r") as f:
            buf = io.StringIO()
            with (
                redirect_stdout(buf),
                redirect_stderr(open(os.devnull, "w")),
            ):
                result = validate_pdb_format(f)
        if result == 0:
            return CheckResult(passed=True)
        return CheckResult(passed=False, message=buf.getvalue().strip() or None)
    except Exception as e:
        logger.error("Error validating PDB file: %s", e)
        return CheckResult(passed=False, message=str(e))
