import sys
from kaggle_environments import make

def run_match(agent1_path, agent2_name, steps=720):
    print(f"--- Running simulation: {agent1_path} vs {agent2_name} ({steps} steps) ---")
    
    # Initialize the kaggriculture environment
    env = make("kaggriculture", configuration={"episodeSteps": steps}, debug=True)
    
    # Run the environment
    # We pass the file path for our agent, which tests that it's self-contained and loads correctly
    try:
        env.run([agent1_path, agent2_name])
    except Exception as e:
        print(f"Error during simulation: {e}")
        import traceback
        traceback.print_exc()
        return None

    # Get the final step outputs
    final_step = env.steps[-1]
    
    for i, player_state in enumerate(final_step):
        reward = player_state.reward
        status = player_state.status
        name = "Our Agent (P0)" if i == 0 else f"{agent2_name} (P1)"
        print(f"  {name}: final money = {reward}, status = {status}")
        
    return env

def main():
    agent_path = "main.py"
    
    # 1. Play against "random"
    run_match(agent_path, "random", steps=720)
    
    print()
    
    # 2. Play against "starter"
    run_match(agent_path, "starter", steps=720)
    
    print()
    
    # 3. Play against itself
    run_match(agent_path, "main.py", steps=720)

if __name__ == "__main__":
    main()
