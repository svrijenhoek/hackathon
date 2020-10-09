import json
import pandas as pd
from models.Item import Item


class Helper:

    def __init__(self):
        try:
            self.known_persons = self.read_json_file('data/known_persons.json')
        except FileNotFoundError:  # when no persons file is found, create a new dict
            self.known_persons = {}

    @staticmethod
    def read_json_file(file):
        with open(file) as F:
            return json.load(F)

    @staticmethod
    def write_to_json(file, s):
        with open(file, 'w') as outfile:
            json.dump(s, outfile, indent=4, separators=(',', ': '), sort_keys=True)

    def get_item_by_id(self, id, helper):
        row = self.item_df.loc[self.item_df['item'] == id]
        item = Item(row, helper)
        return item
