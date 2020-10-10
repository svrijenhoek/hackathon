from collections import defaultdict


class User:

    def __init__(self, row, helper):
        self.history = row['history']
        self.preferences = {'calibration': 0.5, 'actor_fairness': 0.25, 'description_similarity': 1}
        self.genre_distribution = []
        self.helper = helper

    def get_genre_distribution(self):
        if not self.genre_distribution:
            total = 0
            genres = defaultdict(float)
            for row in self.history.tolist():
                for entry in row:
                    item = self.helper.get_item_by_id(entry["item"], self.helper)
                    for genre in item.genres.tolist():
                        for term in genre[0]['terms']:
                            genres[term] += 1
                            total += 1
            for k, v in genres.items():
                genres[k] = v/total
            self.genre_distribution = genres
        return self.genre_distribution

    def get_items_in_history(self):
        ids = []
        for row in self.history.tolist():
            for entry in row:
                ids.append(entry["item"])
        return ids
