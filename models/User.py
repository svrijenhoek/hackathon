from collections import defaultdict
import models.Helper


class User:

    def __init__(self, row):
        self.history = row['history']
        self.preferences = {'topic_similarity': 1}

    def get_genre_distribution(self):
        total = 0
        genres = defaultdict(float)
        for row in self.history.tolist():
            for entry in row:
                item = models.Helper.get_item_by_id(entry["item"])
                for genre in item.genres.tolist():
                    for term in genre[0]['terms']:
                        genres[term] += 1
                        total += 1
        for k, v in genres.items():
            genres[k] = v/total
        return genres
