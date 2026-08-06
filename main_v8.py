import math
from scipy.optimize import linprog

# Constants
SAFETY_BUFFER = 200.0
LAND_PRICES = [1000.0, 2000.0, 4000.0]
LAND_ORDER = ["NE", "SW", "SE"]
LAND_BUY_THRESHOLDS = [2000.0, 3500.0, 6000.0]

CROPS = {
    "WHEAT": {"seed_cost": 10, "max_yield_day": 4, "first_yield_day": 2, "ongoing": False, "base_yield": 4, "base_price": 25.0},
    "CARROT": {"seed_cost": 20, "max_yield_day": 3, "first_yield_day": 2, "ongoing": False, "base_yield": 3, "base_price": 35.0},
    "TOMATO": {"seed_cost": 50, "max_yield_day": 11, "first_yield_day": 8, "ongoing": True, "base_yield": 4, "base_price": 60.0},
    "STRAWBERRY": {"seed_cost": 100, "max_yield_day": 16, "first_yield_day": 10, "ongoing": True, "base_yield": 4, "base_price": 120.0},
    "MELON": {"seed_cost": 80, "max_yield_day": 10, "first_yield_day": 10, "ongoing": False, "base_yield": 6, "base_price": 250.0},
}

BASE_PRICES = {
    "WHEAT": 25.0,
    "CARROT": 35.0,
    "TOMATO": 60.0,
    "STRAWBERRY": 120.0,
    "MELON": 250.0,
    "EGG": 50.0,
    "MILK": 160.0,
    "WOOL": 200.0,
    "FERTILIZER": 100.0,
}

CENTER_TILES = [(4, 4), (5, 4), (4, 5), (5, 5)]

def get_fib(n):
    """Computes the n-th Fibonacci number (1, 1, 2, 3, 5, 8, 13, 21, ...) for n >= 0."""
    if n < 0:
        return 0
    if n == 0 or n == 1:
        return 1
    a, b = 1, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b

def get_distance(pos1, pos2):
    """Manhattan distance between two points."""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def get_closest_center(pos):
    """Finds the closest center tile and distance to it."""
    best_dist = float("inf")
    best_tile = CENTER_TILES[0]
    for cx, cy in CENTER_TILES:
        dist = get_distance(pos, (cx, cy))
        if dist < best_dist:
            best_dist = dist
            best_tile = (cx, cy)
    return best_tile, best_dist

def route_towards(current, target):
    """Computes a 1-step move towards the target."""
    cx, cy = current
    tx, ty = target
    if tx > cx:
        return ["EAST"]
    elif tx < cx:
        return ["WEST"]
    elif ty > cy:
        return ["SOUTH"]
    elif ty < cy:
        return ["NORTH"]
    return ["PASS"]

