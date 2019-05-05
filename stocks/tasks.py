from __future__ import absolute_import, unicode_literals
import os
from celery import task
from shared.download_data import get_payload, download_data
from shared.plotly_draw import generate_image
from shared.keys import ALPHA_DOWNLOAD_KEY, PLOTLY_KEY
from stocks.models import Share


@task()
def download_data_task():
    root_path = os.path.abspath(os.path.dirname(__name__))
    storage_path = root_path + '/static/data'
    for share in Share.objects.all():
        download_data(share.ticker, ALPHA_DOWNLOAD_KEY, storage_path)


@task()
def draw_plot_task():
    root_path = os.path.abspath(os.path.dirname(__name__))
    data_path = root_path + '/static/data'
    storage_path = root_path + '/static/img/stocks'
    for share in Share.objects.all():
        csv_path = data_path + '/' + share.ticker + '.csv'
        generate_image(csv_path, 52, storage_path)
