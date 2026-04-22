import pandas as pd
from simulation import simulate
from config import chance, N, price

rows = []  # list to store all simulation results (will become a DataFrame)

# Iterate over each item type and its enchant probability table
for item_name, chance_item in chance.items():
    max_lvl = max(chance_item.keys())  # maximum available enchant level for this item

    # Iterate over target levels (starting from +4)
    for target_lvl in range(4, max_lvl + 1):

        # Adjust number of simulations depending on difficulty (performance optimization)
        if item_name == "Magic Weapon" and target_lvl >= 13:
            N_local = 1000  # fewer runs for very hard cases
        elif "Armor" in item_name and target_lvl >= 11:
            N_local = 2000
        else:
            N_local = N  # default number of runs

        # Run simulation for both modes: with and without stone
        for use_stone in [False, True]:

            # Run Monte Carlo simulation
            items, norm_scr, bless_scr, stones = simulate(
                chance_item, target_lvl, lucky_mode=use_stone, N=N_local
            )

            # Progress log (helps track long simulations)
            print(f"{item_name} | lvl {target_lvl} | stone={use_stone} → done")

            # Select correct scroll prices based on item type
            if "Weapon" in item_name:
                norm_price = price["scroll"]["weapon_norm"]
                bless_price = price["scroll"]["weapon_bless"]
            else:
                norm_price = price["scroll"]["armor_norm"]
                bless_price = price["scroll"]["armor_bless"]

            price_stone = price["stone"]  # cost per stone use

            # Build dataset row-by-row for each simulation run
            for i in range(len(items)):
                total_cost = (
                    norm_scr[i] * norm_price
                    + bless_scr[i] * bless_price
                    + stones[i] * price_stone
                )

                rows.append(
                    {
                        "item": item_name,                  # item type
                        "target_level": target_lvl,         # desired enchant level
                        "stone": use_stone,                 # whether stone (lucky mode) was used
                        "items_used": items[i],             # number of items consumed
                        "norm_scr": norm_scr[i],            # normal scroll usage
                        "bless_scr": bless_scr[i],          # blessed scroll usage
                        "stones": stones[i],                # stones used
                        "total_enchant_cost": total_cost,   # total calculated cost
                    }
                )

# Convert results into a DataFrame
df = pd.DataFrame(rows)

# Save dataset for further analysis
df.to_csv("data.csv", index=False)