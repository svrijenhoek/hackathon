def calculate(candidate):
    maker_distribution = candidate.get_actor_distribution()
    sum = 0
    try:
        for maker in maker_distribution:
            sum += maker_distribution[maker]
    except IndexError:
        return 0
    return sum