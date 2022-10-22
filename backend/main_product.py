import logging

from base import run


def product(payload: list[int]) -> int:
    r = 1
    for n in payload:
        r *= n
    return r


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run('product', 'results', product)
