import argparse
from datetime import datetime as dt
from datetime import timedelta
from shared.download_data import download_share_data_moex_full
from shared.share_data_item_loader import ShareDataItemLoader


def download_share_data_moex_period(url, date_str, periods, folder, store_to_db=False):
    '''
    Downloads data from MOEX from the set date for required amount of periods
    '''
    start_date = dt.strptime(date_str, '%Y-%m-%d')
    for i in range(periods):
        date_argument = start_date.strftime('%Y-%m-%d')
        pages = download_share_data_moex_full(date_argument, url, folder)
        if store_to_db:
            for page in pages:
                loader = ShareDataItemLoader(page)
                print(f'Store page {page}')
                loader.load_moex_xml(start_date.date())
        start_date += timedelta(weeks=1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Downloads historical data from MOEX.'
    )
    parser.add_argument(
        'date',
        metavar='date',
        type=str,
        help='The date of the first data request.'
    )
    parser.add_argument(
        'periods',
        metavar='periods',
        type=int,
        nargs='?',
        default=1,
        help='The amount of time periods when the data will be downloaded.'
    )
    parser.add_argument(
        'folder',
        metavar='folder',
        type=str,
        nargs='?',
        help='The folder where data will be stored'
    )
    parser.add_argument(
        'store',
        metavar='store',
        type=bool,
        nargs='?',
        default=False,
        const=True,
        help='The flag which '
    )
    args = parser.parse_args()
    url = 'https://iss.moex.com/iss/history/engines/stock/markets/shares/securities.xml?'
    download_share_data_moex_period(
        url,
        args.date,
        args.periods,
        args.folder,
        args.store
    )
