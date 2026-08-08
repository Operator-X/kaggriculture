# venks_killer_dynamic.py
# Kaggriculture Sabotage Agent with Dynamic Real-time Opponent Tracking.
# Runs with a 1-hour shift to start at Step 0 and prevent opponent head starts.

import json
import zlib
import base64

VENKS_ACTIONS_DATA = "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"

# Parse original actions
ORIG_ACTIONS = {int(k): v for k, v in json.loads(zlib.decompress(base64.b64decode(VENKS_ACTIONS_DATA.strip().encode('utf-8'))).decode('utf-8')).items()}

# Shift schedule by -1 hour
EARLY_ACTIONS = {k - 1: v for k, v in ORIG_ACTIONS.items() if k > 0}

# Persistent opponent tracking state
PREV_OPP_TILES = None
OPP_HARVESTED_CARRYING = {"MELON": 0, "STRAWBERRY": 0, "MILK": 0, "WOOL": 0}
OPP_SHED_ESTIMATE = {"MELON": 0, "STRAWBERRY": 0, "MILK": 0, "WOOL": 0}

def track_opponent_activity(opp_tiles, opp_units):
    global PREV_OPP_TILES, OPP_HARVESTED_CARRYING, OPP_SHED_ESTIMATE
    
    if PREV_OPP_TILES is None:
        PREV_OPP_TILES = [[None]*10 for _ in range(10)]
        
    # 1. Detect harvests: compare prev tiles to current tiles
    for y in range(10):
        for x in range(10):
            prev_tile = PREV_OPP_TILES[y][x]
            curr_tile = opp_tiles[y][x]
            
            # Case A: Crop harvested
            if isinstance(prev_tile, dict) and prev_tile.get("kind") == "PLANT":
                crop = prev_tile.get("crop")
                is_harvested = False
                if curr_tile is None or (isinstance(curr_tile, dict) and curr_tile.get("kind") == "WEED"):
                    is_harvested = True
                elif isinstance(curr_tile, dict) and curr_tile.get("kind") == "PLANT":
                    # If yield units dropped to 0
                    if prev_tile.get("yield_units", 0) > 0 and curr_tile.get("yield_units", 0) == 0:
                        is_harvested = True
                        
                if is_harvested and crop in OPP_HARVESTED_CARRYING:
                    qty = prev_tile.get("yield_units", 1)
                    OPP_HARVESTED_CARRYING[crop] += qty
                    
            # Case B: Animal product collected (pasture yield dropped)
            elif isinstance(prev_tile, dict) and prev_tile.get("kind") == "PASTURE":
                animal = prev_tile.get("animal")
                if animal == "COW" and isinstance(curr_tile, dict) and curr_tile.get("animal") == "COW":
                    if prev_tile.get("yield_units", 0) > 0 and curr_tile.get("yield_units", 0) == 0:
                        OPP_HARVESTED_CARRYING["MILK"] += prev_tile.get("yield_units", 1)
                elif animal == "SHEEP" and isinstance(curr_tile, dict) and curr_tile.get("animal") == "SHEEP":
                    if prev_tile.get("yield_units", 0) > 0 and curr_tile.get("yield_units", 0) == 0:
                        OPP_HARVESTED_CARRYING["WOOL"] += prev_tile.get("yield_units", 1)
                        
    # Update prev tiles reference
    PREV_OPP_TILES = [list(row) for row in opp_tiles]
    
    # 2. Detect drops: check if any opponent unit is adjacent to the center shed
    center_tiles = {(4, 4), (5, 4), (4, 5), (5, 5)}
    opp_at_shed = False
    for pos in opp_units:
        if tuple(pos) in center_tiles:
            opp_at_shed = True
            break
            
    if opp_at_shed:
        # Transfer carrying balance to the shed estimate
        for item in OPP_HARVESTED_CARRYING:
            if OPP_HARVESTED_CARRYING[item] > 0:
                OPP_SHED_ESTIMATE[item] += OPP_HARVESTED_CARRYING[item]
                OPP_HARVESTED_CARRYING[item] = 0

def agent(observation, configuration=None):
    global PREV_OPP_TILES, OPP_HARVESTED_CARRYING, OPP_SHED_ESTIMATE
    
    player = observation["player"]
    day = observation["day"]
    hour = observation["hour"]
    private = observation["private"]
    step = observation.get("step", day * 24 + hour)
    
    # Reset tracking state at Step 0
    if step == 0:
        PREV_OPP_TILES = None
        OPP_HARVESTED_CARRYING = {"MELON": 0, "STRAWBERRY": 0, "MILK": 0, "WOOL": 0}
        OPP_SHED_ESTIMATE = {"MELON": 0, "STRAWBERRY": 0, "MILK": 0, "WOOL": 0}
        
    # Get opponent public state
    opp_farm = observation["farms"][1 - player]
    opp_tiles = opp_farm["tiles"]
    opp_units = [opp_farm["farmer"]] + list(opp_farm["hands"])
    
    # Track opponent activity
    track_opponent_activity(opp_tiles, opp_units)
    
    # Fallback if step is out of bounds
    if step not in EARLY_ACTIONS:
        return {"farmer": ["PASS"], "hands": [], "market": []}
        
    # Base copy of venks actions
    base_act = EARLY_ACTIONS[step]
    action = {
        "farmer": list(base_act["farmer"]),
        "hands": [list(h) for h in base_act["hands"]],
        "market": [list(m) for m in base_act["market"]]
    }
    
    # -------------------------------------------------------------
    # SABOTAGE: DYNAMIC REAL-TIME FRONT-RUNNING
    # -------------------------------------------------------------
    # Check if the opponent has crops/products sitting in their shed.
    # If so, we sell ours immediately to capture the high price and crash theirs!
    items_to_sell = []
    for item in ["MELON", "STRAWBERRY", "MILK", "WOOL"]:
        if OPP_SHED_ESTIMATE[item] > 0:
            items_to_sell.append(item)
            # Reset shed estimate once we act on it
            OPP_SHED_ESTIMATE[item] = 0
            
    # Inject front-running sell orders
    for item in items_to_sell:
        count = private["shed"].get(item, 0)
        if count > 0:
            action["market"] = [["SELL", item, count]] + action["market"]
            
    # End-game liquidation safety net (sells everything on final steps)
    if step in [714, 715, 716, 717, 718]:
        for item in ["WOOL", "MILK", "WHEAT", "FERTILIZER"]:
            count = private["shed"].get(item, 0)
            if count > 0:
                action["market"] = [["SELL", item, count]] + action["market"]
                
    action["market"] = action["market"][:10]
    return action
