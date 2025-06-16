# Meme Bot AI: Can a Machine Learn Comedy?



This project documents my attempt to teach an Artificial Intelligence to be funny. Using Python, Reinforcement Learning, and Computer Vision, this AI learns to tell jokes by watching my face and getting rewarded when I laugh.

The goal was to see if an AI could learn something as abstract and human as humor. I gave the AI a soundboard of classic meme sounds and a library of random images. Its task: find the combinations that make me laugh.

But this led to one of the biggest challenges in machine learning: the **Exploration vs. Exploitation dilemma**. The bot would often get addicted to one joke that worked once and spam it endlessly. This project is the story of solving that problem with creative chaos and advanced Reinforcement Learning techniques.

---

## 🤖 How It Works

The project is a closed-loop Reinforcement Learning system:

1.  **Action**: The AI agent (using the PPO algorithm) selects a sound to play.
2.  **Environment**: The Python environment plays the sound and begins cycling through a series of random images, creating a "call and response" comedic rhythm.
3.  **Observation**: An OpenCV and MediaPipe module watches my face via webcam in real-time.
4.  **Reward**: If the computer vision system detects a smile or a laugh, it calculates a positive "reward" signal. No reaction results in a small penalty.
5.  **Learning**: The reward is fed back to the PPO agent, which updates its neural network. It learns which sounds are more likely to create a context for a funny image combination, slowly developing its own unique sense of humor.

---

## 🛠️ Tech Stack & Concepts

*   **AI Framework**: Reinforcement Learning (Proximal Policy Optimization - PPO) with `stable-baselines3`
*   **Programming Language**: Python
*   **Computer Vision**: `OpenCV` for camera access and `MediaPipe` for facial landmark detection.
*   **GUI & Sound**: `pygame` for audio playback and `OpenCV` for window management.
*   **Core ML Concept**: Exploration vs. Exploitation dilemma.

---

## 🚀 Getting Started

Follow these steps to run the Meme Bot on your own machine and train it on *your* sense of humor.

### 1. Prerequisites

*   Python 3.8+ (Python 3.10 recommended)
*   A webcam
*   Git

### 2. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### 3. Set Up The Environment

First, create and activate a Python virtual environment. This keeps your project dependencies isolated.

```bash
# Create the virtual environment
python -m venv venv

# Activate it
# On Windows (PowerShell):
.\venv\Scripts\Activate
# On macOS/Linux:
source venv/bin/activate
```

Now, install all the required packages from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4. Add Your Memes

The AI needs raw material to work with.

*   **Sounds**: Place your meme audio clips (e.g., `vine-boom.mp3`, `bruh.mp3`) inside the `/sounds` folder.
*   **Images**: Place a wide variety of random images (memes, reaction images, abstract pictures, etc.) inside the `/images` folder. The more, the better!

*Tip: You can use the included scraper scripts (`scrape_myinstants_efficient.py` and `get_images_for_sounds.py`) to quickly populate these folders.*

### 5. Train Your AI

Run the main script in `train` mode. This will open your webcam and start the learning process. Your job is to react naturally!

```bash
python main.py train
```

The AI will save its progress in the `/models` folder. You can stop training at any time with `Ctrl+C` and it will resume where it left off.

**(Optional) Monitor with TensorBoard:** While training, open a second terminal, activate the environment, and run:
```bash
tensorboard --logdir logs
```
This will launch a dashboard in your browser where you can see the AI's reward progress and other metrics live.

### 6. Test Your Comedian

Once you've trained the model for a while, run it in `test` mode to see what it has learned. It will now try to play the jokes it thinks are the funniest.

```bash
python main.py test
```

Can it make you laugh?

---

## 📁 Project Structure

```
meme_generator/
│
├── models/               # Saved AI models
├── sounds/               # Your meme audio files
├── images/               # Your meme image files
│
├── config.py             # All project settings and hyperparameters
├── laugh_detector.py     # Computer vision module for smile/laugh detection
├── meme_env.py           # The custom Reinforcement Learning environment
├── trainer.py            # Logic for training the agent
├── tester.py             # Logic for testing the agent
├── main.py               # Main entry point to run the app
│
├── .gitignore            # Specifies which files Git should ignore
├── requirements.txt      # List of project dependencies
└── README.md             # This file
```
