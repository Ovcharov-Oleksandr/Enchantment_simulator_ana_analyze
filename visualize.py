from analysis import (
    build_plot,
    plot_complexity,
    plot_ratio_bars
)
import matplotlib.pyplot as plt


# Plot overall cost and number of attempts for weapons and armor
# Uses log scale to better visualize exponential growth
def plot_cost_and_attempts(stats):
    fig, ax = plt.subplots(2, 2)
    fig.suptitle("Cost & Attempts (Log Scale)", fontsize=16)

    # --- Weapons: cost ---
    build_plot(
        ax[0, 0],
        stats,
        ["Magic Weapon", "Physical Weapon"],
        "total_enchant_cost",
        "Weapons Cost",
        log=True,
    )

    # --- Weapons: attempts ---
    build_plot(
        ax[0, 1],
        stats,
        ["Magic Weapon", "Physical Weapon"],
        "items_used",
        "Weapons Attempts",
        log=True,
    )

    # --- Armor: cost ---
    build_plot(
        ax[1, 0],
        stats,
        ["Full Armor", "Armor Parts and Jewelry"],
        "total_enchant_cost",
        "Armor Cost",
        log=True,
    )

    # --- Armor: attempts ---
    build_plot(
        ax[1, 1],
        stats,
        ["Full Armor", "Armor Parts and Jewelry"],
        "items_used",
        "Armor Attempts",
        log=True,
    )

    # Adjust layout to prevent overlap
    fig.tight_layout()
    return fig


# Compare cost and attempts for a single item
# with and without stone (lucky mode)
def plot_with_vs_without_stone(stats, item, log=False):
    fig, ax = plt.subplots(1, 2)
    fig.suptitle(f"{item}: With vs Without Stone", fontsize=16)

    # --- Cost comparison ---
    build_plot(
        ax[0], stats, [item], "total_enchant_cost", "Cost", mode="stone", log=log
    )

    # --- Attempts comparison ---
    build_plot(
        ax[1], stats, [item], "items_used", "Attempts", mode="stone", log=log
    )

    # Adjust layout
    fig.tight_layout()
    return fig


# Compare two different items using ratio and percentage difference
def plot_item_comparison(stats, item1, item2):
    fig, ax = plt.subplots(2, 2)
    fig.suptitle(f"{item1} vs {item2} Complexity Comparison", fontsize=16)

    # Plot ratio and percentage difference between two items
    plot_ratio_bars(ax, stats, [item1, item2])
    
    # Adjust layout
    fig.tight_layout()
    return fig


# Analyze how cost/attempts change between levels (delta and growth)
# Optionally limit analysis to a maximum level
def plot_delta_weapon_analysis(stats, item, max_level=None):
    fig1, ax1 = plt.subplots(2, 2)
    fig1.suptitle(f"{item} Delta", fontsize=16)

    # Full range delta/growth analysis
    plot_complexity(ax1, stats, item)

    fig2, ax2 = plt.subplots(2, 2)

    # Build dynamic title depending on max_level
    title = f"{item} Delta"
    if max_level is not None:
        title += f" Max lvl {max_level}"

    fig2.suptitle(title, fontsize=13)

    # Limited range analysis (if max_level is set)
    plot_complexity(ax2, stats, item, max_level=max_level)

    # Adjust layouts
    fig1.tight_layout()
    fig2.tight_layout()

    return fig1, fig2


def plot_distribution(df, item, level, column, log=False):

    # Filter data for selected item and target level
    data  = df[
        (df["item"] == item) &
        (df["target_level"] == level)
    ]

    # Split data into two groups: with stone and without stone
    data_no_stone = data[data["stone"] == False][column]
    data_stone = data[data["stone"] == True][column]

    # Create figure with 2 subplots (histogram + boxplot)
    fig, ax = plt.subplots(1, 2)

    # Optional: use logarithmic scale for better visibility of long tails
    if log:
        ax[0].set_yscale("log")

    # --- histogram ---
    # Compare distributions of costs (with vs without stone)
    ax[0].hist(data_no_stone, bins=50, alpha=0.5, label="No Stone")
    ax[0].hist(data_stone, bins=50, alpha=0.5, label="With Stone")
    ax[0].legend()
    ax[0].set_title("Histogram")
    ax[0].set_xlabel(column)
    ax[0].set_ylabel("Frequency")

    # --- boxplot ---
    # Show median, spread, and outliers for both groups
    ax[1].boxplot([data_no_stone, data_stone], labels=["No Stone", "With Stone"])

    # Global title for the figure
    fig.suptitle(f"{item} Distribution With / No Stone", fontsize=16)

    # Adjust layout to prevent overlap
    fig.tight_layout()

    return fig