def agent(observation, configuration=None):
    player = observation["player"]
    day = observation["day"]
    hour = observation["hour"]
    me = observation["farms"][player]
    private = observation["private"]
    market_prices = observation["market"]["prices"]
    tiles = me["tiles"]
    money = me["money"]
    n_unlocked_quads = len(me["unlocked_quadrants"])
    
    # Dynamic capacity parameters based on day
    if day < 5:
        cap_per_worker = 8
        plant_limit_per_worker = 6
    else:
        cap_per_worker = 9
        plant_limit_per_worker = 9
        
    # 1. Gather all units and their inventories
    farmer_pos = me["farmer"]
    hands_pos = me["hands"]
    unit_positions = [farmer_pos] + list(hands_pos)
    unit_inventories = private["inventories"]
    num_units = len(unit_positions)
    
    # Ensure unit_inventories has enough slots
    while len(unit_inventories) < num_units:
        unit_inventories.append({})
        
    # Count active crops by species
    crop_counts = {crop: 0 for crop in CROPS}
    active_crops_count = 0
    for row in tiles:
        for tile in row:
            if isinstance(tile, dict) and tile.get("kind") == "PLANT":
                crop = tile["crop"]
                if crop in crop_counts:
                    crop_counts[crop] += 1
                active_crops_count += 1
                
    has_animals = any(
        isinstance(tile, dict) and tile.get("kind") in ("COOP", "PASTURE") and tile.get("animal") is not None
        for row in tiles for tile in row
    )
    seeds_owned = sum(private["seeds"].values())
    
    # Dynamic safety buffer: bootstrap gets 20, Day >= 24 decays to 0, other phases get optimal 200.0
    if active_crops_count == 0 and seeds_owned == 0 and not has_animals:
        current_safety_buffer = 20.0
    elif day >= 24:
        current_safety_buffer = max(0.0, SAFETY_BUFFER * (28 - day) / 4.0)
    else:
        current_safety_buffer = SAFETY_BUFFER
        
    # 2. Identify and rank active tasks on the farm
    tasks = []
    new_plant_tasks_count = 0
    
    # Scan coops, pastures, and empty tiles
    coops = []
    pastures = []
    empty_tiles = []
    
    for y in range(10):
        for x in range(10):
            tile = tiles[y][x]
            if tile == "LOCKED":
                continue
            if tile is None:
                empty_tiles.append((x, y))
            elif isinstance(tile, dict):
                kind = tile.get("kind")
                if kind == "COOP":
                    coops.append(((x, y), tile))
                elif kind == "PASTURE":
                    pastures.append(((x, y), tile))

    # Add mid-day Drop/Sell tasks for units
    for u_idx in range(num_units):
        u_pos = unit_positions[u_idx]
        u_inv = unit_inventories[u_idx]
        inv_size = sum(u_inv.values())
        
        # Day 29 drop has top priority (Priority 5). Regular drop has priority 35.
        if (day == 29 and inv_size > 0) or (inv_size >= 10):
            cx, cy = get_closest_center(u_pos)[0]
            tasks.append({
                "pos": (cx, cy),
                "action": "DROP_INVENTORY",
                "priority": 5 if day == 29 else 35
            })
            


    # Scan tiles for actions
    for y in range(10):
        for x in range(10):
            tile = tiles[y][x]
            if tile == "LOCKED":
                continue
                
            if day == 29:
                # Day 29 logic: ONLY harvest is allowed
                if isinstance(tile, dict):
                    kind = tile.get("kind")
                    if kind in ("PLANT", "COOP", "PASTURE"):
                        if tile.get("yield_units", 0) > 0:
                            tasks.append({
                                "pos": (x, y),
                                "action": "HARVEST",
                                "priority": 20
                            })
                continue
                
            if tile is None:
                # Build coops and pastures if we have enough money and space
                # Delay building until Day 4 and money >= 1500 to avoid bootstrapping cash issues
                # Limit to exactly 1 coop and 1 pasture to prevent labor overcrowding
                if day >= 4 and day < 20:
                    if len(coops) < 1 and money >= 1500:
                        tasks.append({
                            "pos": (x, y),
                            "action": "BUILD_COOP",
                            "priority": 45
                        })
                        coops.append(((x, y), {"kind": "COOP", "animal": None}))
                        continue
                    elif len(pastures) < 1 and money >= 1800:
                        tasks.append({
                            "pos": (x, y),
                            "action": "BUILD_PASTURE",
                            "priority": 45
                        })
                        pastures.append(((x, y), {"kind": "PASTURE", "animal": None}))
                        continue
                
                # Check for planting crops
                # Limit planting hours to hour < 18 to ensure we water it on day 0 and protect end-of-day labor allocation
                if hour < 18:
                    remaining_hours = (28 - day) * 24 + (23 - hour)
                    eligible_crops = []
                    for crop, count in private["seeds"].items():
                        if count > 0:
                            needed_hours = CROPS[crop]["max_yield_day"] * 24
                            if remaining_hours >= needed_hours:
                                eligible_crops.append(crop)
                            
                    if len(eligible_crops) > 0:
                        # Pick the most profitable one we have in stock
                        best_crop = None
                        best_profit = -float("inf")
                        for crop in eligible_crops:
                            crop_data = CROPS[crop]
                            live_price = market_prices.get(crop, crop_data["base_price"])
                            profit = crop_data["base_yield"] * live_price - crop_data["seed_cost"]
                            if profit > best_profit:
                                best_profit = profit
                                best_crop = crop
                                
                        if best_crop and new_plant_tasks_count < num_units * 4:
                            tasks.append({
                                "pos": (x, y),
                                "action": f"PLANT_{best_crop}",
                                "priority": 50
                            })
                            new_plant_tasks_count += 1
                            
            elif isinstance(tile, dict):
                kind = tile.get("kind")
                if kind == "PLANT":
                    crop = tile["crop"]
                    crop_data = CROPS[crop]
                    age = day - tile["planted_day"]
                    
                    # Water crop
                    if not tile["watered_today"]:
                        tasks.append({
                            "pos": (x, y),
                            "action": "WATER",
                            "priority": 10
                        })
                        
                    # Fertilize Tomato and Strawberry ONLY (Melon is not cost-effective)
                    if (
                        crop in ("STRAWBERRY", "TOMATO")
                        and tile.get("fertilized_until_day", -1) < day
                        and age < crop_data["max_yield_day"] - 2
                    ):
                        tasks.append({
                            "pos": (x, y),
                            "action": "FERTILIZE",
                            "priority": 15
                        })
                        
                    # Harvest crops
                    is_mature = False
                    if not crop_data["ongoing"]:
                        is_mature = age >= crop_data["max_yield_day"] or day == 28
                    else:
                        is_mature = tile.get("yield_units", 0) > 0
                        
                    if is_mature and tile.get("yield_units", 0) > 0:
                        tasks.append({
                            "pos": (x, y),
                            "action": "HARVEST",
                            "priority": 20
                        })
                        
                elif kind in ("COOP", "PASTURE"):
                    animal = tile.get("animal")
                    if animal is None:
                        # Unoccupied structure - check if animal is in transit to place it
                        if kind == "COOP":
                            geese_in_shed = private["shed"].get("GOOSE", 0)
                            geese_in_inv = sum(inv.get("GOOSE", 0) for inv in unit_inventories)
                            if geese_in_shed > 0 or geese_in_inv > 0:
                                tasks.append({
                                    "pos": (x, y),
                                    "action": "PLACE_GOOSE",
                                    "priority": 40
                                })
                        elif kind == "PASTURE":
                            cows_in_shed = private["shed"].get("COW", 0)
                            cows_in_inv = sum(inv.get("COW", 0) for inv in unit_inventories)
                            if cows_in_shed > 0 or cows_in_inv > 0:
                                tasks.append({
                                    "pos": (x, y),
                                    "action": "PLACE_COW",
                                    "priority": 40
                                })
                    else:
                        # Feed animal
                        if not tile["fed_today"]:
                            tasks.append({
                                "pos": (x, y),
                                "action": "FEED",
                                "priority": 10
                            })
                            
                        # Care animal
                        if not tile.get("cared_today", False):
                            tasks.append({
                                "pos": (x, y),
                                "action": "CARE",
                                "priority": 12
                            })
                            
                        # Harvest produce
                        if tile.get("yield_units", 0) > 0:
                            tasks.append({
                                "pos": (x, y),
                                "action": "HARVEST",
                                "priority": 20
                            })
                            
                        # Collect fertilizer
                        if tile.get("fertilizer_available", False):
                            tasks.append({
                                "pos": (x, y),
                                "action": "COLLECT_FERTILIZER",
                                "priority": 25
                            })
                            
                elif kind == "WEED":
                    # Only clear weeds if we are before Day 25
                    if day < 25:
                        tasks.append({
                            "pos": (x, y),
                            "action": "DIG",
                            "priority": 60
                        })

    # Sort tasks: highest priority first (lower value of priority)
    tasks.sort(key=lambda t: t["priority"])
    
    # 3. Greedy unit task assignment
    unit_assignments = [None] * num_units
    assigned_task_positions = set()
    
    for task in tasks:
        task_pos = task["pos"]
        task_action = task["action"]
        
        # Multiple units can drop inventory at the center, so we do not restrict center positions
        if task_action != "DROP_INVENTORY" and task_pos in assigned_task_positions:
            continue
            
        best_unit_idx = -1
        best_dist = float("inf")
        
        for u_idx in range(num_units):
            if unit_assignments[u_idx] is not None:
                continue
                
            u_pos = unit_positions[u_idx]
            u_inv = unit_inventories[u_idx]
            
            # Check availability of required items
            if task_action == "FEED":
                has_wheat = u_inv.get("WHEAT", 0) > 0
                shed_has_wheat = private["shed"].get("WHEAT", 0) > 0
                if not (has_wheat or shed_has_wheat):
                    continue
                dist = get_distance(u_pos, task_pos) if has_wheat else (get_closest_center(u_pos)[1] + get_closest_center(task_pos)[1])
            elif task_action == "FERTILIZE":
                has_fert = u_inv.get("FERTILIZER", 0) > 0
                shed_has_fert = private["shed"].get("FERTILIZER", 0) > 0
                if not (has_fert or shed_has_fert):
                    continue
                dist = get_distance(u_pos, task_pos) if has_fert else (get_closest_center(u_pos)[1] + get_closest_center(task_pos)[1])
            elif task_action == "PLACE_GOOSE":
                has_goose = u_inv.get("GOOSE", 0) > 0
                shed_has_goose = private["shed"].get("GOOSE", 0) > 0
                if not (has_goose or shed_has_goose):
                    continue
                dist = get_distance(u_pos, task_pos) if has_goose else (get_closest_center(u_pos)[1] + get_closest_center(task_pos)[1])
            elif task_action == "PLACE_COW":
                has_cow = u_inv.get("COW", 0) > 0
                shed_has_cow = private["shed"].get("COW", 0) > 0
                if not (has_cow or shed_has_cow):
                    continue
                dist = get_distance(u_pos, task_pos) if has_cow else (get_closest_center(u_pos)[1] + get_closest_center(task_pos)[1])
            else:
                dist = get_distance(u_pos, task_pos)
                
            if dist < best_dist:
                best_dist = dist
                best_unit_idx = u_idx
                
        if best_unit_idx != -1:
            unit_assignments[best_unit_idx] = task
            if task_action != "DROP_INVENTORY":
                assigned_task_positions.add(task_pos)
            
    # 4. Generate actions for each unit based on assignment
    unit_actions = []
    for u_idx in range(num_units):
        u_pos = unit_positions[u_idx]
        u_inv = unit_inventories[u_idx]
        task = unit_assignments[u_idx]
        
        if task is None:
            # Idle behavior: move to center tile (4,4)
            if tuple(u_pos) in CENTER_TILES:
                unit_actions.append(["PASS"])
            else:
                unit_actions.append(route_towards(u_pos, (4, 4)))
        else:
            t_pos = task["pos"]
            action = task["action"]
            
            if action == "FEED":
                if u_inv.get("WHEAT", 0) > 0:
                    if tuple(u_pos) == t_pos:
                        unit_actions.append(["FEED"])
                    else:
                        unit_actions.append(route_towards(u_pos, t_pos))
                else:
                    if tuple(u_pos) in CENTER_TILES:
                        unit_actions.append(["PICKUP", "WHEAT", 1])
                    else:
                        cx, cy = get_closest_center(u_pos)[0]
                        unit_actions.append(route_towards(u_pos, (cx, cy)))
            elif action == "FERTILIZE":
                if u_inv.get("FERTILIZER", 0) > 0:
                    if tuple(u_pos) == t_pos:
                        unit_actions.append(["FERTILIZE"])
                    else:
                        unit_actions.append(route_towards(u_pos, t_pos))
                else:
                    if tuple(u_pos) in CENTER_TILES:
                        unit_actions.append(["PICKUP", "FERTILIZER", 1])
                    else:
                        cx, cy = get_closest_center(u_pos)[0]
                        unit_actions.append(route_towards(u_pos, (cx, cy)))
            elif action == "PLACE_GOOSE":
                if u_inv.get("GOOSE", 0) > 0:
                    if tuple(u_pos) == t_pos:
                        unit_actions.append(["PLACE", "GOOSE"])
                    else:
                        unit_actions.append(route_towards(u_pos, t_pos))
                else:
                    if tuple(u_pos) in CENTER_TILES:
                        unit_actions.append(["PICKUP", "GOOSE", 1])
                    else:
                        cx, cy = get_closest_center(u_pos)[0]
                        unit_actions.append(route_towards(u_pos, (cx, cy)))
            elif action == "PLACE_COW":
                if u_inv.get("COW", 0) > 0:
                    if tuple(u_pos) == t_pos:
                        unit_actions.append(["PLACE", "COW"])
                    else:
                        unit_actions.append(route_towards(u_pos, t_pos))
                else:
                    if tuple(u_pos) in CENTER_TILES:
                        unit_actions.append(["PICKUP", "COW", 1])
                    else:
                        cx, cy = get_closest_center(u_pos)[0]
                        unit_actions.append(route_towards(u_pos, (cx, cy)))
            elif action == "DROP_INVENTORY":
                if tuple(u_pos) in CENTER_TILES:
                    unit_actions.append(["DROP"])
                else:
                    cx, cy = get_closest_center(u_pos)[0]
                    unit_actions.append(route_towards(u_pos, (cx, cy)))
            else:
                if tuple(u_pos) == t_pos:
                    if action == "WATER":
                        unit_actions.append(["WATER"])
                    elif action == "HARVEST":
                        unit_actions.append(["HARVEST"])
                    elif action == "COLLECT_FERTILIZER":
                        unit_actions.append(["COLLECT_FERTILIZER"])
                    elif action == "DIG":
                        unit_actions.append(["DIG"])
                    elif action == "CARE":
                        unit_actions.append(["CARE"])
                    elif action == "BUILD_COOP":
                        unit_actions.append(["BUILD_COOP"])
                    elif action == "BUILD_PASTURE":
                        unit_actions.append(["BUILD_PASTURE"])
                    elif action.startswith("PLANT_"):
                        crop = action.split("_")[1]
                        unit_actions.append(["PLANT", crop])
                else:
                    unit_actions.append(route_towards(u_pos, t_pos))

    farmer_act = unit_actions[0] if num_units > 0 else ["PASS"]
    hands_acts = unit_actions[1:] if num_units > 1 else []
    
    # 5. Market orders planning
    market_orders = []
    
    # Continuous Emergency Feed / Starvation Protection (any turn)
    unfed_animals_count = sum(
        1 for row in tiles for tile in row
        if isinstance(tile, dict) and tile.get("kind") in ("COOP", "PASTURE")
        and tile.get("animal") is not None and not tile.get("fed_today", False)
    )
    if unfed_animals_count > 0:
        total_wheat_owned = private["shed"].get("WHEAT", 0) + sum(inv.get("WHEAT", 0) for inv in unit_inventories)
        wheat_deficit = unfed_animals_count - total_wheat_owned
        if wheat_deficit > 0:
            wheat_cost = market_prices.get("WHEAT", 25.0)
            max_affordable = int((money - current_safety_buffer) // wheat_cost)
            buy_qty = min(wheat_deficit, max_affordable)
            if buy_qty > 0:
                market_orders.append(["BUY_PRODUCT", "WHEAT", buy_qty])
                money -= buy_qty * wheat_cost
    
    # Sell inventory matching price-threshold and anti-glut logic
    wheat_to_keep = 10 if has_animals else 0
    shed_count = sum(private["shed"].values())
    
    # Fertilizer Arbitrage: Keep a small reserve for Strawberries/Tomatoes, sell the excess
    active_strawberry_count = crop_counts.get("STRAWBERRY", 0)
    active_tomato_count = crop_counts.get("TOMATO", 0)
    fertilizer_to_keep = (active_strawberry_count + active_tomato_count) * 2
    
    for item, count in private["shed"].items():
        if count > 0:
            if day == 29:
                # Sell absolutely everything on the final day!
                market_orders.append(["SELL", item, count])
            else:
                price = market_prices.get(item, BASE_PRICES.get(item, 1.0))
                base = BASE_PRICES.get(item, 1.0)
                
                # Default selling rule (crops)
                if item != "FERTILIZER":
                    if price >= 0.5 * base or shed_count >= 80 or day >= 27:
                        if item == "WHEAT":
                            sell_qty = max(0, count - wheat_to_keep)
                            if sell_qty > 0:
                                market_orders.append(["SELL", "WHEAT", sell_qty])
                        elif item in BASE_PRICES:
                            market_orders.append(["SELL", item, count])
                else:
                    # Dynamic Fertilizer selling rule: only sell if price is high (>= $80) to maximize yield value, 
                    # or we are at the end, or the shed is full.
                    if price >= 80.0 or day >= 27 or shed_count >= 80:
                        sell_qty = max(0, count - fertilizer_to_keep)
                        if sell_qty > 0:
                            market_orders.append(["SELL", "FERTILIZER", sell_qty])
                
    # Restrict all BUY and HIRE orders to Hour 0, and not on Day 29
    if hour == 0 and day < 29:
        # Land Expansion: only buy land if density is >= 70% and we have money
        n_unlocked_extra = n_unlocked_quads - 1
        if n_unlocked_extra < len(LAND_ORDER) and day < 20:
            land_cost = LAND_PRICES[n_unlocked_extra]
            buy_threshold = LAND_BUY_THRESHOLDS[n_unlocked_extra]
            total_unlocked_tiles = n_unlocked_quads * 25
            density = active_crops_count / total_unlocked_tiles
            if money >= buy_threshold and density >= 0.70:
                market_orders.append(["BUY_LAND"])
                money -= land_cost
                n_unlocked_quads += 1
                
        # Fertilizer purchasing: buy fertilizer if we have Strawberry/Tomato crops that need it
        fertilize_needed = sum(
            1 for row in tiles for tile in row
            if isinstance(tile, dict) and tile.get("kind") == "PLANT"
            and tile["crop"] in ("STRAWBERRY", "TOMATO")
            and tile.get("fertilized_until_day", -1) < day
            and (day - tile["planted_day"]) < CROPS[tile["crop"]]["max_yield_day"] - 2
        )
        fertilizer_owned = private["shed"].get("FERTILIZER", 0) + sum(inv.get("FERTILIZER", 0) for inv in unit_inventories)
        fertilizer_needed = max(0, fertilize_needed - fertilizer_owned)
        if fertilizer_needed > 0:
            fertilizer_cost = market_prices.get("FERTILIZER", 100.0)
            max_affordable = int((money - current_safety_buffer) // fertilizer_cost)
            buy_qty = min(fertilizer_needed, max_affordable)
            if buy_qty > 0:
                market_orders.append(["BUY_PRODUCT", "FERTILIZER", buy_qty])
                money -= buy_qty * fertilizer_cost

        # Buy animals (Goose/Cow) if we have empty structures and money (incorporating feed safety buffers)
        coops_list = []
        pastures_list = []
        for y in range(10):
            for x in range(10):
                tile = tiles[y][x]
                if isinstance(tile, dict):
                    if tile.get("kind") == "COOP":
                        coops_list.append(tile)
                    elif tile.get("kind") == "PASTURE":
                        pastures_list.append(tile)
                        
        empty_coops_count = sum(1 for tile in coops_list if tile.get("animal") is None)
        empty_pastures_count = sum(1 for tile in pastures_list if tile.get("animal") is None)
        
        geese_in_transit = private["shed"].get("GOOSE", 0) + sum(inv.get("GOOSE", 0) for inv in unit_inventories)
        cows_in_transit = private["shed"].get("COW", 0) + sum(inv.get("COW", 0) for inv in unit_inventories)
        
        geese_needed = max(0, empty_coops_count - geese_in_transit)
        cows_needed = max(0, empty_pastures_count - cows_in_transit)
        
        # Safe budget threshold: Goose costs 300, we want 400 total (100 feed buffer). Cow costs 400, we want 550 (150 feed buffer).
        if geese_needed > 0 and money - current_safety_buffer >= 400:
            buy_qty = min(geese_needed, int((money - current_safety_buffer) // 300))
            if buy_qty > 0:
                market_orders.append(["BUY_ANIMAL", "GOOSE", buy_qty])
                money -= buy_qty * 300
                geese_in_transit += buy_qty
                
        if cows_needed > 0 and money - current_safety_buffer >= 550:
            buy_qty = min(cows_needed, int((money - current_safety_buffer) // 400))
            if buy_qty > 0:
                market_orders.append(["BUY_ANIMAL", "COW", buy_qty])
                money -= buy_qty * 400
                cows_in_transit += buy_qty

        # Mathematical Linear Programming Solver for Crop Selection & Hiring
        # Town Demand Forecasting coefficients
        demand_weights = {crop: 1.0 for crop in CROPS}
        unlocked_shops = observation["town"].get("unlocked_shops", [])
        for shop in unlocked_shops:
            if shop == "BAKERY":
                demand_weights["WHEAT"] += 1.0
            elif shop == "PIZZA_SHOP":
                demand_weights["WHEAT"] += 1.0
                demand_weights["TOMATO"] += 1.0
            elif shop == "BRUNCH_SPOT":
                demand_weights["WHEAT"] += 1.0
                demand_weights["STRAWBERRY"] += 1.0
            elif shop == "ICE_CREAM_SHOP":
                demand_weights["WHEAT"] += 1.0
                demand_weights["STRAWBERRY"] += 1.0
            elif shop == "PET_CAFE":
                demand_weights["CARROT"] += 2.0
            elif shop == "SMOOTHIE_SHOP":
                demand_weights["STRAWBERRY"] += 1.0
            elif shop == "FARMERS_MARKET":
                demand_weights["WHEAT"] += 1.0
                demand_weights["CARROT"] += 1.0
                demand_weights["TOMATO"] += 1.0
                demand_weights["STRAWBERRY"] += 1.0

        # Define Optimization Bounds
        crop_names = ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON"]
        bounds = []
        total_unlocked_tiles = n_unlocked_quads * 25
        remaining_days = 28 - day
        
        # 10 Variables: 
        # x_0 to x_4: seeds to BUY today
        # s_0 to s_4: seeds to plant from STOCK today
        for crop in crop_names:
            crop_data = CROPS[crop]
            # Maturation deadline check
            if remaining_days < crop_data["max_yield_day"]:
                bounds.append((0.0, 0.0))  # x_c upper bound = 0
            else:
                bounds.append((0.0, None)) # x_c upper bound = infinity

        for crop in crop_names:
            crop_data = CROPS[crop]
            seeds_owned_c = float(private["seeds"].get(crop, 0))
            if remaining_days < crop_data["max_yield_day"]:
                bounds.append((0.0, 0.0))  # s_c upper bound = 0
            else:
                bounds.append((0.0, seeds_owned_c)) # s_c upper bound = seeds in stock

        # Formulate LP Objective function (maximizing expected net profit)
        c_coef = []
        P_vals = []
        for crop in crop_names:
            crop_data = CROPS[crop]
            live_price = market_prices.get(crop, crop_data["base_price"])
            
            # Tuned Optimal Price Decay Modeling (Divisor = 2500.0)
            market_inv = observation["market"]["inventory"].get(crop, 10000)
            est_price = live_price
            if crop in ("MELON", "STRAWBERRY"):
                est_price = max(1.0, live_price * (1.0 - (market_inv - 10000) / 2500.0))
                
            # Apply Town Demand Forecast Modifier
            est_price *= (1.0 + 0.1 * (demand_weights[crop] - 1.0))
            
            # Expected Yield (assume Tomatoes & Strawberries are fertilized, and adjust for remaining productions)
            if crop == "TOMATO":
                prod_ages = [8, 9, 10, 11]
                n_prods = sum(1 for age in prod_ages if day + age <= 28)
                exp_yield = float(n_prods * 2)
            elif crop == "STRAWBERRY":
                prod_ages = [10, 12, 14, 16]
                n_prods = sum(1 for age in prod_ages if day + age <= 28)
                exp_yield = float(n_prods * 2)
            else:
                exp_yield = float(crop_data["base_yield"])
                
            P_vals.append(exp_yield * est_price)

        # Objective is Minimizing: sum x_i * (seed_cost_i - P_i) + sum s_i * (-P_i)
        for i, crop in enumerate(crop_names):
            c_coef.append(CROPS[crop]["seed_cost"] - P_vals[i])
        for i in range(5):
            c_coef.append(-P_vals[i])
            
        # Formulate base inequalities: A_ub * X <= b_ub
        # Row 0: Seed Budget: sum x_i * seed_cost_i <= B_y
        # Row 1: Space bounds: sum (x_i + s_i) <= empty_tiles
        # Row 2: Labor bounds: sum (x_i + s_i) <= (y + 1) * cap_per_worker - active_crops_count
        # Row 3: New plantings limit: sum (x_i + s_i) <= (y + 1) * plant_limit_per_worker
        # Rows 4 to 8: Crop Diversity bounds: (x_j + s_j) <= max_allowed_j - active_crops_j
        A_ub = [
            [CROPS[c]["seed_cost"] for c in crop_names] + [0.0]*5, # Budget
            [1.0]*10, # Space
            [1.0]*10, # Labor
            [1.0]*10  # New plantings
        ]
        # Add diversity rows
        for j in range(5):
            row = [0.0]*10
            row[j] = 1.0      # x_j
            row[j + 5] = 1.0  # s_j
            A_ub.append(row)
        
        # Max hands we can support based on unlocked quadrants
        max_hands_limit = n_unlocked_quads + 1
        
        best_y = 0
        best_seeds = [0, 0, 0, 0, 0]
        best_profit = -float("inf")
        
        # Loop through all possible farm hand hiring options to find optimal scenarios
        for y in range(max_hands_limit + 1):
            # Feasibility check: must hire enough hands to cover active crops
            if (y + 1) * cap_per_worker < active_crops_count:
                continue
                
            C_y = 0.0
            hires_today = me.get("hires_today", 0)
            for i in range(y):
                C_y += get_fib(hires_today + i)
                
            B_y = money - current_safety_buffer - C_y
            if B_y < 0.0:
                continue
                
            # Right-hand side b_ub
            total_unlocked_tiles = n_unlocked_quads * 25
            b_ub = [
                B_y,
                max(0.0, float(len(empty_tiles))),
                max(0.0, float((y + 1) * cap_per_worker - active_crops_count)),
                max(0.0, float((y + 1) * plant_limit_per_worker))
            ]
            for j, crop in enumerate(crop_names):
                # Tuned Optimal Diversity Limit Cap (0.45 = 45%)
                max_allowed = max(3.0, total_unlocked_tiles * 0.45)
                b_ub.append(max(0.0, max_allowed - crop_counts[crop]))
            
            try:
                res = linprog(c_coef, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")
                if res.success:
                    x_opt = res.x[:5]
                    round_seeds = [math.floor(val + 1e-7) for val in x_opt]
                    
                    s_opt = res.x[5:]
                    round_s = [math.floor(val + 1e-7) for val in s_opt]
                    
                    # Compute actual integer profit for evaluation
                    actual_profit = sum(round_seeds[i] * (-c_coef[i]) for i in range(5)) + sum(round_s[i] * (-c_coef[i + 5]) for i in range(5)) - C_y
                    
                    if actual_profit > best_profit:
                        best_profit = actual_profit
                        best_y = y
                        best_seeds = round_seeds
            except Exception:
                continue
                
        # Queue the optimal market choices calculated by the LP solver
        if best_profit > -float("inf"):
            # Queue hires
            for _ in range(best_y):
                market_orders.append(["HIRE"])
            # Queue seed buys
            for i, crop in enumerate(crop_names):
                qty = best_seeds[i]
                if qty > 0:
                    market_orders.append(["BUY_SEED", crop, qty])
                    
    market_orders = market_orders[:10]
    
    return {
        "farmer": farmer_act,
        "hands": hands_acts,
        "market": market_orders
    }
