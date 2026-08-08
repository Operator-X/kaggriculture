# venks_killer.py
# Hybrid Kaggriculture Agent: Plays a dynamic, general-purpose strategy against arbitrary opponents,
# but automatically detects and plays a premium front-running sabotage strategy against the static venks agent.

import json
import zlib
import base64

VENKS_ACTIONS_DATA = "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"

EARLY_ACTIONS = {int(k): v for k, v in json.loads(zlib.decompress(base64.b64decode(VENKS_ACTIONS_DATA.strip().encode('utf-8'))).decode('utf-8')).items()}

# Sell steps mapped to premium products only to prevent resource starvation (Wheat/Fertilizer).
VENKS_SELL_STEPS = {
    # Melon
    257: ["MELON"], 259: ["MELON"], 260: ["MELON"], 262: ["MELON"], 265: ["MELON"],
    499: ["MELON"], 504: ["MELON"], 505: ["MELON"], 529: ["MELON", "STRAWBERRY", "MILK"],
    
    # Strawberry
    425: ["STRAWBERRY"], 431: ["STRAWBERRY"], 433: ["STRAWBERRY", "MILK", "WOOL"],
    457: ["STRAWBERRY", "MILK"], 471: ["STRAWBERRY"],
    481: ["STRAWBERRY", "MILK"], 519: ["STRAWBERRY"], 528: ["STRAWBERRY"],
    553: ["STRAWBERRY", "MILK"], 569: ["STRAWBERRY"], 572: ["STRAWBERRY"],
    573: ["STRAWBERRY"], 575: ["STRAWBERRY"], 576: ["STRAWBERRY"],
    577: ["STRAWBERRY", "MILK"], 601: ["STRAWBERRY", "WOOL"],
    619: ["STRAWBERRY"], 622: ["STRAWBERRY"], 625: ["STRAWBERRY", "MILK"],
    649: ["STRAWBERRY", "MILK", "WOOL"], 669: ["STRAWBERRY"], 673: ["STRAWBERRY"],
    
    # Milk/Wool
    169: ["WOOL"], 217: ["MILK"],
    241: ["WOOL"], 313: ["MILK", "WOOL"],
    361: ["MILK"], 385: ["MILK", "WOOL"],
    409: ["MILK"], 452: ["MILK", "WOOL"], 473: ["MILK"],
    475: ["MILK"], 497: ["MILK", "WOOL"], 521: ["MILK", "WOOL"],
    526: ["MILK", "WOOL"], 565: ["MILK", "WOOL"], 566: ["WOOL"], 567: ["MILK", "WOOL"],
    593: ["MILK"], 595: ["MILK"], 599: ["WOOL"],
    617: ["MILK"], 
    665: ["MILK", "WOOL"], 666: ["MILK"], 
    670: ["MILK"], 672: ["WOOL"], 
    697: ["MILK"],
    
    # End game sells
    715: ["WOOL", "WHEAT"], 716: ["MILK", "WOOL", "WHEAT", "FERTILIZER"],
    717: ["MILK", "WHEAT", "WOOL", "FERTILIZER"], 718: ["WHEAT"], 719: ["WHEAT"]
}

CENTER_TILES = [(4, 4), (5, 4), (4, 5), (5, 5)]

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

def dynamic_planner_agent(observation, configuration=None):
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
        for x, y in list(empty_tiles):
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
                tasks.append({"pos": (x, y), "action": "PLANT_STRAWBERRY", "priority": 28})
                strawberry_seeds -= 1
            elif melon_seeds > 0:
                tasks.append({"pos": (x, y), "action": "PLANT_MELON", "priority": 29})
                melon_seeds -= 1
            elif wheat_seeds > 0:
                tasks.append({"pos": (x, y), "action": "PLANT_WHEAT", "priority": 65})
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
                            tasks.append({"pos": (x, y), "action": "PLACE_COW", "priority": 16})
                        elif sheep_avail > 0:
                            tasks.append({"pos": (x, y), "action": "PLACE_SHEEP", "priority": 16})
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
                "priority": 5 if day == 29 else 35
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
            
            if tuple(u_pos) in CENTER_TILES and act not in ("FEED", "FERTILIZE", "PLACE_COW", "PLACE_SHEEP", "DROP_INVENTORY"):
                if sum(u_inv.values()) > 0:
                    unit_actions.append(["DROP"])
                    continue
            
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
                    elif act.startswith("PLANT_"):
                        crop = act.split("_")[1]
                        unit_actions.append(["PLANT", crop])
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

def agent(observation, configuration=None):
    player = observation["player"]
    day = observation["day"]
    hour = observation["hour"]
    me = observation["farms"][player]
    private = observation["private"]
    step = observation.get("step", day * 24 + hour)
    
    # -------------------------------------------------------------
    # ADAPTIVE HYBRID LOGIC
    # -------------------------------------------------------------
    # Detect if opponent is playing venks's static schedule.
    # At Step 24 (Day 1, Hour 0), venks always has exactly 5 hands and 12 Melon tiles planted.
    opponent_is_venks = True
    if step >= 24:
        opp = observation["farms"][1 - player]
        opp_hands = len(opp["hands"])
        opp_melons = sum(1 for row in opp["tiles"] for tile in row if isinstance(tile, dict) and tile.get("crop") == "MELON")
        if opp_hands != 5 or opp_melons != 12:
            opponent_is_venks = False
            
    # If the opponent is not venks, switch to the fully dynamic planner strategy
    if not opponent_is_venks:
        return dynamic_planner_agent(observation, configuration)
        
    # Otherwise, execute the hardcoded actions with perfect front-running against venks
    if step not in EARLY_ACTIONS:
        return {"farmer": ["PASS"], "hands": [], "market": []}
        
    base_act = EARLY_ACTIONS[step]
    action = {
        "farmer": list(base_act["farmer"]),
        "hands": [list(h) for h in base_act["hands"]],
        "market": [list(m) for m in base_act["market"]]
    }
    
    # Front-run premium crops 1 step before venks sells them
    next_step = step + 1
    if next_step in VENKS_SELL_STEPS:
        items_to_sell = VENKS_SELL_STEPS[next_step]
        for item in items_to_sell:
            count = private["shed"].get(item, 0)
            if count > 0:
                action["market"] = [["SELL", item, count]] + action["market"]
                
    action["market"] = action["market"][:10]
    return action
