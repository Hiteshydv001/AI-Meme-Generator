# trainer.py

import os
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
import config
from meme_env import MemeEnv

def train_agent():
    """Initializes and trains the PPO agent."""
    print("--- 🧠 INITIALIZING TRAINING ---")
    
    # Ensure necessary directories exist
    os.makedirs(config.MODELS_DIR, exist_ok=True)
    os.makedirs(config.LOG_DIR, exist_ok=True)
    
    # Create the vectorized environment
    vec_env = make_vec_env(MemeEnv, n_envs=1, env_kwargs=dict(render_mode="human"))
    
    # Check for an existing model to continue training, otherwise create a new one
    if os.path.exists(config.MODEL_PATH):
        print(f"Loading existing model from: {config.MODEL_PATH}")
        model = PPO.load(
            config.MODEL_PATH,
            env=vec_env,
            custom_objects={"learning_rate": config.LEARNING_RATE, "ent_coef": config.ENT_COEF}
        )
    else:
        print("No existing model found. Creating a new one.")
        model = PPO(
            "MlpPolicy", 
            vec_env, 
            verbose=1, 
            tensorboard_log=config.LOG_DIR,
            n_steps=config.N_STEPS,
            batch_size=config.BATCH_SIZE,
            ent_coef=config.ENT_COEF,
            learning_rate=config.LEARNING_RATE
        )

    print("--- TRAINING STARTED ---")
    print("React to the memes! The AI is learning from your laughs.")
    print("You can stop training anytime with Ctrl+C. Progress will be saved.")
    
    try:
        model.learn(
            total_timesteps=config.TOTAL_TIMESTEPS,
            reset_num_timesteps=not os.path.exists(config.MODEL_PATH)
        )
    except KeyboardInterrupt:
        print("\nTraining interrupted by user.")
    finally:
        print("Saving model...")
        model.save(config.MODEL_PATH)
        print(f"Model saved to {config.MODEL_PATH}")
        vec_env.close()

    print("--- ✅ TRAINING COMPLETE ---")