# Optimized Ben Hamilton Strategy Bot - Version 2
# Incorporates dynamic price hoarding, fertilizer capping, and Day 18 Melon buys.

CENTER_TILES = [(4, 4), (5, 4), (4, 5), (5, 5)]

# Exact HIRE, BUY_SEED, BUY_ANIMAL, BUY_LAND schedule from top player replays
MARKET_SCHEDULE = {
    0: [
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'BUY_ANIMAL', 'SHEEP', 2),
        (1, 'BUY_ANIMAL', 'COW', 2),
        (1, 'BUY_SEED', 'WHEAT', 7),
        (1, 'BUY_SEED', 'MELON', 12),
    ],
    2: [
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
    ],
    3: [
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'BUY_ANIMAL', 'COW', 1),
    ],
    4: [
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'BUY_SEED', 'WHEAT', 7),
    ],
    5: [
        (1, 'HIRE'),
        (1, 'BUY_ANIMAL', 'COW', 1),
    ],
    6: [
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
    ],
    7: [
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'BUY_LAND'),
        (1, 'BUY_ANIMAL', 'SHEEP', 2),
        (1, 'BUY_ANIMAL', 'COW', 2),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'BUY_SEED', 'STRAWBERRY', 9),
    ],
    8: [
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'BUY_SEED', 'WHEAT', 7),
        (1, 'BUY_SEED', 'STRAWBERRY', 4),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
    ],
    9: [
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'BUY_ANIMAL', 'COW', 2),
        (1, 'BUY_SEED', 'STRAWBERRY', 6),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
    ],
    10: [
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
    ],
    11: [
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'BUY_LAND'),
        (1, 'BUY_ANIMAL', 'SHEEP', 2),
        (1, 'BUY_SEED', 'MELON', 12),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'BUY_SEED', 'STRAWBERRY', 23),
        (3, 'HIRE'),
        (3, 'HIRE'),
        (3, 'HIRE'),
        (3, 'HIRE'),
    ],
    12: [
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'BUY_SEED', 'WHEAT', 7),
        (2, 'HIRE'),
        (2, 'HIRE'),
    ],
    13: [
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
    ],
    14: [
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
    ],
    15: [
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (3, 'HIRE'),
        (3, 'HIRE'),
    ],
    16: [
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'BUY_SEED', 'WHEAT', 7),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
    ],
    17: [
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (3, 'HIRE'),
    ],
    18: [
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'BUY_SEED', 'MELON', 6),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (3, 'HIRE'),
        (3, 'HIRE'),
    ],
    19: [
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (3, 'HIRE'),
        (3, 'HIRE'),
    ],
    20: [
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'BUY_SEED', 'WHEAT', 7),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (3, 'HIRE'),
        (3, 'HIRE'),
        (3, 'HIRE'),
        (3, 'HIRE'),
    ],
    21: [
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (3, 'HIRE'),
        (3, 'HIRE'),
        (3, 'HIRE'),
    ],
    22: [
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'BUY_SEED', 'WHEAT', 8),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (3, 'HIRE'),
        (3, 'HIRE'),
        (3, 'HIRE'),
        (3, 'HIRE'),
    ],
    23: [
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'BUY_SEED', 'WHEAT', 4),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (3, 'HIRE'),
        (3, 'HIRE'),
        (3, 'HIRE'),
    ],
    24: [
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'BUY_SEED', 'WHEAT', 11),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (3, 'HIRE'),
        (3, 'HIRE'),
        (3, 'HIRE'),
        (3, 'HIRE'),
    ],
    25: [
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'BUY_SEED', 'WHEAT', 8),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (3, 'HIRE'),
        (3, 'HIRE'),
        (3, 'HIRE'),
    ],
    26: [
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'BUY_SEED', 'WHEAT', 15),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (3, 'HIRE'),
        (3, 'HIRE'),
        (3, 'HIRE'),
        (3, 'HIRE'),
    ],
    27: [
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'BUY_SEED', 'WHEAT', 4),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (3, 'HIRE'),
        (3, 'HIRE'),
    ],
    28: [
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (2, 'HIRE'),
        (3, 'HIRE'),
        (3, 'HIRE'),
        (3, 'HIRE'),
    ],
    29: [
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (1, 'HIRE'),
        (2, 'HIRE'),
    ],
}

