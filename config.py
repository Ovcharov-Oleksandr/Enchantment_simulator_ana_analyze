# Number of simulation runs (used to estimate average outcomes)
N = 10_000  # test

# Enchant success probabilities for each item type by level
# Key = item type, Value = dict of level → success probability
chance = {
    "Physical Weapon": {
        1: 1,  # guaranteed success at low levels
        2: 1,
        3: 1,
        4: 0.7,  # success chance drops from +4 onwards
        5: 0.7,
        6: 0.7,
        7: 0.7,
        8: 0.7,
        9: 0.7,
        10: 0.7,
        11: 0.55,  # further decrease at higher levels
        12: 0.55,
        13: 0.55,
        14: 0.55,
        15: 0.55,
        16: 0.3,  # very low chance at max level
    },
    "Magic Weapon": {
        1: 1,
        2: 1,
        3: 1,
        4: 0.5,  # lower base chances compared to physical weapons
        5: 0.5,
        6: 0.5,
        7: 0.5,
        8: 0.5,
        9: 0.5,
        10: 0.5,
        11: 0.35,
        12: 0.35,
        13: 0.35,
        14: 0.35,
        15: 0.35,
        16: 0.2,
    },
    "Full Armor": {
        1: 1,
        2: 1,
        3: 1,
        4: 1,  # guaranteed up to +4
        5: 0.66,
        6: 0.45,
        7: 0.4,
        8: 0.3,
        9: 0.25,
        10: 0.2,
        11: 0.2,
        12: 0.2,
    },
    "Armor Parts and Jewelry": {
        1: 1,
        2: 1,
        3: 1,
        4: 0.66,
        5: 0.45,
        6: 0.4,
        7: 0.35,
        8: 0.25,
        9: 0.2,
        10: 0.15,
        11: 0.15,
        12: 0.15,
    },
}

# Pricing configuration for cost calculation
price = {
    "item": {
        # Base item cost (not directly used in current calculations)
        "Physical Weapon": 1000,
        "Magic Weapon": 1000,
        "Full Armor": 700,
        "Armor Parts and Jewelry": 500,
    },
    "scroll": {
        # Cost of normal and blessed scrolls (weapon vs armor)
        "weapon_norm": 10,
        "weapon_bless": 300,
        "armor_norm": 3,
        "armor_bless": 30,
    },
    # Cost per enchant attempt when using a stone (lucky mode)
    "stone": 20,
}
