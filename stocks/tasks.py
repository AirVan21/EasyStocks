from __future__ import absolute_import, unicode_literals
import os
from celery import task, chain
from shared.download_data import download_share_data_alpha, download_fx_data, download_share_data_wtd
from shared.plotly_draw import generate_candle_image, generate_fx_image
from shared.keys import ALPHA_DOWNLOAD_KEY, WORLD_TRADING_DATA_KEY
from stocks.models import Share, CurrencyInstrument


@task()
def download_and_draw_share(share_name, mdp_folder, mdp_url, storage_path, img_path):
    storage_path = ''.join([storage_path, '/', mdp_folder])
    logger = download_and_draw_share.get_logger()
    csv_path = ''.join([storage_path, '/', share_name, '.csv'])
    weeks_count = 52
    logger.info('Processing ' + share_name + ' ' + storage_path)
    if mdp_folder == 'alphavantage':
        download_share_data_alpha(share_name, mdp_url, ALPHA_DOWNLOAD_KEY, storage_path)
        generate_candle_image(csv_path, weeks_count, img_path)
    elif mdp_folder == 'worldtradingdata':
        download_share_data_wtd(share_name, mdp_url, WORLD_TRADING_DATA_KEY, storage_path)
    else:
        logger.info('No market data provider specified!')
        return


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
    share_tasks = [download_and_draw_share.signature((share.ticker,
                                                      share.dataProvider.folder,
                                                      share.dataProvider.url,
                                                      storage_path,
                                                      img_path_shares),
                                                     countdown=20,
                                                     immutable=True)
        for share in Share.objects.all()]
    logger = download_data_task.get_logger()
    logger.info("Starting shares task chain!")
    chain(share_tasks).apply_async()


@task()
def download_fx_data_task():
    root_path = os.path.abspath(os.path.dirname(__name__))
    storage_path = root_path + '/static/data'
    img_path_fx = root_path + '/static/img/currency'
    fx_tasks = [download_and_draw_fx.signature((instrument.base_currency,
                                                instrument.instrument_currency,
                                                storage_path,
                                                img_path_fx),
                                               countdown=20,
                                               immutable=True)
        for instrument in CurrencyInstrument.objects.all()]
    logger = download_data_task.get_logger()
    logger.info("Starting FX task chain!")
    chain(fx_tasks).apply_async()
