import sys

from loguru import logger

logger.remove(0)

logger.add(
    "./logs/logs.log",
    rotation="50 MB",
    compression="zip",
    format="{time:YYYY-MM-DD HH:mm:ss zz} | {level: <8} | {name}:{function}:{line} - {message}",
)

logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss zz}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
)


# logger.add(sys.stderr, colorize=True)
