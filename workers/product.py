import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from workers._base import run   # noqa: E402
from common import setup_logging  # noqa: E402
from common.constants import TOPICS  # noqa: E402


def product(payload: list[int]) -> int:
    r = 1
    for n in payload:
        r *= n
    return r


if __name__ == '__main__':
    setup_logging(TOPICS.PRODUCT)
    run(TOPICS.PRODUCT, product)
