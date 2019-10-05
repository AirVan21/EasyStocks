import os
import pandas as pd


class DataManager(object):
    def __init__(self, path_to_data):
        self.path = path_to_data

    def resample_daily_data_to_weekly(self):
        if not os.path.isfile(self.path_to_data):
            print("Wrong file path: " + self.path_to_data)
            return
        df = pd.read_csv(self.path_to_data)
        df['Date'] = pd.to_datetime(df['Date'], errors='ignore')
        # Resamples daily data to weekly
        df.set_index('Date', inplace=True)
        aggregator = {'Open':'first',
                    'Close' : 'last',
                    'High'  : 'max',
                    'Low'   : 'min',
                    'Volume': 'sum'}
        offset = pd.offsets.timedelta(days=-6)
        df = df.resample('W', loffset=offset).apply(aggregator)
        df.reset_index(level=0, inplace=True)
        df.dropna(inplace=True)
        df.to_csv(self.path_to_data, index=None)

    def rename_columns(self, mapping):
        if not os.path.isfile(self.path_to_data):
            print("Wrong file path: " + self.path_to_data)
            return
        df = pd.read_csv(self.path_to_data)
        df.rename(columns=mapping)
        df.to_csv(self.path_to_data, index=None)


if __name__ == '__main__':
    print("Data management unit")
