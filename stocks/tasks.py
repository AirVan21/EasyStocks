from __future__ import absolute_import, unicode_literals
import os
from celery import task
from shared.download_data import get_payload, download_data
from stocks.models import models


@task()
def download_data_task():
    root_path = os.path.abspath(os.path.dirname(__name__))
    storage_path = root_path + '/static/data'
    download_data('AAPL', 'demo', storage_path)


@task()
def draw_plot_task():
    root_path = os.path.abspath(os.path.dirname(__name__))
    storage_path = root_path + '/static/img/stocks'