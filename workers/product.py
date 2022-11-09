from . import run
from common import setup_logging
from common.contants import TOPICS


def product(payload: list[int]) -> int:
    r = 1
    for n in payload:
        r *= n
    return r


if __name__ == '__main__':
    setup_logging(TOPICS.PRODUCT)
    run(TOPICS.PRODUCT, product)
