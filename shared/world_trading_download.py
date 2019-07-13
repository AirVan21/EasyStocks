import argparse
from download_data import get_world_trading_data_payload, download_data_json


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Downloads historical data from world trading data.')
    parser.add_argument('symbol', metavar='symbol', type=str, help='stock symbol')
    parser.add_argument('apikey', metavar='apikey', type=str, help='private api key')
    parser.add_argument('folder', metavar='folder', type=str, nargs='?', help='folder for storage')
    args = parser.parse_args()
    download_data_json(get_world_trading_data_payload(args.symbol, args.apikey),
                       args.symbol,
                       args.folder)
