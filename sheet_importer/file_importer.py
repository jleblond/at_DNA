from pandas import pandas as pd
from .csv_file import CSVFile


def read_csv(file, headers):
    csv_file_obj = CSVFile(file, headers)
    csv_file_obj.load()
    return csv_file_obj


def get_dataframe_from_csv(file, headers):
    csv_fobj = read_csv(file, headers)
    return pd.DataFrame(csv_fobj.dataframe)