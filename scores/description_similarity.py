import pandas as pd

similarities = pd.read_pickle("data\\dic_cos_summaries.pkl")


def find_similarity(x, y):
    for k, v in similarities.items():
        if k == (x, y):
            return v
    for k, v in similarities.items():
        if k == (y, x):
            return v
    return 0


def calculate(user, candidate):
    total = 0
    history = user.get_items_in_history()
    for item in history:
        similarity = find_similarity(candidate.id, item)
        total += similarity
    return total / len(history)
