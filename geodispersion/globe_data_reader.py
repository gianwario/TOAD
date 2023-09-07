import pandas as pd


def read_data(globe_data_path: str):
    df = pd.read_excel(globe_data_path, index_col=0)
    return df
