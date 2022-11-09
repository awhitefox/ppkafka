from base import run
from common import setup_logging

if __name__ == '__main__':
    setup_logging('sum')
    run('sum', 'results', sum)
