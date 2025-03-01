import logging
import sys

def setup_logger():
    logger = logging.getLogger("project")

    # Prevent the logger from propagating messages to the root logger
    logger.propagate = False
    logger.setLevel(logging.INFO)

    # Create console handler with formatting
    console_handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger

# Create and configure logger
logger = setup_logger()
