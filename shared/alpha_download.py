import argparse
from shared.download_data import download_share_data_alpha


def get_aggregator_alpha():
    aggregator = {
        'open': 'first',
        'close': 'last',
        'high': 'max',
        'low': 'min',
        'volume': 'sum'}
    return aggregator


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Downloads historical data from alphavantage.')
    parser.add_argument('symbol', metavar='symbol', type=str, help='stock symbol')
    parser.add_argument('apikey', metavar='apikey', type=str, help='private api key')
    parser.add_argument('folder', metavar='folder', type=str, nargs='?', help='folder for storage')
    args = parser.parse_args()
    url = 'https://www.alphavantage.co/query?'
    download_share_data_alpha(args.symbol, url, args.apikey, args.folder)
