import os
import sys
from io import BytesIO

import requests
from PIL import Image, ImageOps

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from workers._base import run  # noqa: E402
from common import setup_logging, try_load_dotenv  # noqa: E402
from common.constants import TOPICS  # noqa: E402

POST_URL = 'https://api.imgbb.com/1/upload'


def grayscale(payload: str) -> str:
    tg_response = requests.get(payload)

    with BytesIO(tg_response.content) as src:
        img = Image.open(src)

        with BytesIO() as data:
            ImageOps.grayscale(img).save(data, format='PNG')
            data.seek(0)
            payload = {
                'key': os.getenv('IMGBB_TOKEN'),
            }
            files = {
                'image': data
            }
            r = requests.post(POST_URL, data=payload, files=files).json()

    return r['data']['url']


if __name__ == '__main__':
    setup_logging(TOPICS.GRAYSCALE)
    try_load_dotenv()
    run(TOPICS.GRAYSCALE, grayscale)
