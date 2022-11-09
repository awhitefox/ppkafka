from base import run
from common import setup_logging


def product(payload: list[int]) -> int:
    r = 1
    for n in payload:
        r *= n
    return r


if __name__ == '__main__':
    setup_logging('product')
    run('product', 'results', product)
