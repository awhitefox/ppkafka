import logging
import os.path
import sys


def try_load_dotenv():
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass


def setup_logging(name: str) -> None:
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs', f'{name}-{os.getpid()}.log')
    fmt = '%(asctime)s:%(levelname)s:%(name)s:%(message)s'
    logging.basicConfig(
        level=logging.INFO,
        format=fmt,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(p)
        ]
    )
