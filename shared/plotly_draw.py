import pandas as pd
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
    layout = go.Layout(xaxis=dict(rangeslider=dict(visible=False)))
    fig = go.Figure(data=[trace], layout=layout)
    fig.layout.template = 'plotly_white'
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
    layout = go.Layout(xaxis=dict(rangeslider=dict(visible=False)))
    fig = go.Figure(data=[trace], layout=layout)
    fig.layout.template = 'plotly_white'
    base_name = os.path.basename(path_to_data)
    image_path = output_folder + "/" + os.path.splitext(base_name)[0] + '.png'
    pio.write_image(fig, image_path, width=450, height=300)
    print("Successfully created FX image " + image_path)
