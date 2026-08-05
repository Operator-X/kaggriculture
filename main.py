import math

# Constants
SAFETY_BUFFER = 200.0
LAND_PRICES = [1000.0, 2000.0, 4000.0]
LAND_ORDER = ["NE", "SW", "SE"]
# High money thresholds before we buy land to ensure we have a working capital surplus
LAND_BUY_THRESHOLDS = [2000.0, 3500.0, 6000.0]

CROPS = {
    "WHEAT": {"seed_cost": 10, "max_yield_day": 4, "first_yield_day": 2, "ongoing": False},
    "CARROT": {"seed_cost": 20, "max_yield_day": 3, "first_yield_day": 2, "ongoing": False},
    "TOMATO": {"seed_cost": 50, "max_yield_day": 11, "first_yield_day": 8, "ongoing": True},
    "STRAWBERRY": {"seed_cost": 100, "max_yield_day": 16, "first_yield_day": 10, "ongoing": True},
    "MELON": {"seed_cost": 80, "max_yield_day": 10, "first_yield_day": 10, "ongoing": False},
}

# Center / shed-adjacent tiles
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
    
    # 1. Gather all units and their inventories
    farmer_pos = me["farmer"]
    hands_pos = me["hands"]
    unit_positions = [farmer_pos] + list(hands_pos)
    unit_inventories = private["inventories"]
    num_units = len(unit_positions)
    
    # Ensure unit_inventories has enough slots
    while len(unit_inventories) < num_units:
        unit_inventories.append({})
        
    # Count active crops and seeds owned
    active_crops_count = sum(
        1 for row in tiles for tile in row
        if isinstance(tile, dict) and tile.get("kind") == "PLANT"
    )
    seeds_owned = sum(private["seeds"].values())
    
    # Dynamic safety buffer: if we have no crops and no seeds, lower the buffer to bootstrap
    if active_crops_count == 0 and seeds_owned == 0:
        current_safety_buffer = 20.0
    else:
        current_safety_buffer = SAFETY_BUFFER
        
    # Labor capacity limit: 12 plants per unit (farmer/hand) to ensure they can be watered
    max_plants_supported = num_units * 12
    
    # 2. Identify and rank active tasks on the farm
    tasks = []
    seeds_avail = dict(private["seeds"])
    new_plant_tasks_count = 0
    
    for y in range(10):
        for x in range(10):
            tile = tiles[y][x]
            if tile == "LOCKED":
                continue
            
            if tile is None:
                # Avoid planting late in the day (hour 23) because they turn into weeds overnight
                # Also stay within labor capacity limits to prevent crops dying from lack of watering
                if hour < 23 and (active_crops_count + new_plant_tasks_count < max_plants_supported):
                    # Check which seeds we actually have in stock and choose the most profitable one
                    available_crops = [crop for crop, count in seeds_avail.items() if count > 0]
                    if available_crops:
                        best_crop = None
                        best_profit = -float("inf")
                        for crop in available_crops:
                            if crop == "WHEAT":
                                profit = 4 * market_prices.get("WHEAT", 25) - 10
                            elif crop == "CARROT":
                                profit = 3 * market_prices.get("CARROT", 35) - 20
                            else:
                                profit = 0
                            if profit > best_profit:
                                best_profit = profit
                                best_crop = crop
                        
                        if best_crop:
                            tasks.append({
                                "pos": (x, y),
                                "action": f"PLANT_{best_crop}",
                                "priority": 40
                            })
                            seeds_avail[best_crop] -= 1
                            new_plant_tasks_count += 1
            elif isinstance(tile, dict):
                kind = tile.get("kind")
                if kind == "PLANT":
                    crop = tile["crop"]
                    crop_data = CROPS[crop]
                    age = day - tile["planted_day"]
                    
                    # Emergency watering (Priority 10)
                    if not tile["watered_today"]:
                        tasks.append({
                            "pos": (x, y),
                            "action": "WATER",
                            "priority": 10
                        })
                    
                    # Harvesting (Priority 20)
                    is_mature = False
                    if not crop_data["ongoing"]:
                        is_mature = age >= crop_data["max_yield_day"] or day == 29
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
                    if animal is not None:
                        # Feed animal (Priority 10)
                        if not tile["fed_today"]:
                            tasks.append({
                                "pos": (x, y),
                                "action": "FEED",
                                "priority": 10
                            })
                        
                        # Harvest animal produce (Priority 20)
                        if tile.get("yield_units", 0) > 0:
                            tasks.append({
                                "pos": (x, y),
                                "action": "HARVEST",
                                "priority": 20
                            })
                            
                        # Collect fertilizer (Priority 25)
                        if tile.get("fertilizer_available", False):
                            tasks.append({
                                "pos": (x, y),
                                "action": "COLLECT_FERTILIZER",
                                "priority": 25
                            })
                elif kind == "WEED":
                    # Clear weed (Priority 30)
                    tasks.append({
                        "pos": (x, y),
                        "action": "DIG",
                        "priority": 30
                    })

    # Sort tasks: highest priority first (lower value of priority)
    tasks.sort(key=lambda t: t["priority"])
    
    # 3. Greedy unit task assignment
    unit_assignments = [None] * num_units
    assigned_task_positions = set()
    
    for task in tasks:
        task_pos = task["pos"]
        task_action = task["action"]
        
        if task_pos in assigned_task_positions:
            continue
            
        best_unit_idx = -1
        best_dist = float("inf")
        
        for u_idx in range(num_units):
            if unit_assignments[u_idx] is not None:
                continue
                
            u_pos = unit_positions[u_idx]
            u_inv = unit_inventories[u_idx]
            
            if task_action == "FEED":
                has_wheat = u_inv.get("WHEAT", 0) > 0
                shed_has_wheat = private["shed"].get("WHEAT", 0) > 0
                if not (has_wheat or shed_has_wheat):
                    continue
                
                if has_wheat:
                    dist = get_distance(u_pos, task_pos)
                else:
                    _, dist_to_shed = get_closest_center(u_pos)
                    _, dist_shed_to_task = get_closest_center(task_pos)
                    dist = dist_to_shed + dist_shed_to_task
            else:
                dist = get_distance(u_pos, task_pos)
                
            if dist < best_dist:
                best_dist = dist
                best_unit_idx = u_idx
                
        if best_unit_idx != -1:
            unit_assignments[best_unit_idx] = task
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
                    elif action.startswith("PLANT_"):
                        crop = action.split("_")[1]
                        unit_actions.append(["PLANT", crop])
                else:
                    unit_actions.append(route_towards(u_pos, t_pos))

    farmer_act = unit_actions[0] if num_units > 0 else ["PASS"]
    hands_acts = unit_actions[1:] if num_units > 1 else []
    
    # 5. Market orders planning
    market_orders = []
    
    # Sell non-wheat inventory
    has_animals = any(
        isinstance(tile, dict) and tile.get("kind") in ("COOP", "PASTURE") and tile.get("animal") is not None
        for row in tiles for tile in row
    )
    wheat_to_keep = 10 if has_animals else 0
    
    for item, count in private["shed"].items():
        if count > 0:
            if item == "WHEAT":
                sell_qty = max(0, count - wheat_to_keep)
                if sell_qty > 0:
                    market_orders.append(["SELL", "WHEAT", sell_qty])
            elif item in ("CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER"):
                market_orders.append(["SELL", item, count])
                
    # Restrict all BUY and HIRE orders to Hour 0
    if hour == 0:
        # Land Expansion: only buy land if we have a very large cash surplus
        n_unlocked_quads = len(me["unlocked_quadrants"])
        n_unlocked_extra = n_unlocked_quads - 1
        if n_unlocked_extra < len(LAND_ORDER):
            land_cost = LAND_PRICES[n_unlocked_extra]
            buy_threshold = LAND_BUY_THRESHOLDS[n_unlocked_extra]
            if money >= buy_threshold:
                market_orders.append(["BUY_LAND"])
                money -= land_cost
                n_unlocked_quads += 1
                
        # Labor Scaling prediction: cap max hands based on unlocked land size to prevent overspending
        # NW: max 2 hands. NE: max 3 hands. SW: max 4 hands. SE: max 5 hands.
        max_hands_limit = n_unlocked_quads + 1
        
        num_jobs = active_crops_count + seeds_owned
        predicted_hands = 0
        if num_jobs > 0:
            target_hands = min(max_hands_limit, max(1, num_jobs // 5))
            hires_today = me.get("hires_today", 0)
            
            temp_money = money
            h = hires_today
            while h < target_hands:
                cost = get_fib(h)
                if temp_money - cost >= current_safety_buffer:
                    market_orders.append(["HIRE"])
                    temp_money -= cost
                    h += 1
                    predicted_hands += 1
                else:
                    break
            money = temp_money
                    
        # Feed purchasing safety
        unfed_animals_count = sum(
            1 for row in tiles for tile in row
            if isinstance(tile, dict) and tile.get("kind") in ("COOP", "PASTURE")
            and tile.get("animal") is not None and not tile.get("fed_today", False)
        )
        if unfed_animals_count > 0:
            total_wheat_owned = private["shed"].get("WHEAT", 0) + sum(inv.get("WHEAT", 0) for inv in unit_inventories)
            wheat_deficit = unfed_animals_count - total_wheat_owned
            if wheat_deficit > 0:
                wheat_cost = market_prices.get("WHEAT", 25)
                max_affordable = int((money - current_safety_buffer) // wheat_cost)
                buy_qty = min(wheat_deficit, max_affordable)
                if buy_qty > 0:
                    market_orders.append(["BUY_PRODUCT", "WHEAT", buy_qty])
                    money -= buy_qty * wheat_cost

        # Seed purchasing (predicted_hands + num_units represents the capacity we will have today)
        empty_tiles = sum(1 for row in tiles for tile in row if tile is None)
        predicted_max_supported = (predicted_hands + num_units) * 12
        additional_seeds_needed = max(0, predicted_max_supported - (active_crops_count + seeds_owned))
        seeds_needed = min(empty_tiles - seeds_owned, additional_seeds_needed)
        
        if seeds_needed > 0:
            wheat_profit = 4 * market_prices.get("WHEAT", 25) - 10
            carrot_profit = 3 * market_prices.get("CARROT", 35) - 20
            chosen_crop = "WHEAT" if wheat_profit >= carrot_profit else "CARROT"
            seed_cost = CROPS[chosen_crop]["seed_cost"]
            
            max_affordable = int((money - current_safety_buffer) // seed_cost)
            buy_qty = min(seeds_needed, max_affordable)
            if buy_qty > 0:
                market_orders.append(["BUY_SEED", chosen_crop, buy_qty])
                money -= buy_qty * seed_cost
            
    market_orders = market_orders[:10]
    
    return {
        "farmer": farmer_act,
        "hands": hands_acts,
        "market": market_orders
    }
