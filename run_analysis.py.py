import pandas as pd
import matplotlib.pyplot as plt
from analysis import get_stats
from visualize import (
    plot_cost_and_attempts,
    plot_with_vs_without_stone,
    plot_item_comparison,
    plot_delta_weapon_analysis,
    plot_distribution
)

# Load precomputed simulation data from CSV file
df = pd.read_csv("data.csv", sep=";")

# Aggregate raw data into grouped statistics (mean cost and attempts)
stats = get_stats(df)

# --- Main visualizations ---

# Overall cost and attempts (log scale)
fig1 = plot_cost_and_attempts(stats)

# Stone impact for Physical Weapon
fig2 = plot_with_vs_without_stone(stats, "Physical Weapon")

# Comparison between Magic and Physical weapons
fig3 = plot_item_comparison(stats, "Magic Weapon", "Physical Weapon")

# Stone impact for Full Armor
fig4 = plot_with_vs_without_stone(stats, "Full Armor")

# Delta and growth analysis for Physical Weapon
fig5, fig6 = plot_delta_weapon_analysis(stats, "Physical Weapon")

# Plot distribution of total enchant cost for Physical Weapon at level 16
fig7 = plot_distribution(df, "Physical Weapon", 16, "total_enchant_cost", log=True)

# Display all generated figures
plt.show()