def get_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def get_closest_center(pos):
    best_dist = float("inf")
    best_tile = CENTER_TILES[0]
    for cx, cy in CENTER_TILES:
        dist = get_distance(pos, (cx, cy))
        if dist < best_dist:
            best_dist = dist
            best_tile = (cx, cy)
    return best_tile, best_dist

def route_towards(current, target):
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
    tiles = me["tiles"]
    money = me["money"]
    market_prices = observation["market"]["prices"]
    
    farmer_pos = me["farmer"]
    hands_pos = me["hands"]
    unit_positions = [farmer_pos] + list(hands_pos)
    unit_inventories = private["inventories"]
    num_units = len(unit_positions)
    
    while len(unit_inventories) < num_units:
        unit_inventories.append({})
        
    cows_owned = sum(1 for row in tiles for tile in row if isinstance(tile, dict) and tile.get("kind") == "PASTURE" and tile.get("animal") == "COW")
    cows_transit = private["shed"].get("COW", 0) + sum(inv.get("COW", 0) for inv in unit_inventories)
    sheep_owned = sum(1 for row in tiles for tile in row if isinstance(tile, dict) and tile.get("kind") == "PASTURE" and tile.get("animal") == "SHEEP")
    sheep_transit = private["shed"].get("SHEEP", 0) + sum(inv.get("SHEEP", 0) for inv in unit_inventories)
    
    total_animals = cows_owned + cows_transit + sheep_owned + sheep_transit
    pasture_count = sum(1 for row in tiles for tile in row if isinstance(tile, dict) and tile.get("kind") == "PASTURE")
    
    tasks = []
    
    empty_tiles = []
    for y in range(10):
        for x in range(10):
            tile = tiles[y][x]
            if tile is None:
                empty_tiles.append((x, y))
                
    empty_tiles.sort(key=lambda p: get_distance(p, (4, 4)))
    
    pasture_needed = total_animals - pasture_count
    if pasture_needed > 0:
        for x, y in empty_tiles:
            tasks.append({"pos": (x, y), "action": "BUILD_PASTURE", "priority": 15})
            pasture_count += 1
            pasture_needed -= 1
            empty_tiles.remove((x, y))
            if pasture_needed == 0:
                break
                
    if hour < 18:
        strawberry_seeds = private["seeds"].get("STRAWBERRY", 0)
        melon_seeds = private["seeds"].get("MELON", 0)
        wheat_seeds = private["seeds"].get("WHEAT", 0)
        
        for x, y in empty_tiles:
            if strawberry_seeds > 0:
                tasks.append({"pos": (x, y), "action": "PLANT", "crop": "STRAWBERRY", "priority": 50})
                strawberry_seeds -= 1
            elif melon_seeds > 0:
                tasks.append({"pos": (x, y), "action": "PLANT", "crop": "MELON", "priority": 50})
                melon_seeds -= 1
            elif wheat_seeds > 0:
                tasks.append({"pos": (x, y), "action": "PLANT", "crop": "WHEAT", "priority": 50})
                wheat_seeds -= 1
                
    for y in range(10):
        for x in range(10):
            tile = tiles[y][x]
            if tile == "LOCKED" or tile is None:
                continue
                
            if isinstance(tile, dict):
                kind = tile.get("kind")
                if kind == "PLANT":
                    crop = tile["crop"]
                    age = day - tile["planted_day"]
                    
                    if not tile.get("watered_today", False):
                        consec = tile.get("consecutive_unwatered", 0)
                        priority = 5 if consec >= 1 else 30
                        tasks.append({"pos": (x, y), "action": "WATER", "priority": priority})
                        
                    if (crop == "STRAWBERRY" and age in (9, 11, 13, 15)
                            and tile.get("fertilized_until_day", -1) < day):
                        fert_available = private["shed"].get("FERTILIZER", 0) + sum(inv.get("FERTILIZER", 0) for inv in unit_inventories)
                        if fert_available > 0:
                            tasks.append({"pos": (x, y), "action": "FERTILIZE", "priority": 15})
                            
                    mature = False
                    if crop == "MELON":
                        mature = age >= 10 or day == 28
                    elif crop == "WHEAT":
                        mature = age >= 4 or day == 28
                    else:
                        mature = tile.get("yield_units", 0) > 0
                        
                    if mature and tile.get("yield_units", 0) > 0:
                        tasks.append({"pos": (x, y), "action": "HARVEST", "priority": 20})
                        
                elif kind == "PASTURE":
                    animal = tile.get("animal")
                    if animal is None:
                        cows_avail = private["shed"].get("COW", 0) + sum(inv.get("COW", 0) for inv in unit_inventories)
                        sheep_avail = private["shed"].get("SHEEP", 0) + sum(inv.get("SHEEP", 0) for inv in unit_inventories)
                        if cows_avail > 0:
                            tasks.append({"pos": (x, y), "action": "PLACE_COW", "priority": 40})
                        elif sheep_avail > 0:
                            tasks.append({"pos": (x, y), "action": "PLACE_SHEEP", "priority": 40})
                    else:
                        if not tile.get("fed_today", False):
                            consec = tile.get("consecutive_unfed", 0)
                            priority = 5 if consec >= 1 else 10
                            tasks.append({"pos": (x, y), "action": "FEED", "priority": priority})
                        if not tile.get("cared_today", False):
                            tasks.append({"pos": (x, y), "action": "CARE", "priority": 12})
                        if tile.get("yield_units", 0) > 0:
                            tasks.append({"pos": (x, y), "action": "HARVEST", "priority": 20})
                        if tile.get("fertilizer_available", False):
                            fert_price = market_prices.get("FERTILIZER", 100.0)
                            active_strawberry_count = sum(
                                1 for row in tiles for t in row
                                if isinstance(t, dict) and t.get("kind") == "PLANT" and t.get("crop") == "STRAWBERRY"
                            )
                            fertilizer_to_keep = active_strawberry_count * 2
                            fert_owned = private["shed"].get("FERTILIZER", 0) + sum(inv.get("FERTILIZER", 0) for inv in unit_inventories)
                            if fert_price >= 40.0 or fert_owned < fertilizer_to_keep:
                                tasks.append({"pos": (x, y), "action": "COLLECT_FERTILIZER", "priority": 25})
                            
                elif kind == "WEED":
                    tasks.append({"pos": (x, y), "action": "DIG", "priority": 60})
                    
    for u_idx in range(num_units):
        u_pos = unit_positions[u_idx]
        u_inv = unit_inventories[u_idx]
        if day == 29:
            inv_size = sum(u_inv.values())
        else:
            inv_size = sum(u_inv.get(item, 0) for item in u_inv if item not in ("WHEAT", "FERTILIZER", "COW", "SHEEP"))
            
        if (day == 29 and inv_size > 0) or (inv_size >= 8):
            cx, cy = get_closest_center(u_pos)[0]
            tasks.append({
                "pos": (cx, cy),
                "action": "DROP_INVENTORY",
                "priority": 35
            })
            
    tasks.sort(key=lambda t: t["priority"])
    
    unit_assignments = [None] * num_units
    assigned_positions = set()
    
    for task in tasks:
        t_pos = task["pos"]
        act = task["action"]
        
        if act != "DROP_INVENTORY" and t_pos in assigned_positions:
            continue
            
        best_unit_idx = -1
        best_dist = float("inf")
        
        for u_idx in range(num_units):
            if unit_assignments[u_idx] is not None:
                continue
                
            u_pos = unit_positions[u_idx]
            u_inv = unit_inventories[u_idx]
            
            if act == "FEED":
                if u_inv.get("WHEAT", 0) == 0 and private["shed"].get("WHEAT", 0) == 0:
                    continue
            elif act == "FERTILIZE":
                if u_inv.get("FERTILIZER", 0) == 0 and private["shed"].get("FERTILIZER", 0) == 0:
                    continue
            elif act == "PLACE_COW":
                if u_inv.get("COW", 0) == 0 and private["shed"].get("COW", 0) == 0:
                    continue
            elif act == "PLACE_SHEEP":
                if u_inv.get("SHEEP", 0) == 0 and private["shed"].get("SHEEP", 0) == 0:
                    continue
                    
            dist = get_distance(u_pos, t_pos)
            if dist < best_dist:
                best_dist = dist
                best_unit_idx = u_idx
                
        if best_unit_idx != -1:
            unit_assignments[best_unit_idx] = task
            if act != "DROP_INVENTORY":
                assigned_positions.add(t_pos)
                
    unit_actions = []
    for u_idx in range(num_units):
        u_pos = unit_positions[u_idx]
        u_inv = unit_inventories[u_idx]
        task = unit_assignments[u_idx]
        
        if task is None:
            if tuple(u_pos) in CENTER_TILES:
                unit_actions.append(["PASS"])
            else:
                cx, cy = get_closest_center(u_pos)[0]
                unit_actions.append(route_towards(u_pos, (cx, cy)))
        else:
            t_pos = task["pos"]
            act = task["action"]
            
            if act == "FEED" and u_inv.get("WHEAT", 0) == 0:
                if tuple(u_pos) in CENTER_TILES:
                    needed = sum(1 for t in tasks if t["action"] == "FEED")
                    qty = min(needed, private["shed"].get("WHEAT", 0))
                    unit_actions.append(["PICKUP", "WHEAT", max(1, qty)])
                else:
                    cx, cy = get_closest_center(u_pos)[0]
                    unit_actions.append(route_towards(u_pos, (cx, cy)))
            elif act == "FERTILIZE" and u_inv.get("FERTILIZER", 0) == 0:
                if tuple(u_pos) in CENTER_TILES:
                    needed = sum(1 for t in tasks if t["action"] == "FERTILIZE")
                    qty = min(needed, private["shed"].get("FERTILIZER", 0))
                    unit_actions.append(["PICKUP", "FERTILIZER", max(1, qty)])
                else:
                    cx, cy = get_closest_center(u_pos)[0]
                    unit_actions.append(route_towards(u_pos, (cx, cy)))
            elif act == "PLACE_COW" and u_inv.get("COW", 0) == 0:
                if tuple(u_pos) in CENTER_TILES:
                    needed = sum(1 for t in tasks if t["action"] == "PLACE_COW")
                    qty = min(needed, private["shed"].get("COW", 0))
                    unit_actions.append(["PICKUP", "COW", max(1, qty)])
                else:
                    cx, cy = get_closest_center(u_pos)[0]
                    unit_actions.append(route_towards(u_pos, (cx, cy)))
            elif act == "PLACE_SHEEP" and u_inv.get("SHEEP", 0) == 0:
                if tuple(u_pos) in CENTER_TILES:
                    needed = sum(1 for t in tasks if t["action"] == "PLACE_SHEEP")
                    qty = min(needed, private["shed"].get("SHEEP", 0))
                    unit_actions.append(["PICKUP", "SHEEP", max(1, qty)])
                else:
                    cx, cy = get_closest_center(u_pos)[0]
                    unit_actions.append(route_towards(u_pos, (cx, cy)))
            elif act == "DROP_INVENTORY":
                if tuple(u_pos) in CENTER_TILES:
                    unit_actions.append(["DROP"])
                else:
                    cx, cy = get_closest_center(u_pos)[0]
                    unit_actions.append(route_towards(u_pos, (cx, cy)))
            else:
                if tuple(u_pos) == t_pos:
                    if act in ("WATER", "FEED", "CARE", "HARVEST", "COLLECT_FERTILIZER", "DIG", "BUILD_PASTURE"):
                        unit_actions.append([act])
                    elif act == "FERTILIZE":
                        unit_actions.append(["FERTILIZE"])
                    elif act == "PLACE_COW":
                        unit_actions.append(["PLACE", "COW"])
                    elif act == "PLACE_SHEEP":
                        unit_actions.append(["PLACE", "SHEEP"])
                    elif act == "PLANT":
                        unit_actions.append(["PLANT", task["crop"]])
                else:
                    unit_actions.append(route_towards(u_pos, t_pos))
                    
    market_orders = []
    
    today_schedule = MARKET_SCHEDULE.get(day, [])
    for h, cmd, *args in today_schedule:
        if h == hour:
            if cmd == "HIRE":
                market_orders.append(["HIRE"])
            elif cmd == "BUY_LAND":
                market_orders.append(["BUY_LAND"])
            elif cmd == "BUY_ANIMAL":
                market_orders.append(["BUY_ANIMAL", args[0], args[1]])
            elif cmd == "BUY_SEED":
                if day in (26, 27) and args[0] == "WHEAT":
                    continue
                market_orders.append(["BUY_SEED", args[0], args[1]])
                
    active_animals_count = sum(
        1 for row in tiles for tile in row
        if isinstance(tile, dict) and tile.get("kind") == "PASTURE" and tile.get("animal") is not None
    )
    if active_animals_count > 0:
        total_wheat_owned = private["shed"].get("WHEAT", 0) + sum(inv.get("WHEAT", 0) for inv in unit_inventories)
        target_stock = active_animals_count * 2
        trigger_threshold = active_animals_count + 2
        if total_wheat_owned < trigger_threshold:
            wheat_cost = market_prices.get("WHEAT", 25.0)
            qty_needed = target_stock - total_wheat_owned
            max_affordable = int(money // wheat_cost)
            buy_qty = min(qty_needed, max_affordable)
            if buy_qty > 0:
                market_orders.append(["BUY_PRODUCT", "WHEAT", buy_qty])
                money -= buy_qty * wheat_cost
                
    active_strawberry_count = sum(
        1 for row in tiles for t in row
        if isinstance(t, dict) and t.get("kind") == "PLANT" and t.get("crop") == "STRAWBERRY"
    )
    fertilizer_to_keep = active_strawberry_count * 2
    wheat_to_keep = active_animals_count * 3
    
    shed_count = sum(private["shed"].values())
    
    THRESHOLDS = {
        "MILK": 160.0,
        "WOOL": 200.0,
        "STRAWBERRY": 120.0,
        "MELON": 200.0,
        "EGG": 50.0,
        "FERTILIZER": 80.0
    }
    
    for item, count in private["shed"].items():
        if count > 0:
            if item == "WHEAT":
                sell_qty = max(0, count - wheat_to_keep)
                if sell_qty > 0:
                    market_orders.append(["SELL", "WHEAT", sell_qty])
            else:
                price = market_prices.get(item, 1.0)
                threshold = THRESHOLDS.get(item, 0.0)
                if day == 29 or shed_count >= 80 or price >= threshold:
                    if item == "FERTILIZER":
                        sell_qty = max(0, count - fertilizer_to_keep)
                        if sell_qty > 0:
                            market_orders.append(["SELL", "FERTILIZER", sell_qty])
                    elif item in THRESHOLDS:
                        market_orders.append(["SELL", item, count])
                
    return {
        "farmer": unit_actions[0] if num_units > 0 else ["PASS"],
        "hands": unit_actions[1:] if num_units > 1 else [],
        "market": market_orders[:10]
    }
