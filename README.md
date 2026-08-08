# Kaggriculture Simulation Bot, Test Bench & Sabotage Engine

This repository contains a suite of optimized simulation bots, a local evaluation test bench, and a round-robin tournament engine built for Kaggle's **Kaggriculture** competition—a turn-based, multi-agent farming simulation game.

---

## Game Overview

- **Objective**: Maximize final bank balance over a 30-day season (720 total turns per episode).
- **Farm Grid**: 10x10 grid divided into four 5x5 quadrants. Starts with only the NW quadrant unlocked; others are purchasable via `BUY_LAND`.
- **Crops**: Wheat, Carrot, Tomato, Strawberry, and Melon (each with unique seed costs, growth curves, and lifespan limits). Unwatered plants decay into weeds.
- **Labor**: Hired hands can scale up turn capacity per day. Hires follow Fibonacci cost scaling and reset daily.
- **Shed (Inventory)**: Non-seed capacity is capped at 100 items. Excess items are discarded at the end of the day.

---

## Strategy Evolution

### 1. The Heuristic Era (v1–v3)
* **[main.py](file:///Users/lavlinjaison/Desktop/python/kaggleculture/main.py):** Simple priority-queue based agent. Walks around watering crops, placing animals, and selling immediately. Net profit ~$17,400 vs. random.
* **[main_v2.py](file:///Users/lavlinjaison/Desktop/python/kaggleculture/old/main_v2.py) (Fertilizer Arbitrage):** Adds fertilizer priority scaling. Young Tomato and Strawberry crops are fertilized to double their yield, while Melon is ignored. Net profit ~$22,900 vs. random.
* **[main_v3.py](file:///Users/lavlinjaison/Desktop/python/kaggleculture/old/main_v3.py) (Livestock Safeguards):** Introduces turn-level Wheat inventory checks to buy feed immediately if animals are hungry, preventing animal starvation/escapes.

### 2. The Linear Programming Era (v4–v6)
* **[main_v4.py](file:///Users/lavlinjaison/Desktop/python/kaggleculture/old/main_v4.py) (10-Variable LP Solver):** Models Day 0 purchases using a 10-variable Linear Program (`scipy.optimize.linprog(method="highs")`) mapping both new purchases ($x_c$) and stock usage ($s_c$). Integrates dynamic worker limits and density-based land expansion to keep crops compact. Net profit ~$26,100 vs. random.
* **[main_v5.py](file:///Users/lavlinjaison/Desktop/python/kaggleculture/old/main_v5.py) (Dynamic Pricing & Safety Buffers):** Adds dynamic fertilizer pricing (holding fertilizer during gluts and selling when price $\ge \$80$) and animal purchase safety buffers (Goose needs $400, Cow needs $550).
* **[main_v6.py](file:///Users/lavlinjaison/Desktop/python/kaggleculture/old/main_v6.py) (Monoculture Optimization):** Restricts animal scaling to exactly 1 coop and 1 pasture. Prioritizes Melon/Strawberry monoculture and imports feed on the market rather than wasting crop tiles on low-value Wheat.

### 3. The Optimization & Logistics Era (v7–v9)
* **[main_v7.py](file:///Users/lavlinjaison/Desktop/python/kaggleculture/old/main_v7.py) (Hyperparameter Tuned LP):** Grid-search optimized over 27 safety buffer, diversity cap, and price decay coordinates. Scored **$27,655** vs. random.
* **[main_v8.py](file:///Users/lavlinjaison/Desktop/python/kaggleculture/main_v8.py) (Hour-Level Cutoff & Safety Buffer Decay):** Adds hour-level remaining game time calculations mapping exact maturity limits and safety cash buffer decay ($200 scaling to $0 by Day 28) to release locked capital. Clean-sweep victory against all v1–v7 opponents.
* **[main_v9.py](file:///Users/lavlinjaison/Desktop/python/kaggleculture/main_v9.py) (Dynamic Capacity Limits):** Experimental version introducing adaptive capacity bounds and worker scheduling parameters adjusted dynamically by day progression. Underperforms in competitive sabotage scenarios.

### 4. The Sabotage & Static-Schedule Era (Ben / Venks / Saboteurs)
* **[ben.py](file:///Users/lavlinjaison/Desktop/python/kaggleculture/ben.py) (Optimized Static Schedule):** Implements a premium static execution schedule derived from top-tier replays. Features optimized pathfinding priorities, automatic center-tile drops, and a pasture list iterator fix.
* **[ben_v2.py](file:///Users/lavlinjaison/Desktop/python/kaggleculture/ben_v2.py) (Hoarding & Fertilizer Capping):** Adds dynamic price hoarding (holding goods until market prices peak), fertilizer caps to minimize waste, and custom Day 18 Melon purchases.
* **[venks_variant.py](file:///Users/lavlinjaison/Desktop/python/kaggleculture/venks_variant.py) (Shifted Schedules):** Explores timeline modifications to Venks schedules combined with adaptive price logic.
* **[venks_killer.py](file:///Users/lavlinjaison/Desktop/python/kaggleculture/venks_killer.py) (Sabotage Hybrid fallback):** Dual-logic agent. Plays a dynamic general-purpose strategy by default, but switches to high-priority target front-running if it detects the static `venks` schedule from the opponent.
* **[venks_killer_dynamic.py](file:///Users/lavlinjaison/Desktop/python/kaggleculture/venks_killer_dynamic.py) (Dynamic Opponent Shed Tracking):** Dynamically estimates the opponent's shed contents in real-time by tracking crop harvests and pasture collections, combined with farmer/hands location checks near the center shed. When items are detected in the opponent's inventory, it triggers front-running sells to crash the market price before the opponent can liquidate.
* **[venks_killer_hybrid.py](file:///Users/lavlinjaison/Desktop/python/kaggleculture/venks_killer_hybrid.py) (1-Hour Schedule Shift & Front-Runner):** Plays the optimal schedule with a 1-hour shift starting at Step 0 (instead of Step 1) to preempt the opponent. Dynamically detects static opponents at Step 47 (inspecting melon tile counts) and injects targeted market sales exactly 1 step prior to opponent liquidations. Currently the **undefeated #1 rank** in the local tournament.

---

## Double Round-Robin Tournament Leaderboard

All local agent variations are evaluated in a double round-robin tournament (double-sided play, 720 turns/episode) via [run_tournament.py](file:///Users/lavlinjaison/Desktop/python/kaggleculture/run_tournament.py).

The current leaderboard results (persisted in [tournament_report.md](file:///Users/lavlinjaison/Desktop/python/kaggleculture/tournament_report.md)):

| Rank | Agent Name | Wins | Draws | Losses | Points | Win Rate % | Avg Score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | [venks_killer_hybrid.py](file:///Users/lavlinjaison/Desktop/python/kaggleculture/venks_killer_hybrid.py) | 20 | 0 | 0 | **60** | 100.0% | $172,938.9 |
| **2** | [venks_killer_dynamic.py](file:///Users/lavlinjaison/Desktop/python/kaggleculture/venks_killer_dynamic.py) | 18 | 0 | 2 | **54** | 90.0% | $157,593.1 |
| **3** | [ben.py](file:///Users/lavlinjaison/Desktop/python/kaggleculture/ben.py) | 16 | 0 | 4 | **48** | 80.0% | $113,585.4 |
| **4** | [venks_killer.py](file:///Users/lavlinjaison/Desktop/python/kaggleculture/venks_killer.py) | 14 | 0 | 6 | **42** | 70.0% | $80,394.0 |
| **5** | [ben_v2.py](file:///Users/lavlinjaison/Desktop/python/kaggleculture/ben_v2.py) | 11 | 1 | 8 | **34** | 55.0% | $72,602.0 |
| **6** | [venks_variant.py](file:///Users/lavlinjaison/Desktop/python/kaggleculture/venks_variant.py) | 10 | 1 | 9 | **31** | 50.0% | $71,269.0 |
| **7** | [main_v8.py](file:///Users/lavlinjaison/Desktop/python/kaggleculture/main_v8.py) | 8 | 0 | 12 | **24** | 40.0% | $21,977.5 |
| **8** | [main_v9.py](file:///Users/lavlinjaison/Desktop/python/kaggleculture/main_v9.py) | 5 | 0 | 15 | **15** | 25.0% | $11,799.9 |
| **9** | [main.py](file:///Users/lavlinjaison/Desktop/python/kaggleculture/main.py) | 4 | 0 | 16 | **12** | 20.0% | $13,856.7 |
| **10** | `starter` | 3 | 0 | 17 | **9** | 15.0% | $3,498.4 |
| **11** | `random` | 0 | 0 | 20 | **0** | 0.0% | $1.5 |

---

## Project Structure

```
.
├── ben.py                     # Static schedule bot with pathfinding improvements
├── ben_v2.py                  # static schedule bot with price hoarding
├── main.py                    # Heuristic bot (v1)
├── main_v8.py                 # LP solver with safety buffer decay
├── main_v9.py                 # LP solver with dynamic capacity
├── old/                       # Archive of older LP iterations (v2–v7)
│   ├── main_v2.py
│   ├── main_v3.py
│   ├── main_v4.py
│   ├── main_v5.py
│   ├── main_v6.py
│   └── main_v7.py
├── run_local.py               # Plays a single local match against a given strategy
├── run_tournament.py          # Simulates a double round-robin tournament between all bots
├── tournament_report.md       # Persisted tournament leaderboard markdown file
├── venks_killer.py            # Sabotage fallback bot
├── venks_killer_dynamic.py    # Sabotage bot with real-time opponent shed tracking
├── venks_killer_hybrid.py     # Undefeated sabotage bot with 1-hour preemption logic
└── venks_variant.py           # Venks schedule variants
```

---

## Getting Started

### Prerequisites

You need `python3`, `scipy`, and `kaggle-environments` installed.

```bash
pip install -U kaggle-environments scipy --break-system-packages
```

### Running a Local Match

Use [run_local.py](file:///Users/lavlinjaison/Desktop/python/kaggleculture/run_local.py) to simulate single episodes:

```bash
python3 run_local.py
```

### Running the Tournament

To update leaderboard standings after modifying strategies, run the tournament suite:

```bash
python3 run_tournament.py
```
