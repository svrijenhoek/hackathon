import json
import pandas as pd
import requests

data_folder = "Data\\data"
item_file = data_folder + "\\hackaton-item-properties.jsonl"
base_url = "https://www.npostart.nl/"


def get_publication_date(key):
    url = base_url+"/"+key
    response = requests.get(url)
    if response.history:
        split = response.url.split("/")
        return split[-2]
    else:
        return "01-01-1900"


def data_preparation():
    items = []
    with open(item_file) as itemfile:
        line = itemfile.readline()
        while line:
            item = json.loads(line)
            key = next(iter(item))
            value = item[key]
            value['publication_date'] = get_publication_date(key)
            items.append(value)
            line = itemfile.readline()
    df = pd.DataFrame(items)
    df['publication_date'] = pd.to_datetime(df['publication_date'], format='%d-%m-%Y')
    df.to_pickle("data\\item_df")


data_preparation()
