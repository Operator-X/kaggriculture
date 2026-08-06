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

## Strategy Evolution (Versions 1 to 8)

### 1. The Heuristic Era (v1–v3)
* **`main.py` (v1 Baseline):** Simple priority-queue based agent. Walks around watering crops, placing animals, and selling immediately. Net profit ~$17,400 vs. random.
* **`main_v2.py` (Fertilizer Arbitrage):** Adds fertilizer priority scaling. Young Tomato and Strawberry crops are fertilized to double their yield, while Melon is ignored. Net profit ~$22,900 vs. random.
* **`main_v3.py` (Livestock Safeguards):** Introduces turn-level Wheat inventory checks to buy feed immediately if animals are hungry, preventing animal starvation/escapes.

### 2. The Linear Programming Era (v4–v6)
* **`main_v4.py` (10-Variable LP Solver):** Models Day 0 purchases using a 10-variable Linear Program (`scipy.optimize.linprog(method="highs")`) mapping both new purchases ($x_c$) and stock usage ($s_c$). Integrates dynamic worker limits and density-based land expansion to keep crops compact. Net profit ~$26,100 vs. random.
* **`main_v5.py` (Dynamic Pricing & Safety Buffers):** Adds dynamic fertilizer pricing (holding fertilizer during gluts and selling when price $\ge \$80$) and animal purchase safety buffers (Goose needs $400, Cow needs $550).
* **`main_v6.py` (Monoculture Optimization):** Restricts animal scaling to exactly 1 coop and 1 pasture. Prioritizes Melon/Strawberry monoculture and imports feed on the market rather than wasting crop tiles on low-value Wheat.

### 3. The Optimization & Logistics Era (v7–v8)
* **`main_v7.py` (Hyperparameter Tuned LP):** Grid-search optimized over 27 safety buffer, diversity cap, and price decay coordinates. Scored **$27,655** vs. random.
* **`main_v8.py` (Hour-Level Cutoff & Safety Buffer Decay):** Adds hour-level remaining game time calculations mapping exact maturity limits and safety cash buffer decay ($200 scaling to $0 by Day 28) to release locked capital.
* **Outcome:** Clean-sweep victory against all opponents on the tournament grid, and outclassed version 7 head-to-head (**$23,910** vs. **$18,275**).

---

## Head-to-Head Tournament Matrix

A round-robin tournament was simulated where every agent version played as both Player 0 (P0) and Player 1 (P1) against all other agents:

| Agent (P0) \ Opponent (P1) | random | starter | main.py | main_v2.py | main_v3.py | main_v4.py | main_v5.py | main_v6.py | main_v7.py | main_v8.py |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **random** | $0 / $0 | $0 / $3518 | $0 / $19052 | $0 / $22959 | $0 / $23680 | $40 / $25961 | $0 / $26155 | $0 / $25480 | $0 / $27658 | $0 / $27661 |
| **starter** | $3516 / $0 | $3516 / $3516 | $3499 / $19052 | $3504 / $23073 | $3485 / $23177 | $3487 / $26210 | $3499 / $26142 | $3489 / $25849 | $3501 / $27662 | $3487 / $27674 |
| **main.py** | $24973 / $0 | $15789 / $3510 | $13057 / $16354 | $13481 / $20808 | $13426 / $19160 | $14801 / $22330 | $13690 / $23150 | $18972 / $22098 | $10769 / $23790 | $12748 / $23385 |
| **main_v2.py** | $23246 / $0 | $23342 / $3489 | $20243 / $16056 | $21290 / $19353 | $19661 / $21559 | $20670 / $24114 | $20628 / $24312 | $20547 / $24342 | $19442 / $25098 | $19494 / $25138 |
| **main_v3.py** | $23250 / $40 | $23014 / $3509 | $22345 / $200 | $21143 / $21641 | $21645 / $21443 | $20586 / $24128 | $20931 / $24184 | $20859 / $24029 | $19199 / $25741 | $19723 / $25617 |
| **main_v4.py** | $27975 / $110 | $26037 / $3507 | $23125 / $11420 | $24010 / $20666 | $23867 / $20233 | $22499 / $22499 | $22971 / $22971 | $22635 / $22635 | $19932 / $24260 | $22496 / $21349 |
| **main_v5.py** | $25803 / $20 | $26043 / $3508 | $20562 / $12647 | $24325 / $20570 | $24289 / $21014 | $22879 / $22879 | $22905 / $22905 | $22618 / $22618 | $20246 / $24285 | $18121 / $24477 |
| **main_v6.py** | $26227 / $0 | $25944 / $3487 | $23143 / $13690 | $24032 / $20585 | $24253 / $19759 | $19664 / $22988 | $22737 / $22737 | $22895 / $22895 | $20158 / $24259 | $20155 / $24269 |
| **main_v7.py** | $27670 / $0 | $27667 / $3510 | $21331 / $13050 | $25133 / $19848 | $25721 / $18251 | $23387 / $20467 | $24290 / $20025 | $24287 / $20303 | $18264 / $23927 | $21013 / $21013 |
| **main_v8.py** | **$27,662** / $0 | **$27,663** / $3,499 | **$23,394** / $9,390 | **$24,074** / $19,784 | **$25,444** / $19,198 | **$24,297** / $20,418 | **$24,294** / $20,357 | **$24,291** / $20,223 | **$23,910** / $18,275 | $19,575 / $23,956 |

*Values display: **P0 Cash Balance / P1 Cash Balance**.*

---

## Project Structure

- **[main_v8.py](main_v8.py)**: The peak tuned entry point for the Kaggle submission, housing the `agent(observation, configuration)` function.
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
