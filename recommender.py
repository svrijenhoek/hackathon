import pandas as pd
from datetime import datetime, timedelta

item_file = "data\\item_df"
date = datetime.strptime("09-10-2020", "%d-%m-%Y")
time_range = 3


def get_candidate_items(df, genres=None, date=None):
    threshold_date = date - timedelta(days=time_range)
    if date:
        df = df[(df['publication_date'] > threshold_date)]
    if genres:
        df = df[(df['genres'] == genres)]
    return df


df = pd.read_pickle(item_file)
df['publication_date'] = pd.to_datetime(df['publication_date'], format='%d-%m-%Y')
candidates = get_candidate_items(df, date=date)
print(df)

