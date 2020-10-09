import pandas as pd
from models.Item import Item
from models.User import User
from models.Helper import Helper
from scores import topic_similarity
from scores import actor_fairness

item_file = "data\\item_df"
user_file = "data\\user_df"
# specify the id of which user we need to generate recommendations for
user = 60
# to be implemented
recommendation_length = 5

helper = Helper()


def get_candidate_items(df):
    # generate item list of all candidate items. More constraints can be added when the dataset becomes bigger
    items = []
    for index, row in df.iterrows():
        items.append(Item(row, helper))
    return items


def calculate_scores(user, candidates):
    # obtain the absolute scores for each of the specified metrics
    scores = {}
    for candidate in candidates:
        candidate_scores = {}
        candidate_scores['topic_similarity'] = topic_similarity.calculate(user, candidate)
        candidate_scores['actor_fairness'] = actor_fairness.calculate(candidate)
        scores[candidate.id] = candidate_scores
    return scores


def get_weighted_average(user, candidates):
    # weight all obtained scores by the weights specified in the user profiles
    # currently all are automatically set to one
    total_scores = {}
    for candidate in candidates:
        item = candidates[candidate]
        weighted_values = {}
        for metric in item:
            weight = user.preferences[metric]
            weighted_values[metric] = item[metric] * weight
        sum = 0
        for k, v in weighted_values.items():
            sum += v
        total_scores[candidate] = sum/len(item)
    return total_scores

# read the data
item_df = pd.read_pickle(item_file)
user_df = pd.read_pickle(user_file)

# retrieve user data
user = User(user_df.loc[user_df['user'] == user], helper)
# retrieve all candidate items
candidates = get_candidate_items(item_df)
# calculate the score for each metric for each candidate
scores = calculate_scores(user, candidates)
# average all scores according to preferences specified in user profile (currently all 1)
average_scores = get_weighted_average(user, scores)
# sort scores
sorted = {k: v for k, v in sorted(average_scores.items(), key=lambda item: item[1], reverse=True)}
# print first n outcomes
dict_items = sorted.items()
first_n = list(dict_items)[:recommendation_length]
print(first_n)

