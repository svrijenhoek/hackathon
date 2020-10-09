def calculate(user, candidate):
    user_genre_distribution = user.get_genre_distribution()
    candidate_genre = candidate.genres
    sum = 0
    try:
        for genre in candidate_genre[0]["terms"]:
            sum += user_genre_distribution[genre]
    except IndexError:
        return 0
    return sum



