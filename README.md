# Kaggriculture Simulation Bot & Test Bench

This repository contains a suite of optimized simulation bots and a local evaluation test bench built for Kaggle's **Kaggriculture** competition—a turn-based, multi-agent farming simulation game.

---

## Game Overview

- **Objective**: Maximize final bank balance over a 30-day season (720 total turns per episode).
- **Farm Grid**: 10x10 grid divided into four 5x5 quadrants. Starts with only the NW quadrant unlocked; others are purchasable via `BUY_LAND`.
- **Crops**: Wheat, Carrot, Tomato, Strawberry, and Melon (each with unique seed costs, growth curves, and lifespan limits). Unwatered plants decay into weeds.
- **Labor**: Hired hands can scale up turn capacity per day. Hires follow Fibonacci cost scaling and reset daily.
- **Shed (Inventory)**: Non-seed capacity is capped at 100 items. Excess items are discarded at the end of the day.

---

## Strategy Evolution (Versions 1 to 7)

### 1. The Heuristic Era (v1–v3)
* **`main.py` (v1 Baseline):** Simple priority-queue based agent. Walks around watering crops, placing animals, and selling immediately. Net profit ~$17,400 vs. random.
* **`main_v2.py` (Fertilizer Arbitrage):** Adds fertilizer priority scaling. Young Tomato and Strawberry crops are fertilized to double their yield, while Melon is ignored. Net profit ~$22,900 vs. random.
* **`main_v3.py` (Livestock Safeguards):** Introduces turn-level Wheat inventory checks to buy feed immediately if animals are hungry, preventing animal starvation/escapes.

### 2. The Linear Programming Era (v4–v6)
* **`main_v4.py` (10-Variable LP Solver):** Models Day 0 purchases using a 10-variable Linear Program (`scipy.optimize.linprog(method="highs")`) mapping both new purchases ($x_c$) and stock usage ($s_c$). Integrates dynamic worker limits and density-based land expansion to keep crops compact. Net profit ~$26,100 vs. random.
* **`main_v5.py` (Dynamic Pricing & Safety Buffers):** Adds dynamic fertilizer pricing (holding fertilizer during gluts and selling when price $\ge \$80$) and animal purchase safety buffers (Goose needs $400, Cow needs $550).
* **`main_v6.py` (Monoculture Optimization):** Restricts animal scaling to exactly 1 coop and 1 pasture. Prioritizes Melon/Strawberry monoculture and imports feed on the market rather than wasting crop tiles on low-value Wheat.

### 3. The Parameter Optimization Era (v7)
* **`main_v7.py` (Hyperparameter Tuned LP):** Conducted an offline grid search tuning process over 27 combinations of safety buffer mapping, diversity cap bounds, and price decay divisor variables. Tuned parameters (SB=200.0, DL=0.45, PDD=2500.0) compiled directly into the LP solver. 
* **Outcome:** Achieved a tournament-leading **$27,655** vs. random, and completely dominated version 6 head-to-head (**$24,640** vs. **$19,082**).

---

## Head-to-Head Tournament Matrix

A round-robin tournament was simulated where every agent version played as both Player 0 (P0) and Player 1 (P1) against all other agents:

| Agent (P0) \ Opponent (P1) | random | starter | main.py | main_v2.py | main_v3.py | main_v4.py | main_v5.py | main_v6.py | main_v7.py |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **random** | $0 / $0 | $0 / $3509 | $540 / $38292 | $0 / $23558 | $0 / $23123 | $0 / $26109 | $0 / $25987 | $0 / $25926 | $0 / $27639 |
| **starter** | $3514 / $0 | $3506 / $3506 | $3496 / $15789 | $3501 / $23196 | $3491 / $21990 | $3514 / $25847 | $3487 / $25942 | $3501 / $25855 | $3518 / $27647 |
| **main.py** | $17412 / $0 | $15820 / $3503 | $14136 / $16133 | $16141 / $20397 | $26153 / $20513 | $13690 / $22769 | $12817 / $19947 | $2415 / $24834 | $11097 / $24846 |
| **main_v2.py** | $22901 / $0 | $21682 / $3514 | $21094 / $14796 | $20848 / $20848 | $20194 / $21312 | $20635 / $24327 | $20663 / $24346 | $21076 / $24058 | $17691 / $25603 |
| **main_v3.py** | $22507 / $0 | $23054 / $3491 | $19603 / $13491 | $21065 / $21636 | $21308 / $21308 | $18903 / $23716 | $20902 / $24290 | $20998 / $24116 | $20202 / $25347 |
| **main_v4.py** | $26169 / $0 | $26141 / $3497 | $22844 / $14598 | $24222 / $19716 | $24426 / $20634 | $19428 / $22629 | $22794 / $22794 | $22993 / $22993 | $17125 / $24279 |
| **main_v5.py** | $27752 / $0 | $25988 / $3514 | $20270 / $21065 | $24191 / $20396 | $24421 / $20359 | $23039 / $23039 | $22698 / $22698 | $22787 / $22787 | $20457 / $24311 |
| **main_v6.py** | $26082 / $0 | $25933 / $3509 | $22734 / $15798 | $24080 / $21108 | $24234 / $18455 | $24441 / $22991 | $22906 / $22906 | $22777 / $22777 | $18514 / $24281 |
| **main_v7.py** | **$27,655** / $0 | **$27,673** / $3,507 | **$26,507** / $5,172 | **$25,384** / $19,648 | **$25,593** / $19,632 | **$24,291** / $20,226 | **$24,290** / $20,473 | **$24,640** / $19,082 | $21,040 / $21,040 |

*Values display: **P0 Cash Balance / P1 Cash Balance**.*

---

## Project Structure

- **[main_v7.py](main_v7.py)**: The peak tuned entry point for the Kaggle submission, housing the `agent(observation, configuration)` function.
- **[run_local.py](run_local.py)**: A local match evaluation bench that plays the agent against other strategies (e.g. `random`, `starter`, or itself) and logs performance.

---

## Getting Started

### Prerequisites

You need `python3`, `scipy`, and `kaggle-environments` installed.

```bash
pip install -U kaggle-environments scipy --break-system-packages
```

### Running the Local Test Bench

Run the test bench script to play simulated episodes:

```bash
python3 run_local.py
```
