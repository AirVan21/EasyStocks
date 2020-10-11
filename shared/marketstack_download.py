import argparse
from download_data import download_share_data_marketstack


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Downloads historical data from marketstack.')
    parser.add_argument('symbol', metavar='symbol', type=str, help='stock symbol')
    parser.add_argument('apikey', metavar='apikey', type=str, help='private api key')
    parser.add_argument('folder', metavar='folder', type=str, nargs='?', help='folder for storage')
    args = parser.parse_args()
    url = 'http://api.marketstack.com/v1/eod'
    download_share_data_marketstack(args.symbol, url, args.apikey, args.folder)
