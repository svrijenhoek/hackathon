protected_group_key = "gender"
protected_group_value = "female"


def calculate(candidate):
    maker_data = candidate.get_maker_data()
    protected_sum = 0
    try:
        for maker in maker_data:
            if protected_group_key in maker:
                if maker[protected_group_key][0] == protected_group_value:
                    protected_sum += 1
    except IndexError:
        return 0
    if not protected_sum == 0:
        return protected_sum/len(maker_data)
    else:
        return 0
