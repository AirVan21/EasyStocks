from __future__ import absolute_import, unicode_literals
import os
from celery import task, chain
from shared.download_data import get_share_payload, get_fx_payload, download_share_data, download_fx_data
from shared.plotly_draw import generate_candle_image, generate_fx_image
from shared.keys import ALPHA_DOWNLOAD_KEY, PLOTLY_KEY
from stocks.models import Share, CurrencyInstrument


@task()
def download_and_draw_share(share_name, storage_path, img_path):
    logger = download_and_draw_share.get_logger()
    logger.info("Processing " + share_name)
    download_share_data(share_name, ALPHA_DOWNLOAD_KEY, storage_path)
    csv_path = storage_path + '/' + share_name + '.csv'
    weeks_count = 52
    generate_candle_image(csv_path, weeks_count, img_path)


@task()
def download_and_draw_fx(base_ccy, ccy, storage_path, img_path):
    logger = download_and_draw_fx.get_logger()
    logger.info('Processing ' + base_ccy + '/' + ccy)
    download_fx_data(base_ccy, ccy, ALPHA_DOWNLOAD_KEY, storage_path)
    csv_path = storage_path + '/' + base_ccy + ccy + '.csv'
    days_count = 60
    generate_fx_image(csv_path, days_count, img_path)


@task()
def download_data_task():
    root_path = os.path.abspath(os.path.dirname(__name__))
    storage_path = root_path + '/static/data'
    img_path_shares = root_path + '/static/img/stocks'
    share_tasks = [ download_and_draw_share.signature((share.ticker, storage_path, img_path_shares), countdown=10, immutable=True)
        for share in Share.objects.all()
    ]
    logger = download_data_task.get_logger()
    logger.info("Starting shares task chain!")
    chain(share_tasks).apply_async()


@task()
def download_fx_data_task():
    root_path = os.path.abspath(os.path.dirname(__name__))
    storage_path = root_path + '/static/data'
    img_path_fx = root_path + '/static/img/fx'
    fx_tasks = [ download_and_draw_fx.signature((instrument.base_currency, instrument.instrument_currency, 
                                                 storage_path, img_path_fx), countdown=10, immutable=True)
        for instrument in CurrencyInstrument.objects.all()
    ]
    logger = download_data_task.get_logger()
    logger.info("Starting FX task chain!")
    chain(fx_tasks).apply_async()