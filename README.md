# Player Rotation Script

## Introduction

This Python script is designed to manage player rotations for sports or games. It ensures that each player gets an equal opportunity to play and rest, while also keeping track of the number of times each pair of players has played together. It's perfect for organizing team rotations in games like badminton, volleyball, etc.

## Features

- **Player Rotation**: Automatically rotates players to ensure equal playing time.
- **Duplicate Name Check**: Identifies and alerts if there are duplicate player names.
- **Pair Tracking**: Keeps track of how often each pair of players has played together.
- **Flexible Rounds and Courts**: Supports different numbers of rounds and courts.
- **Rest and Play Management**: Manages which players are resting and playing each round.

## Requirements

- Python installed on your computer.
- Basic understanding of how to run Python scripts.

## How to Use

1. **List of Players**: First, update the `players` list in the script with the names of all the players participating.

    ```python
    players = ['Player1', 'Player2', 'Player3', ...]
    ```

2. **Running the Script**: Use a Python interpreter to run the script. You can do this by opening a terminal or command prompt, navigating to the folder where the script is located, and typing `python script_name.py`.

3. **Output**: The script will display the playing and resting players for each round, as well as the pairing counts if chosen.

4. **Parameters**:
    - **Max Rounds**: The number of rounds to be played. Default is set to 10.
    - **Max Courts**: The maximum number of courts available. Default is calculated based on the number of players.

5. **Duplicate Names**: If there are players with identical names, the script will prompt you to differentiate them (e.g., by adding a surname).

6. **Display Flags**: The script ends with a `main_with_counters` function call, where `display_flag='Y'` will show detailed statistics about player rotations and pairings after the rounds are completed.

## Customization

- **Modifying Player List**: Change the `players` list to include the names of your participants.
- **Changing Rounds and Courts**: Adjust the `max_rounds` and `max_courts` variables to fit your needs.
