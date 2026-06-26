import io
import logging
from contextlib import redirect_stdout
from pathlib import Path

from pdbtools import pdb_wc

logger = logging.getLogger(__name__)


def get_overview(file_path: Path) -> dict[str, str]:
    """Return summary statistics for a PDB file using pdb_wc."""
    try:
        with open(file_path) as f:
            buf = io.StringIO()
            with redirect_stdout(buf):
                pdb_wc.run(f, "")

        result: dict[str, str] = {}
        for line in buf.getvalue().splitlines():
            parts = line.split("\t")
            if len(parts) >= 2:
                key = parts[0].rstrip(":")
                value = parts[1].strip()
                if value == "True":
                    value = "Yes"
                elif value == "False":
                    value = "No"
                result[key] = value
        return result
    except Exception as e:
        logger.error("Error getting file overview: %s", e)
        return {}
