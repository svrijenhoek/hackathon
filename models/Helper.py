import pandas as pd
from models.Item import Item


item_df = pd.read_pickle("data\\item_df")


def get_item_by_id(id):
    row = item_df.loc[item_df['item'] == id]
    item = Item(row)
    return item
