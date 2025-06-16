# meme_env.py

import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame
import os
import cv2
import time
import random
import config
from laugh_detector import LaughDetector

class MemeEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 30}

    def __init__(self, render_mode="human"):
        super().__init__()
        self._setup_assets()
        pygame.mixer.init()
        
        # The AI's action is simplified: just choose a sound.
        self.action_space = spaces.Discrete(len(self.sound_paths))
        self.observation_space = spaces.Box(low=0, high=255, shape=(1,), dtype=np.uint8)

        self.laugh_detector = LaughDetector()
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened(): raise IOError("Cannot open webcam.")
            
        self.render_mode = render_mode
        self.webcam_window, self.meme_window = "Reaction Cam", "Meme"
        self.current_step = 0

    def _setup_assets(self):
        """Loads all sounds and images into separate lists."""
        print("--- Loading Sound and Image Libraries ---")
        self.sound_paths = [os.path.join(config.SOUNDS_DIR, f) for f in os.listdir(config.SOUNDS_DIR) if f.endswith(('.mp3', '.wav'))]
        self.image_paths = [os.path.join(config.IMAGES_DIR, f) for f in os.listdir(config.IMAGES_DIR) if f.endswith(('.jpg', '.png', '.jpeg'))]
        if not self.sound_paths: raise ValueError("No sounds found.")
        if not self.image_paths: raise ValueError("No images found.")
        print(f"Loaded {len(self.sound_paths)} sounds and {len(self.image_paths)} images.")

    def _show_random_image(self):
        """Selects and displays a single random image."""
        image_path = random.choice(self.image_paths)
        if self.render_mode == 'human':
            img = cv2.imread(image_path)
            if img is not None:
                cv2.imshow(self.meme_window, img)
            else:
                print(f"Warning: Could not load image at {image_path}")
        return image_path

    def _get_reaction_for_duration(self, duration):
        """Monitors for a laugh for a given duration and returns max reward."""
        max_reward_in_period = 0.0
        start_time = time.time()
        while time.time() - start_time < duration:
            ret, frame = self.cap.read()
            if not ret: break
            frame = cv2.flip(frame, 1)
            reward, annotated_frame = self.laugh_detector.get_reward_from_frame(frame)
            max_reward_in_period = max(max_reward_in_period, reward)
            
            if self.render_mode == "human":
                cv2.imshow(self.webcam_window, annotated_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.close(); exit()
        return max_reward_in_period

    def step(self, action):
        # The AI's action is just the index of the sound to play.
        sound_path = self.sound_paths[action]
        print(f"\nAction: Playing sound '{os.path.basename(sound_path)}'")
        
        sound = pygame.mixer.Sound(sound_path)
        sound.play()

        max_reward_for_step = 0.0
        
        # --- Phase 1: While Sound is Playing ---
        first_image_path = self._show_random_image()
        print(f"  + Showing image '{os.path.basename(first_image_path)}'")
        
        # Monitor for reaction while the sound is busy
        while pygame.mixer.get_busy():
            max_reward_for_step = max(max_reward_for_step, self._get_reaction_for_duration(0.1))

        # --- Phase 2: After Sound Finishes, Cycle Images ---
        print("  - Sound finished. Cycling images...")
        for i in range(config.NUM_IMAGES_PER_SOUND - 1):
            next_image_path = self._show_random_image()
            print(f"  + Showing new image '{os.path.basename(next_image_path)}'")
            # Monitor for reaction for a fixed duration for this new image
            max_reward_for_step = max(max_reward_for_step, self._get_reaction_for_duration(config.IMAGE_DISPLAY_DURATION))

        # --- Cleanup and Finalize ---
        if self.render_mode == 'human':
            try: cv2.destroyWindow(self.meme_window)
            except cv2.error: pass

        self.current_step += 1
        terminated = self.current_step >= config.EPISODE_LENGTH
        final_reward = max_reward_for_step if max_reward_for_step > 0 else config.NO_REACTION_PENALTY
        
        print(f"-> Final reward for this sequence: {final_reward:.2f}")
        return np.array([0]), final_reward, terminated, False, {}

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.current_step = 0
        print("\n" + "="*10 + " NEW EPISODE " + "="*10)
        return np.array([0]), {}

    def close(self):
        print("Closing environment and releasing resources.")
        if self.cap.isOpened(): self.cap.release()
        cv2.destroyAllWindows()
        pygame.mixer.quit()
        if hasattr(self, 'laugh_detector'): self.laugh_detector.close()