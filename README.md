# Lineage 2 Enchant Cost Analysis

## 1. Overview

This project analyzes the cost and complexity of item enchanting in Lineage 2 using Monte Carlo simulation.

The goal is to:
- estimate total enchant cost
- measure number of attempts
- compare strategies (with vs without stone)
- evaluate risk and variability

---

## 2. Game Mechanics

Enchanting is a probabilistic system:

- Each level has a success chance
- On failure → item resets to +0
- This creates exponential growth in cost

Two modes:
- **No Stone** → base probabilities
- **With Stone (Lucky Mode)** → increased success chance but additional cost

---

## 3. Simulation

The system is modeled using Monte Carlo simulation.

Each run:
- simulates full enchant process from +0 to target level
- tracks:
  - items used
  - scrolls used
  - stones used
  - total cost

Implementation: :contentReference[oaicite:0]{index=0}

Key idea:
- thousands of runs → estimate real distribution (not just average)

---

## 4. Data & Metrics

From simulation we calculate:

- `total_enchant_cost`
- `items_used`
- delta (absolute growth)
- growth (relative increase)

Aggregation logic: :contentReference[oaicite:1]{index=1}

---

## 5. Analysis & Results

### Growth of Complexity

Cost and attempts grow exponentially with level.

- After ~+10 → sharp increase
- At +15–16 → extreme cost spike

Magic weapons are significantly more expensive:
- up to ~10x higher cost and attempts

---

### Magic vs Physical Weapons

Magic weapons require consistently higher investment across all levels.

- difference is multiplicative, not linear
- gap increases with level

---

### Impact of Stone

Using a stone reduces effective difficulty:

- +13 with stone ≈ +10 without stone
- equivalent to reducing complexity by 2–3 levels

---

### Local Effect (Armor)

For Full Armor:

- up to ~+8 → stone is inefficient
- stone cost > benefit

---

### Distribution Analysis

Cost distribution is highly skewed:

- **No Stone**
  - high variance
  - long expensive tail
  - risk of extreme cost

- **With Stone**
  - lower median
  - tighter distribution
  - fewer extreme outcomes

 Key effect:
Stone removes high-cost outliers and stabilizes the process.

---

## 6. Key Insights

- Enchanting cost grows exponentially
- Magic weapons are significantly more expensive
- Stone reduces both:
  - average cost
  - variance (risk)
- Main benefit of stone = **risk control**, not just cheaper average

---

## 7. How to Run

```bash
pip install pandas matplotlib
python run_experiment.py
python main.py
```
---

## 8 Project Structure
Enchantment_simulator_and_analyze/
│
├── simulation.py      # Monte Carlo simulation logic (core model)
├── analysis.py        # data aggregation and statistical metrics
├── visualize.py       # plotting and visualization functions
├── config.py          # probabilities and pricing configuration
│
├── run_experiment.py  # generates dataset (data.csv)
├── main.py            # runs analysis and builds plots
│
└── README.md