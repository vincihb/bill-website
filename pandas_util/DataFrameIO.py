import pandas as pd
import string


# One trick pony for reading and writing data frames as json so we don't have to worry about
# the directory or other annoying details
class DataFrameIO:
    DIR_NAME = "./obj/pandas_dfs/"

    @staticmethod
    def read(filename):
        return pd.read_json(DataFrameIO.DIR_NAME + filename + '.json')

    @staticmethod
    def write(data_frame: pd.DataFrame, filename: string):
        json = data_frame.to_json()
        with open(DataFrameIO.DIR_NAME + filename + '.json', 'w+') as f:
            f.write(json)

        return data_frame
