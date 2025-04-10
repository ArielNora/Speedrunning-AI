# Speedrunning-AI

**Speedrunning-AI** is a fun and interactive project that explores how an artificial intelligence agent can learn to master 2D platformer-style levels — not just by completing them, but by doing so as fast as possible, just like in video game speedruns.

Speedrunning is a compelling lens through which to explore AI behavior. It demands not only completion but optimization, making it an ideal playground for experimenting with movement planning, reward strategies, and emergent behavior.

This project blends **game design**, **AI logic**, and **visual simulation** to create an environment where the agent is challenged to think fast, move smart, and plan ahead.

---

## Project Goals

- Train an AI agent to navigate platformer levels efficiently.
- Explore basic AI planning and learning strategies.
- Visualize the agent's decision-making in real time.
- Experiment with parametrable difficulty levels involving precision jumps, puzzle mechanics, and environment interactions.

---

## Key Features

- **Custom 2D Game Environment**: Simple tile-based levels with various mechanics.
- **Multiple Challenge Modes**:
  - **Level 1** – Basic navigation.
  - **Level 2** – Precision-focused gameplay.
  - **Level 3** – Puzzle-solving with buttons and triggers.
- **Interactive Notebook Mode** for step-by-step exploration.
- **Real-Time Graphics** to visualize the agent’s actions and learning process.

---

## How to Use

You can run the project in two ways:

### Option 1: Jupyter Notebook

Open the notebook in the `code` folder to:

- Load different levels
- Visualize the AI’s behavior
- Run experiments interactively

### Option 2: Python Script

Run `main.py` in the `code` folder. You can switch levels by editing the `levelnumber` variable:

```python
levelnumber = 1  # 1: Basic | 2: Precision | 3: Button
