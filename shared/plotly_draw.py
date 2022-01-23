import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
from datetime import date, timedelta
import os
from stocks.models import ShareDataItem


def generate_candle_image(path_to_data, weeks=52, output_folder=''):
    '''
    Generate candle image using data from the csv file
    '''
    if not os.path.isfile(path_to_data):
        print("Wrong file path: " + path_to_data)
        return
    df = pd.read_csv(path_to_data)
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='ignore')
    last_df = df.head(weeks)
    trace = go.Candlestick(
        x=df.timestamp,
        open=last_df.open,
        high=last_df.high,
        low=last_df.low,
        close=last_df.close
    )
    layout = go.Layout(xaxis=dict(rangeslider=dict(visible=False)))
    fig = go.Figure(data=[trace], layout=layout)
    fig.layout.template = 'plotly_white'
    base_name = os.path.basename(path_to_data)
    image_path = output_folder + "/" + os.path.splitext(base_name)[0] + '.png'
    pio.write_image(fig, image_path, width=500, height=335)
    print('Successfully created image ' + image_path)


def generate_week_dates(start_date, weeks):
    '''
    Generates date pairs (monday, frinday) for a provided year
    '''
    monday = start_date + timedelta(days=(7 - start_date.weekday()))
    for _ in range(weeks):
        friday = monday + timedelta(days=4)
        yield monday, friday
        monday += timedelta(days=7)


def generate_candle_image_from_db_by_weeks(share_item, start_date, weeks=52, output_folder=''):
    '''
    Generates candle image using data from the database
    '''
    data = []
    for monday, friday in generate_week_dates(start_date, weeks):
        week_data = list(ShareDataItem.objects.filter(share=share_item).filter(date__range=[monday, friday]).order_by('-date'))
        if week_data:
            summary = {}
            summary['open_price'] = week_data[-1].open_price
            summary['close_price'] = week_data[0].close_price
            summary['high_price'] = max(week_data, key=lambda item: item.high_price).high_price
            summary['low_price'] = min(week_data, key= lambda item: item.low_price).low_price
            summary['date'] = friday
            data.append(summary)
    df = pd.DataFrame(data)
    trace = go.Candlestick(
        x=df.date,
        open=df.open_price,
        high=df.high_price,
        low=df.low_price,
        close=df.close_price
    )
    layout = go.Layout(xaxis=dict(rangeslider=dict(visible=False)))
    fig = go.Figure(data=[trace], layout=layout)
    fig.layout.template = 'plotly_white'
    base_name = share_item.ticker + '.png'
    image_path = output_folder + '/' + base_name
    pio.write_image(fig, image_path, width=500, height=335)
    print('Successfully created image ' + image_path)


def generate_fx_image(path_to_data, days=60, output_folder=''):
    if not os.path.isfile(path_to_data):
        print("Wrong file path: " + path_to_data)
        return
    df = pd.read_csv(path_to_data)
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='ignore')
    last_df = df.head(days)
    trace = go.Scatter(x=last_df.timestamp, y=last_df.close)
    layout = go.Layout(xaxis=dict(rangeslider=dict(visible=False)))
    fig = go.Figure(data=[trace], layout=layout)
    fig.layout.template = 'plotly_white'
    base_name = os.path.basename(path_to_data)
    image_path = output_folder + "/" + os.path.splitext(base_name)[0] + '.png'
    pio.write_image(fig, image_path, width=450, height=300)
    print("Successfully created FX image " + image_path)
