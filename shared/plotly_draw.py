import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
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


def generate_candle_image_from_db(share_item, weeks=52, output_folder=''):
    '''
    Generates candle image using data from the database
    '''
    share_data = ShareDataItem.objects.filter(share=share_item).order_by('-date')
    df = pd.DataFrame(list(share_data.values()))
    last_df = df.head(weeks)
    trace = go.Candlestick(
        x=df.date,
        open=last_df.open_price,
        high=last_df.high_price,
        low=last_df.low_price,
        close=last_df.close_price
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
