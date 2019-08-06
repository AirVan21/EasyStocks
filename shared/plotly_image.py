import argparse
import plotly
from plotly_draw import generate_candle_image


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generates a candlestick chart using a historical data.')
    parser.add_argument('data', metavar='data', type=str, help='csv file with historical data')
    parser.add_argument('apikey', metavar='apikey', type=str, help='private api key for plotly')
    parser.add_argument('weeks', metavar='weeks', type=int, help='numbers of weeks which will be used')
    parser.add_argument('folder', metavar='folder', type=str, nargs='?', help='folder for storage')
    args = parser.parse_args()
    plotly.tools.set_credentials_file(username='airvan21', api_key=args.apikey)
    # Calls generator
    generate_candle_image(args.data, args.weeks, args.folder)
