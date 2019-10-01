import pandas as pd
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.io as pio
import os


def generate_candle_image(path_to_data, weeks=52, output_folder=''):
    if not os.path.isfile(path_to_data):
        print("Wrong file path: " + path_to_data)
        return
    df = pd.read_csv(path_to_data)
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='ignore')
    last_df = df.head(weeks)
    trace = go.Candlestick(x=df.timestamp,
                           open=last_df.open,
                           high=last_df.high,
                           low=last_df.low,
                           close=last_df.close)
    layout = go.Layout(xaxis = dict(rangeslider = dict(visible = False)))
    fig = go.Figure(data=[trace], layout=layout)
    base_name = os.path.basename(path_to_data)
    image_path = output_folder + "/" + os.path.splitext(base_name)[0] + '.png'
    pio.write_image(fig, image_path, width=500, height=335)
    print("Successfully created image " + image_path)


def generate_fx_image(path_to_data, days=60, output_folder=''):
    if not os.path.isfile(path_to_data):
        print("Wrong file path: " + path_to_data)
        return
    df = pd.read_csv(path_to_data)
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='ignore')
    last_df = df.head(days)
    trace = go.Scatter(x=last_df.timestamp, y=last_df.close)
    layout = go.Layout(xaxis = dict(rangeslider = dict(visible = False)))
    fig = go.Figure(data=[trace],layout=layout)
    base_name = os.path.basename(path_to_data)
    image_path = output_folder + "/" + os.path.splitext(base_name)[0] + '.png'
    pio.write_image(fig, image_path, width=450, height=300)
    print("Successfully created FX image " + image_path)


def generate_candle_image_from_daily(path_to_data, weeks=52, output_folder=''):
    if not os.path.isfile(path_to_data):
        print("Wrong file path: " + path_to_data)
        return
    df = pd.read_csv(path_to_data)
    df['Date'] = pd.to_datetime(df['Date'], errors='ignore')
    # Resamples daily data to weekly
    df.set_index('Date', inplace=True)
    aggregator = {'Open'  : 'first',
                  'Close' : 'last',
                  'High'  : 'max',
                  'Low'   : 'min',
                  'Volume': 'sum'}
    offset = pd.offsets.timedelta(days=-6)
    df = df.resample('W', loffset=offset).apply(aggregator)
    last_df = df.tail(weeks)
    trace = go.Candlestick(x=last_df.index,
                           open=last_df.Open,
                           high=last_df.High,
                           low=last_df.Low,
                           close=last_df.Close)
    layout = go.Layout(xaxis = dict(rangeslider = dict(visible = False)))
    fig = go.Figure(data=[trace], layout=layout)
    base_name = os.path.basename(path_to_data)
    image_path = ''.join([output_folder, '/', os.path.splitext(base_name)[0], '.png'])
    pio.write_image(fig, image_path, width=500, height=335)
    print("Successfully created image " + image_path)


def resample_daily_data_to_weekly(path_to_data):
    if not os.path.isfile(path_to_data):
        print("Wrong file path: " + path_to_data)
        return
    df = pd.read_csv(path_to_data)
    df['Date'] = pd.to_datetime(df['Date'], errors='ignore')
    # Resamples daily data to weekly
    df.set_index('Date', inplace=True)
    aggregator = {'Open'  : 'first',
                  'Close' : 'last',
                  'High'  : 'max',
                  'Low'   : 'min',
                  'Volume': 'sum'}
    offset = pd.offsets.timedelta(days=-6)
    df = df.resample('W', loffset=offset).apply(aggregator)
    df.to_csv(path_to_data, index=None)
