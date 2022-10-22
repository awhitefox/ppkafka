import logging

from base import run


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run('sum', 'results', sum)
