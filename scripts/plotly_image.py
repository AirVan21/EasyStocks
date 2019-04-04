import argparse
import pandas as pd
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.io as pio
import os

def generate_image(path_to_data, weeks=52, output_folder=''):
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
    fig = go.Figure(data=[trace],layout=layout)
    base_name = os.path.basename(path_to_data)
    image_path = output_folder + "/" + os.path.splitext(base_name)[0] + '.png'
    pio.write_image(fig, image_path, width=500, height=335)
    print("Successfully created image " + image_path)


parser = argparse.ArgumentParser(description='Generates a candlestick chart using a historical data.')
parser.add_argument('data', metavar='data', type=str, help='csv file with historical data')
parser.add_argument('apikey', metavar='apikey', type=str, help='private api key for plotly')
parser.add_argument('weeks', metavar='weeks', type=int, help='numbers of weeks which will be used')
parser.add_argument('folder', metavar='folder', type=str, nargs='?', help='folder for storage')
args = parser.parse_args()
plotly.tools.set_credentials_file(username='airvan21', api_key=args.apikey)

# Calls generator
generate_image(args.data, args.weeks, args.folder)