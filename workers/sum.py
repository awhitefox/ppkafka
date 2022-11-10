import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from workers._base import run  # noqa: E402
from common import setup_logging  # noqa: E402
from common.contants import TOPICS  # noqa: E402


if __name__ == '__main__':
    setup_logging(TOPICS.SUM)
    run(TOPICS.SUM, sum)
