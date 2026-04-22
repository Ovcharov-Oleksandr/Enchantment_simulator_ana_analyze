import random


# Increases base success probability by a fixed bonus (used in lucky mode)
def lucky(p, bonus=0.15):
    # Ensures probability does not exceed 1
    return min(p * (1 + bonus), 1)


# Core enchant simulation for a single item
def enchant_item(chance_item, target_lvl, lucky_mode):
    weapon_lvl = 0  # current enchant level
    count_item = 1  # number of items consumed (due to resets)

    count_bless_scroll = 0  # number of blessed scrolls used
    count_norm_scroll = 0   # number of normal scrolls used
    count_stone = 0         # number of stones used (only in lucky mode)

    # Continue until desired target level is reached
    while weapon_lvl < target_lvl:
        # Get base success probability for next level
        p = chance_item[weapon_lvl + 1]

        # Apply lucky bonus if enabled
        if lucky_mode:
            p = lucky(p)

        # Decide which scroll is used based on probability
        if p < 1:
            count_bless_scroll += 1
            if lucky_mode:
                count_stone += 1
        else:
            count_norm_scroll += 1

        # Perform enchant attempt
        if random.random() < p:
            # Success → increase level
            weapon_lvl += 1
        else:
            # Failure → reset level and consume another item
            weapon_lvl = 0
            count_item += 1

    # Return total resources used for this single run
    return count_item, count_norm_scroll, count_bless_scroll, count_stone


# Run multiple simulations to estimate average resource usage
def simulate(item, target_lvl, lucky_mode, N):
    items_results = []          # items consumed per run
    norm_scrolls_results = []   # normal scrolls used per run
    bless_scrolls_results = []  # blessed scrolls used per run
    stones_result = []          # stones used per run

    # Repeat simulation N times
    for _ in range(N):
        it, t_n_scr, t_b_scr, s = enchant_item(item, target_lvl, lucky_mode)

        items_results.append(it)
        norm_scrolls_results.append(t_n_scr)
        bless_scrolls_results.append(t_b_scr)
        stones_result.append(s)

    # Return raw results for further aggregation (mean, etc.)
    return items_results, norm_scrolls_results, bless_scrolls_results, stones_result