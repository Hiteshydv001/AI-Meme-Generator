# config.py
import os

# --- Directory Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOUNDS_DIR = os.path.join(BASE_DIR, "sounds")
IMAGES_DIR = os.path.join(BASE_DIR, "images")
MODELS_DIR = os.path.join(BASE_DIR, "models")
LOG_DIR = os.path.join(BASE_DIR, "logs")

# --- Model and Training Parameters ---
MODEL_NAME = "meme_rhythm_ppo" # New name for this new task
MODEL_PATH = os.path.join(MODELS_DIR, f"{MODEL_NAME}.zip")
TOTAL_TIMESTEPS = 10000  # This is a complex task, it may need more steps

# PPO Hyperparameters
N_STEPS = 20           # An "episode" is now 20 turns
BATCH_SIZE = 20
ENT_COEF = 0.015       # Encourage exploration of different sounds
LEARNING_RATE = 0.0003

# --- Environment Parameters ---
EPISODE_LENGTH = N_STEPS
NO_REACTION_PENALTY = -0.1

# NEW: Parameters for the "Call and Response" rhythm
NUM_IMAGES_PER_SOUND = 4      # Total images to show for one sound
IMAGE_DISPLAY_DURATION = 2.0  # Seconds to show each subsequent image after sound finishes

# --- Laugh Detector Parameters ---
SMILE_THRESHOLD = 0.5
LAUGH_THRESHOLD = 0.9
SMILE_REWARD = 1.0
LAUGH_REWARD = 10.0
REWARD_COOLDOWN = 2.0 # Increase cooldown slightly for this rhythm