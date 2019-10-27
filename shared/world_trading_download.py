import argparse
from download_data import download_share_data_wtd


def get_column_name_mapping():
    mapping = {
        'Date': 'timestamp',
        'Open': 'open',
        'Close': 'close',
        'High': 'high',
        'Low': 'low',
        'Volume': 'volume'
    }
    return mapping


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Downloads historical data from world trading data.')
    parser.add_argument('symbol', metavar='symbol', type=str, help='stock symbol')
    parser.add_argument('apikey', metavar='apikey', type=str, help='private api key')
    parser.add_argument('folder', metavar='folder', type=str, nargs='?', help='folder for storage')
    args = parser.parse_args()
    url = 'https://api.worldtradingdata.com/api/v1/history?'
    download_share_data_wtd(args.symbol, url, args.apikey, args.folder)
