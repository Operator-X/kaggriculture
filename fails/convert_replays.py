import json
import os
import sys

def summarize_farm_tiles(tiles, current_day):
    plants = []
    animals = []
    structures = []
    locked_count = 0
    empty_unlocked = 0
    for r in range(10):
        for c in range(10):
            tile = tiles[r][c]
            if tile == 'LOCKED':
                locked_count += 1
            elif tile is None:
                empty_unlocked += 1
            elif isinstance(tile, dict):
                kind = tile.get('kind')
                if kind == 'PLANT':
                    crop = tile.get('crop')
                    planted = tile.get('planted_day', 0)
                    age = current_day - planted
                    watered = "watered" if tile.get('watered_today') else "dry"
                    yield_u = tile.get('yield_units', 0)
                    fert = tile.get('fertilized_until_day', -1)
                    fert_str = f" fert_until_day:{fert}" if fert != -1 else ""
                    plants.append(f"{crop}@{r},{c}(age:{age}, yield:{yield_u}, {watered}{fert_str})")
                elif kind in ['PASTURE', 'COOP']:
                    animal = tile.get('animal')
                    if animal:
                        fed = "fed" if tile.get('fed_today') else "unfed"
                        cared = "cared" if tile.get('cared_today') else "uncared"
                        yield_u = tile.get('yield_units', 0)
                        animals.append(f"{animal}@{r},{c}(yield:{yield_u}, {fed}, {cared})")
                    else:
                        structures.append(f"{kind}@{r},{c}(empty)")
                else:
                    structures.append(f"{kind}@{r},{c}")
    return plants, animals, structures, locked_count, empty_unlocked

def convert_file(json_path, txt_path):
    print(f"Converting {json_path} -> {txt_path}...")
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    # Extract metadata
    episode_id = data.get("info", {}).get("EpisodeId", "Unknown")
    rewards = data.get("rewards", [0, 0])
    statuses = data.get("statuses", ["Unknown", "Unknown"])
    agents = data.get("info", {}).get("Agents", [])
    agent_names = [a.get("Name", "Unknown") for a in agents]
    if len(agent_names) < 2:
        agent_names = ["Player 0", "Player 1"]
        
    steps = data.get("steps", [])
    
    with open(txt_path, 'w') as out:
        out.write("=" * 80 + "\n")
        out.write(f"EPISODE SUMMARY REPORT\n")
        out.write(f"Episode ID: {episode_id}\n")
        out.write(f"Player 0: {agent_names[0]} | Final Money: {rewards[0]:.1f} | Status: {statuses[0]}\n")
        out.write(f"Player 1: {agent_names[1]} | Final Money: {rewards[1]:.1f} | Status: {statuses[1]}\n")
        out.write("=" * 80 + "\n\n")
        
        for t, step in enumerate(steps):
            if len(step) < 2:
                continue
            
            p0_data = step[0]
            p1_data = step[1]
            
            obs = p0_data.get('observation', {})
            day = obs.get('day', 0)
            hour = obs.get('hour', 0)
            
            # Market prices
            market = obs.get('market', {})
            prices = market.get('prices', {})
            prices_str = ", ".join([f"{k}: {v}" for k, v in sorted(prices.items())])
            
            out.write("-" * 80 + "\n")
            out.write(f"Step: {t:03d} | Day: {day} | Hour: {hour}\n")
            out.write(f"Market Prices: {prices_str}\n")
            out.write("-" * 80 + "\n")
            
            for p in [0, 1]:
                p_data = step[p]
                p_obs = p_data.get('observation', {})
                farms = p_obs.get('farms', [])
                if len(farms) <= p:
                    # In case farms length is mismatching
                    continue
                farm = farms[p]
                
                farmer_pos = farm.get('farmer')
                hands_pos = farm.get('hands', [])
                money = farm.get('money', 0.0)
                
                # Actions
                action = p_data.get('action', {})
                farmer_act = action.get('farmer', ['PASS'])
                hands_act = action.get('hands', [])
                market_act = action.get('market', [])
                
                # Private info
                private = p_obs.get('private', {})
                seeds = private.get('seeds', {})
                shed = private.get('shed', {})
                inventories = private.get('inventories', [])
                
                plants, animals, structures, locked, empty = summarize_farm_tiles(farm.get('tiles', []), day)
                
                # Print info if present
                info = p_data.get('info', {})
                info_str = f" | Info: {info}" if info else ""
                
                status = p_data.get('status', 'ACTIVE')
                status_str = f" | Status: {status}" if status != 'ACTIVE' else ""
                
                name = agent_names[p]
                out.write(f"Player {p} ({name}) | Money: {money:.1f} | Hands: {len(hands_pos)}{status_str}{info_str}\n")
                out.write(f"  Farmer Pos: {farmer_pos} | Hands Pos: {hands_pos}\n")
                out.write(f"  Actions: Farmer: {farmer_act} | Hands: {hands_act} | Market: {market_act}\n")
                out.write(f"  Seeds: {seeds}\n")
                out.write(f"  Shed: {shed}\n")
                out.write(f"  Inventories (Active Hands): {inventories}\n")
                
                # Summarize farm content
                if plants:
                    out.write(f"  Plants ({len(plants)}): {', '.join(plants)}\n")
                if animals:
                    out.write(f"  Animals ({len(animals)}): {', '.join(animals)}\n")
                if structures:
                    out.write(f"  Structures ({len(structures)}): {', '.join(structures)}\n")
                out.write(f"  Empty Tiles: {empty} | Locked Tiles: {locked}\n")
                out.write("\n")
            out.write("\n")

def main():
    fails_dir = "/Users/lavlinjaison/Desktop/python/kaggleculture/fails"
    files = [f for f in os.listdir(fails_dir) if f.endswith(".json")]
    for f in sorted(files):
        json_path = os.path.join(fails_dir, f)
        txt_path = os.path.join(fails_dir, f.replace(".json", "_summary.txt"))
        convert_file(json_path, txt_path)

if __name__ == "__main__":
    main()
