import argparse
import requests
from shared.download_data import get_share_payload, download_share_data


parser = argparse.ArgumentParser(description='Downloads historical data from alphavantage.')
parser.add_argument('symbol', metavar='symbol', type=str, help='stock symbol')
parser.add_argument('apikey', metavar='apikey', type=str, help='private api key')
parser.add_argument('folder', metavar='folder', type=str, nargs='?', help='folder for storage')
args = parser.parse_args()


download_share_data(args.symbol, args.apikey, args.folder)
