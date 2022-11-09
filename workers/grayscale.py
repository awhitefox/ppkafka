import os
from io import BytesIO

import requests
from PIL import Image, ImageOps

from . import run
from common import setup_logging, try_load_dotenv

POST_URL = 'https://api.imgbb.com/1/upload'


def product(payload: str) -> str:
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
    setup_logging('grayscale')
    try_load_dotenv()
    run('grayscale', 'results', product)
