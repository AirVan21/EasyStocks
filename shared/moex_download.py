
import argparse
from datetime import datetime
from download_data import download_share_data_moex


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Downloads historical data from MOEX.')
    parser.add_argument('date', metavar='date', type=str, help='data request date')
    parser.add_argument('folder', metavar='folder', type=str, nargs='?', help='folder for storage')
    args = parser.parse_args()
    url = 'https://iss.moex.com/iss/history/engines/stock/markets/shares/securities.xml?'
    download_share_data_moex(args.date, url, args.folder)
