import logging
from pathlib import Path

from pdbtools import pdb_tidy

logger = logging.getLogger(__name__)


def fix_with_tidy(input_path: Path, output_path: Path) -> bool:
    """Apply pdb_tidy to pad/truncate lines to 80 chars and add TER/END records."""
    try:
        with open(input_path) as f:
            lines = list(pdb_tidy.run(f))
        output_path.write_text("".join(lines))
        return True
    except Exception as e:
        logger.error("pdb_tidy failed: %s", e)
        return False
