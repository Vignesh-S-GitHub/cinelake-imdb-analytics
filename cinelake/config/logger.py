from pathlib import Path
from loguru import logger
import sys

def configure_logger() -> None:
    Path("logs").mkdir(exist_ok=True)

    logger.remove()

    logger.add(
        "logs/cinelake.log",
        level="INFO",
        rotation="10 MB",
        retention="30 days",
    )

    logger.add(
        sys.stderr,
        level="INFO",
        colorize=True,
    )