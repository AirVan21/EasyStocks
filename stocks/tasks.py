from __future__ import absolute_import, unicode_literals
import os
from celery import task, chain
from shared.data_manager import DataManager
from shared.share_data_item_loader import ShareDataItemLoader
from shared.plotly_draw import (
    generate_candle_image,
    generate_fx_image
)
from shared.download_data import (
    download_share_data_alpha, download_fx_data,
    download_share_data_wtd
)
from shared.world_trading_download import (
    get_column_name_mapping,
    get_aggregator_wtd
)
from shared.news_download import (
    get_news_api_payload,
    get_start_end_week_dates,
    download_news_json
)
from shared.keys import (
    ALPHA_DOWNLOAD_KEY,
    WORLD_TRADING_DATA_KEY,
    NEWS_API_KEY
)
from stocks.models import (
    Share,
    CurrencyInstrument,
    Article
)


@task
def download_and_draw_share(share_name, mdp_folder, mdp_url, storage_path, img_path):
    storage_path = ''.join([storage_path, '/', mdp_folder])
    logger = download_and_draw_share.get_logger()
    csv_path = ''.join([storage_path, '/', share_name, '.csv'])
    weeks_count = 52
    logger.info('Processing ' + share_name + ' ' + storage_path)
    data_item_loader = ShareDataItemLoader(csv_path, share_name)
    manager = DataManager(csv_path)
    if mdp_folder == 'alphavantage':
        download_share_data_alpha(
            share_name,
            mdp_url,
            ALPHA_DOWNLOAD_KEY,
            storage_path
        )
        generate_candle_image(csv_path, weeks_count, img_path)
        data_item_loader.load_update()
    elif mdp_folder == 'worldtradingdata':
        return
        # Don't use worldtradingdata service
        download_share_data_wtd(
            share_name,
            mdp_url,
            WORLD_TRADING_DATA_KEY,
            storage_path
        )
        manager.resample_daily_data_to_weekly(get_aggregator_wtd())
        manager.rename_columns(get_column_name_mapping())
        generate_candle_image(csv_path, weeks_count, img_path)
        data_item_loader.load_update()
    else:
        logger.info('No market data provider specified!')
        return


@task
def download_and_draw_fx(base_ccy, ccy, mdp_url, storage_path, img_path):
    logger = download_and_draw_fx.get_logger()
    logger.info('Processing ' + base_ccy + '/' + ccy)
    download_fx_data(base_ccy, ccy, mdp_url, ALPHA_DOWNLOAD_KEY, storage_path)
    csv_path = storage_path + '/' + base_ccy + ccy + '.csv'
    days_count = 60
    generate_fx_image(csv_path, days_count, img_path)


@task
def download_data_task():
    root_path = os.path.abspath(os.path.dirname(__name__))
    storage_path = root_path + '/static/data'
    img_path_shares = root_path + '/static/img/stocks'
    share_tasks = [
        download_and_draw_share.signature(
            (
                share.ticker,
                share.dataProvider.folder,
                share.dataProvider.url,
                storage_path,
                img_path_shares
            ),
            countdown=30,
            immutable=True
        )
        for share in Share.objects.all()
    ]
    logger = download_data_task.get_logger()
    logger.info("Starting shares task chain!")
    chain(share_tasks).apply_async()


@task
def download_fx_data_task():
    root_path = os.path.abspath(os.path.dirname(__name__))
    storage_path = root_path + '/static/data'
    img_path_fx = root_path + '/static/img/currency'
    url = 'https://www.alphavantage.co/query?'
    fx_tasks = [
        download_and_draw_fx.signature(
            (
                instrument.base_currency,
                instrument.instrument_currency,
                url,
                storage_path,
                img_path_fx
            ),
            countdown=30,
            immutable=True
        )
        for instrument in CurrencyInstrument.objects.all()
    ]
    logger = download_data_task.get_logger()
    logger.info("Starting FX task chain!")
    chain(fx_tasks).apply_async()


@task
def download_and_store_news(share_name, share_id):
    from_date, to_date = get_start_end_week_dates()
    logger = download_and_store_news.get_logger()
    logger.info('Downloading news for ' + share_name)
    articles_en = download_news_json(
        get_news_api_payload(
            share_name,
            NEWS_API_KEY,
            from_date,
            to_date
        )
    )
    articles_ru = download_news_json(
        get_news_api_payload(
            share_name,
            NEWS_API_KEY,
            from_date,
            to_date,
            'ru'
        )
    )
    articles = articles_ru + articles_en
    # Take every 2nd article
    for article in articles[:50:2]:
        if not Article.are_valid_arguments(article):
            continue
        db_article = Article(
            author=article['author'],
            title=article['title'],
            description=article['description'],
            url=article['url'],
            url_to_image=article['urlToImage'],
            content=article['content'],
            publish_dateTime=article['publishedAt'],
            share=Share.objects.get(id=share_id)
        )
        db_article.save()


@task
def download_news_task():
    news_tasks = [
        download_and_store_news.signature(
            (
                share.title,
                share.id
            ),
            countdown=30,
            immutable=True
        )
        for share in Share.objects.all()
    ]
    logger = download_news_task.get_logger()
    logger.info("Starting news task chain!")
    chain(news_tasks).apply_async()
