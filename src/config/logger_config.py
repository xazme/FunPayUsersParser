import logging


def setup_logger() -> None:
    """
    Docstring for setup_logger
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
