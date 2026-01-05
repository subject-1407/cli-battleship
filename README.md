# CLI Battleship (Work in Progress)

This is a command-line implementation of Battleship in Python.  
The game is playable in the terminal and currently supports:

- Random ship placement for both player and AI
- Player and AI turns (AI currently "easy" mode random targeting)
- Basic hit/miss logic and view updates
- Fog of war using separate ocean and radar views

This project is a work in progress and is designed to demonstrate Python programming, CLI interaction, and game logic implementation.

---

## Features

- Ships of standard sizes: Carrier (5), Battleship (4), Cruiser (3), Submarine (3), Destroyer (2)
- 10x10 grid representation
- Clear terminal-based visual output
- Turn-based play with simple AI

---

## How to Play

Run the game:

```bash
python3 cli-battleship.py
```

---

## TODO

- Manual ship placement
- Fully implemented player turns
- AI hard mode with strategy
- Better input validation and coordinate handling
- Game statistics (turn count, hit/miss ratio)
