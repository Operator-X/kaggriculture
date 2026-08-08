# run_tournament.py
# Simulates a round-robin tournament between all local agents and baselines.

import os
import sys
import traceback
from kaggle_environments import make

def main():
    agents = [
        "random",
        "starter",
        "main.py",
        "main_v8.py",
        "main_v9.py",
        "ben_v2.py",
        "ben.py",
        "venks_killer.py",
        "venks_killer_hybrid.py",
        "venks_variant.py",
        "venks_killer_dynamic.py"
    ]
    
    # Track stats: {agent: {"wins": 0, "draws": 0, "losses": 0, "points": 0, "scores": []}}
    stats = {a: {"wins": 0, "draws": 0, "losses": 0, "points": 0, "scores": []} for a in agents}
    
    matches = []
    for i in range(len(agents)):
        for j in range(len(agents)):
            if i != j:
                matches.append((agents[i], agents[j]))
                
    total_matches = len(matches)
    print(f"Starting tournament: {len(agents)} agents, {total_matches} matches (double round-robin).")
    
    for idx, (a1, a2) in enumerate(matches):
        print(f"[{idx+1}/{total_matches}] Running: {a1} vs {a2}...", end="", flush=True)
        
        try:
            env = make("kaggriculture", configuration={"episodeSteps": 720})
            env.run([a1, a2])
            
            # Extract final rewards
            r0 = env.steps[-1][0].reward
            r1 = env.steps[-1][1].reward
            
            # Status check for errors
            s0 = env.steps[-1][0].status
            s1 = env.steps[-1][1].status
            
            if s0 == "ERROR":
                r0 = 0.0
            if s1 == "ERROR":
                r1 = 0.0
                
            stats[a1]["scores"].append(r0)
            stats[a2]["scores"].append(r1)
            
            if r0 > r1:
                stats[a1]["wins"] += 1
                stats[a1]["points"] += 3
                stats[a2]["losses"] += 1
                result = f"{a1} won (${r0:.1f} vs ${r1:.1f})"
            elif r0 < r1:
                stats[a2]["wins"] += 1
                stats[a2]["points"] += 3
                stats[a1]["losses"] += 1
                result = f"{a2} won (${r1:.1f} vs ${r0:.1f})"
            else:
                stats[a1]["draws"] += 1
                stats[a1]["points"] += 1
                stats[a2]["draws"] += 1
                stats[a2]["points"] += 1
                result = f"Draw (${r0:.1f} vs ${r1:.1f})"
                
            print(f" {result}")
            
        except Exception as e:
            print(f" ERROR: {e}")
            traceback.print_exc()
            
    print("\nTournament complete! Generating leaderboard...\n")
    
    # Sort agents by points (descending), then average score (descending)
    leaderboard = []
    for name, data in stats.items():
        avg_score = sum(data["scores"]) / len(data["scores"]) if data["scores"] else 0.0
        win_rate = (data["wins"] / (data["wins"] + data["draws"] + data["losses"])) * 100 if (data["wins"] + data["draws"] + data["losses"]) > 0 else 0.0
        leaderboard.append({
            "name": name,
            "wins": data["wins"],
            "draws": data["draws"],
            "losses": data["losses"],
            "points": data["points"],
            "avg_score": avg_score,
            "win_rate": win_rate
        })
        
    leaderboard.sort(key=lambda x: (x["points"], x["avg_score"]), reverse=True)
    
    # Print leaderboard to console
    print(f"{'Rank':<5} | {'Agent':<25} | {'Wins':<5} | {'Draws':<5} | {'Losses':<6} | {'Points':<6} | {'Win Rate %':<10} | {'Avg Score':<12}")
    print("-" * 95)
    for rank, entry in enumerate(leaderboard, 1):
        print(f"{rank:<5} | {entry['name']:<25} | {entry['wins']:<5} | {entry['draws']:<5} | {entry['losses']:<6} | {entry['points']:<6} | {entry['win_rate']:<10.1f} | ${entry['avg_score']:<12.1f}")
        
    # Write markdown report
    report_path = "/Users/lavlinjaison/Desktop/python/kaggleculture/tournament_report.md"
    with open(report_path, "w") as f:
        f.write("# Kaggriculture Local Tournament Leaderboard\n\n")
        f.write("| Rank | Agent Name | Wins | Draws | Losses | Points | Win Rate % | Avg Score |\n")
        f.write("| --- | --- | --- | --- | --- | --- | --- | --- |\n")
        for rank, entry in enumerate(leaderboard, 1):
            f.write(f"| {rank} | `{entry['name']}` | {entry['wins']} | {entry['draws']} | {entry['losses']} | **{entry['points']}** | {entry['win_rate']:.1f}% | ${entry['avg_score']:.1f} |\n")
            
    print(f"\nMarkdown report generated successfully at: {report_path}")

if __name__ == "__main__":
    main()
