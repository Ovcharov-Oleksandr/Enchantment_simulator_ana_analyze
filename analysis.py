# ===== ANALYSIS FUNCTIONS =====

# Aggregate raw simulation data:
# - group by item type, stone usage, and target level
# - calculate mean cost and mean number of attempts
def get_stats(df):
    return df.groupby(["item", "stone", "target_level"]).agg(
        {"total_enchant_cost": "mean", "items_used": "mean"}
    )


# Prepare data for comparing different items (e.g., Magic vs Physical)
# Uses only runs WITHOUT stone (stone=False)
# Returns a table where columns = item types, index = level
def get_stats_by_item(stats, column):
    data = stats.xs(False, level="stone")  # filter: no stone
    return data[column].unstack("item")


# Prepare data for analyzing stone impact for a single item
# Returns a table where columns = stone (True/False), index = level
def get_stats_by_stone(stats, item, column):
    data = stats.xs(item, level="item")
    return data[column].unstack("stone")


# Compute complexity metrics:
# - delta: absolute change between levels
# - growth: relative (% change) between levels
def compute_complexity(data):
    delta = data.diff()
    growth = data.pct_change()
    return {"delta": delta, "growth": growth}


# ===== PLOTTING FUNCTIONS =====

# Generic line plot function:
# - plots multiple columns (e.g., items or stone modes)
# - supports optional logarithmic scale
def plot_graph(ax, data, title, ylabel, log=False):

    for col in data.columns:
        ax.plot(data.index, data[col], marker="o", label=col)

    if log:
        ax.set_yscale("log")

    ax.set_title(title)
    ax.set_xlabel("Level")
    ax.set_ylabel(ylabel)
    ax.legend()
    ax.grid()


# Wrapper that prepares data and passes it to plot_graph
# mode:
# - "item"  → compare different items (no stone)
# - "stone" → compare stone vs no stone for one item
def build_plot(ax, stats, items, column, title, mode="item", log=False):

    if mode == "stone":
        # compare stone=True vs False for a single item
        metric = get_stats_by_stone(stats, items[0], column)
    elif mode == "item":
        # compare multiple items without stone
        metric = get_stats_by_item(stats, column)
        metric = metric[items]
    else:
        raise ValueError("Unknown mode")
    
    # Convert technical column name into readable label
    ylabel = "Cost" if column == "total_enchant_cost" else "Attempts"

    plot_graph(ax, metric, title, ylabel, log)


# Plot delta and growth (complexity analysis)
# Shows how cost/attempts change between levels
def plot_complexity(ax, stats, item, log=False, max_level=None):

    metrics = ["total_enchant_cost", "items_used"]

    for i, column in enumerate(metrics):

        # get stone comparison data for the given item
        data = get_stats_by_stone(stats, item, column)

        # optionally limit analysis to a maximum level
        if max_level is not None:
            data = data[data.index <= max_level]

        comp = compute_complexity(data)

        # --- delta plot (absolute change) ---
        for col in comp["delta"].columns:
            ax[i, 0].plot(
                comp["delta"].index, comp["delta"][col], marker="o", label=col
            )

        ax[i, 0].set_title(f"{item} - Delta {column}")
        ax[i, 0].grid()
        ax[i, 0].legend()

        # --- growth plot (relative change) ---
        for col in comp["growth"].columns:
            ax[i, 1].plot(
                comp["growth"].index, comp["growth"][col], marker="o", label=col
            )

        ax[i, 1].set_title(f"{item} - Growth {column}")
        ax[i, 1].grid()
        ax[i, 1].legend()

        # optional log scale for both subplots
        if log:
            ax[i, 0].set_yscale("log")
            ax[i, 1].set_yscale("log")


# Plot comparison between two items using:
# - ratio (how many times one is larger than the other)
# - percentage difference
def plot_ratio_bars(axs, stats, items):

    metrics = ["total_enchant_cost", "items_used"]

    for i, column in enumerate(metrics):

        data = get_stats_by_item(stats, column)
        data = data[items]

        # ratio: item1 / item2
        ratio = data[items[0]] / data[items[1]]

        # percent difference relative to item2
        percent = (ratio - 1) * 100

        # --- ratio bar chart ---
        axs[i, 0].bar(ratio.index, ratio)
        axs[i, 0].set_title(f"{column} Ratio")
        axs[i, 0].set_ylabel("Ratio")
        axs[i, 0].set_xlabel("Level")
        axs[i, 0].grid(axis="y")

        # --- percentage difference bar chart ---
        axs[i, 1].bar(percent.index, percent)
        axs[i, 1].set_title(f"{column} % Difference")
        axs[i, 1].set_ylabel("%")
        axs[i, 1].set_xlabel("Level")
        axs[i, 1].grid(axis="y")