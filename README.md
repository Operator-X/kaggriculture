# Kaggriculture Simulation Bot & Test Bench

This repository contains a Greedy Priority-Upkeep Rule Bot and a local evaluation test bench built for Kaggle's **Kaggriculture** competition—a turn-based, multi-agent farming simulation game.

## Game Overview

- **Objective**: Maximize final bank balance over a 30-day season (720 total turns per episode).
- **Farm Grid**: 10x10 grid divided into four 5x5 quadrants. Starts with only the NW quadrant unlocked; others are purchasable via `BUY_LAND`.
- **Crops**: Wheat, Carrot, Tomato, Strawberry, and Melon (each with unique seed costs, growth curves, and lifespan limits). Unwatered plants decay into weeds.
- **Labor**: Hired hands can scale up turn capacity per day. Hires follow Fibonacci cost scaling and reset daily.
- **Shed (Inventory)**: Non-seed capacity is capped at 100 items. Excess items are discarded at the end of the day.

---

## Strategy & Architecture

We implement a robust **Greedy Priority-Upkeep Rule Bot** that schedules tasks dynamically and executes them using Manhattan distance routing. It features several key economic control policies to resolve standard simulation traps:

1. **FSM Task Priority Queue**:
   - **Priority 10**: Upkeep (Watering thirsty crops & feeding hungry livestock).
   - **Priority 20**: Harvesting mature crops/produce and animal products.
   - **Priority 25**: Gathering animal fertilizer.
   - **Priority 30**: Digging weeds to reclaim empty tiles.
   - **Priority 40**: Replanting empty tiles with the most profitable crop.

2. **Single-Hour Trading**:
   - Restricts all `BUY_SEED`, `BUY_PRODUCT`, `BUY_LAND`, and `HIRE` market orders to the first hour of each day (`hour == 0`).
   - This prevents the "delayed feedback loop" that causes agents to duplicate orders on subsequent turns of the same day and drain capital.

3. **Dynamic Safety Buffer**:
   - Normal safety capital buffer is `$200.0`.
   - If the agent has 0 crops growing and 0 seeds in inventory, the safety buffer drops dynamically to `$20.0` to bootstrap purchasing and prevent a **poverty trap lockout**.

4. **Labor-Predictive Scaling**:
   - Scales planting count limits to match the number of active units (farmer + hired hands) so that crops never die of thirst.
   - Caps max hands based on the unlocked quadrants to ensure we never over-hire hands beyond our land capacity.

---

## Project Structure

- **[main.py](main.py)**: The self-contained entry point for the Kaggle submission, housing the `agent(observation, configuration)` function and helper functions.
- **[run_local.py](run_local.py)**: A local match evaluation bench that plays the agent against other strategies (e.g. `random`, `starter`, or itself) and logs performance.

---

## Getting Started

### Prerequisites

You need `python3` and `kaggle-environments` installed.

```bash
pip install -U kaggle-environments --break-system-packages
```

### Running the Local Test Bench

Run the test bench script to play simulated episodes:

```bash
python3 run_local.py
```

### Local Evaluation Outcomes

A typical simulation run outputs the following rewards:
- **vs `"random"`**: Our agent easily defeats the random policy, netting **`~$1600 - $3000`** in cash depending on market shifts.
- **vs `"starter"` (Carrot Loop)**: Our agent beats the starter agent, earning **`~$3596`** vs `$3512`.
- **Self-Play (`main.py` vs itself)**: Both agents successfully scale, farm, and trade concurrently, yielding competitive final balances (**`~$2150`** and **`~$2850`**) in a shared, dynamically price-sensitive market.
