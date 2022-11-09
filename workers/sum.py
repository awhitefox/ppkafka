from . import run
from common import setup_logging
from common.contants import TOPICS


if __name__ == '__main__':
    setup_logging(TOPICS.SUM)
    run(TOPICS.SUM, sum)
