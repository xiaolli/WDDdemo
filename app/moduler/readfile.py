
import pandas as pd

def read_file(file_url,sheet_name):
    data_orig = pd.read_excel(file_url,sheet_name='Sheet1')
    #print(data_orig.dtypes)
    return data_orig

def read_csv_file(file_url):
    csv_data_orig = pd.read_csv(file_url)
    #print(data_orig.dtypes)
    return csv_data_orig
