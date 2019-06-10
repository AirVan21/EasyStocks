from __future__ import absolute_import, unicode_literals
import os
from celery import task, chain
from shared.download_data import get_share_payload, download_share_data
from shared.plotly_draw import generate_candle_image
from shared.keys import ALPHA_DOWNLOAD_KEY, PLOTLY_KEY
from stocks.models import Share


@task()
def dowload_and_draw_share(share_name, storage_path, img_path):
    logger = dowload_and_draw_share.get_logger()
    logger.info("Processing " + share_name)
    download_share_data(share_name, ALPHA_DOWNLOAD_KEY, storage_path)
    csv_path = storage_path + '/' + share_name + '.csv'
    generate_candle_image(csv_path, 52, img_path)


@task()
def download_data_task():
    root_path = os.path.abspath(os.path.dirname(__name__))
    storage_path = root_path + '/static/data'
    img_path = root_path + '/static/img/stocks'
    subtasks = [ dowload_and_draw_share.signature((share.ticker, storage_path, img_path), countdown=10, immutable=True)
        for share in Share.objects.all()
    ]
    logger = download_data_task.get_logger()
    logger.info("Starting task chain!")
    chain(subtasks).apply_async()

