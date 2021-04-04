import pandas as pd
import argparse
from stocks.models import ShareDataItem, Share


class ShareDataItemLoader(object):
    '''
    ShareDataItemLoader class saves end-of-day data to the database
    '''

    def __init__(self, path_to_file):
        self.path = path_to_file

    def load_items_from_csv(self, share_ticker, count):
        '''
        Loads end-of-day data from the csv file to the database
        '''
        share_items = Share.objects.filter(ticker=share_ticker)
        if not share_items:
            print('Did not find related share for ticker', share_ticker)
            return
        csv_file = pd.read_csv(self.path, delimiter=',')
        csv_file['timestamp'] = pd.to_datetime(
            csv_file['timestamp'],
            errors='ignore'
        )
        csv_file.sort_values(by=['timestamp'], inplace=True, ascending=False)
        csv_file = csv_file.head(count)
        self.load_csv(share_items.first(), csv_file)

    def load_update(self, share_ticker):
        share_items = Share.objects.filter(ticker=share_ticker)
        if not share_items:
            print('Did not find related share!')
            return
        csv_file = pd.read_csv(self.path, delimiter=',')
        csv_file['timestamp'] = pd.to_datetime(
            csv_file['timestamp'],
            errors='ignore'
        )
        csv_file.sort_values(by=['timestamp'], inplace=True, ascending=False)
        # Last share data items
        selected_share = share_items.first()
        share_data_items = ShareDataItem.objects.filter(
            share=selected_share
        ).order_by('-date')
        if not share_data_items:
            self.load_csv(selected_share, csv_file)
        else:
            last_data_item = share_data_items.first()
            last_datetime = pd.to_datetime(last_data_item.date)
            csv_update = csv_file[csv_file['timestamp'] > last_datetime]
            self.load_csv(selected_share, csv_update)

    def load_csv(self, selected_share, csv_frame):
        '''
        Loads end-of-day data related to the share from the csv to database
        '''
        for index, row in csv_frame.iterrows():
            date_value = row['timestamp'].date()
            data_share_item = ShareDataItem(
                share=selected_share,
                date=date_value,
                open_price=row['open'],
                high_price=row['high'],
                low_price=row['low'],
                close_price=row['close'],
                volume=row['volume']
            )
            data_share_item.save()

    def clear_items(self, share_ticker):
        '''
        Removes share data items related to the share from the database
        '''
        share_items = Share.objects.filter(ticker=share_ticker)
        if not share_items:
            print('Did not find related share for ticker', share_ticker)
            return
        ShareDataItem.objects.filter(share=share_items.first()).delete()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Loads stocks historical data to database.')
    parser.add_argument('path', metavar='path', type=str, help='path to csv data')
    parser.add_argument('ticker', metavar='ticker', type=str, help='share ticker')
    args = parser.parse_args()
    # Loads
    loader = ShareDataItemLoader(args.path)
    number_of_weeks = 52
    loader.load_items_from_csv(args.ticker, number_of_weeks)
