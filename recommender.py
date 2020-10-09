import pandas as pd
from models.Item import Item
from models.User import User
from scores import topic_similarity

item_file = "data\\item_df"
user_file = "data\\user_df"
user = 183938
recommendation_length = 5


def get_candidate_items(df, genres=None, date=None):
    # threshold_date = date - timedelta(days=time_range)
    candidates = df
    # # if date:
    # #    mask = (candidates['publication_date'] > threshold_date)
    # #    candidates = candidates.loc[mask]
    # if genres:
    #     df_genres = candidates.mask(lambda x: x['genres'] == genres)
    #     candidates = df_genres
    items = []
    for index, row in df.iterrows():
        items.append(Item(row))
    return items


def calculate_scores(user, candidates):
    scores = {}
    for candidate in candidates:
        candidate_scores = {}
        candidate_scores['topic_similarity'] = topic_similarity.calculate(user, candidate)
        scores[candidate.id] = candidate_scores
    return scores


def get_weighted_average(user, candidates):
    total_scores = {}
    for candidate in candidates:
        weighted_values = {}
        for metric in candidate:
            weight = user.preferences[metric]
            weighted_values[metric] = candidate[metric] * weight
        sum = 0
        for k, v in weighted_values:
            sum += v

    return scores


item_df = pd.read_pickle(item_file)
user_df = pd.read_pickle(user_file)

user = User(user_df.loc[user_df['user'] == user])
candidates = get_candidate_items(item_df)
scores = calculate_scores(user, candidates)
average_scores = get_weighted_average(user, scores)
print(scores)

