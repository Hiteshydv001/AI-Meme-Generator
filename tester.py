# tester.py

import os
import time
from stable_baselines3 import PPO
import config
from meme_env import MemeEnv

def test_agent():
    """Loads and tests the trained PPO agent."""
    print("--- 🤖 INITIALIZING TEST MODE ---")

    if not os.path.exists(config.MODEL_PATH):
        print(f"ERROR: Model not found at {config.MODEL_PATH}")
        print("Please train the agent first by running 'python main.py train'")
        return

    print(f"Loading model from: {config.MODEL_PATH}")
    env = MemeEnv(render_mode="human")
    model = PPO.load(config.MODEL_PATH)
    
    print("--- TESTING STARTED ---")
    print("The AI will now use its learned knowledge to be funny.")
    print("Press 'q' in the webcam window to quit.")
    
    try:
        obs, _ = env.reset()
        while True:
            action, _ = model.predict(obs, deterministic=True)
            obs, _, terminated, _, _ = env.step(action)
            
            if terminated:
                obs, _ = env.reset()
            time.sleep(1.5) # Pause between jokes
    except Exception as e:
        print(f"An error occurred during testing: {e}")
    finally:
        env.close()