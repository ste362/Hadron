# Hadron Game AI

This repository contains the AI logic for **Hadron**, a strategic game-playing AI that dynamically combines two powerful decision-making algorithms: **Alpha-Beta Pruning** and **Monte Carlo Tree Search (MCTS)**.

---

## 🧠 AI Strategy Overview

The core function powering Hadron's decision-making is:

```python
def montecarlo_alphabeta_search(game, state):
    if len(game.actions(state)) > 7:
        return monte_carlo_tree_search(game, state, 800)
    return h_alphabeta_search(game, state)
```

### 🔍 How It Works

- When the number of legal actions is **greater than 7**, the AI assumes the state is too complex for deterministic methods and uses **Monte Carlo Tree Search (MCTS)** to sample possible outcomes.
- When the number of legal actions is **7 or fewer**, it switches to a more precise **Heuristic Alpha-Beta Pruning** algorithm.

This hybrid approach allows the AI to scale well in complexity while retaining accuracy in simpler states.

---

## 🧩 Search Algorithms

### 🔺 Alpha-Beta Pruning (`alphabeta_search`, `h_alphabeta_search`)

- A classic optimization of the minimax algorithm.
- Efficiently prunes the game tree to avoid exploring unnecessary branches.
- `h_alphabeta_search` adds **unusual heuristic functions**—odd, non-intuitive evaluations that, despite seeming strange, have shown to work surprisingly well for Hadron’s game mechanics.
- The heuristics used aren't conventional, matches with an odd number of actions available are preferred, but they consistently improve decision-making performance based on extensive testing.

### 🎲 Monte Carlo Tree Search (`monte_carlo_tree_search`)

- Best suited for large and unpredictable decision spaces.
- Simulates random playouts from possible actions to estimate long-term value.
- The implementation here uses **800 simulations** per move for a balance between performance and precision.

---

## 💡 Why This Hybrid Works

- **MCTS** brings strength in wide, unpredictable scenarios where exploration is key.
- **Alpha-Beta** shines in narrow, tactical situations where deeper evaluation matters.
- By combining both and tuning when each is used, Hadron’s AI can adapt fluidly between early-game chaos and late-game precision.

---
