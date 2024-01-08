import itertools
import random
from collections import deque, defaultdict

def read_players(file_name):
    """Reads player names from a file, checks for duplicates, and returns a list of names."""
    try:
        with open(file_name, 'r') as file:
            players = [line.strip() for line in file if line.strip()]
            player_counts = defaultdict(int)
            for player in players:
                player_counts[player] += 1

            duplicates = [player for player, count in player_counts.items() if count > 1]
            if duplicates:
                for duplicate in duplicates:
                    print(f"Duplicate name found: {duplicate}. Please remove or add a short surname.")
                return []

            return players
    except FileNotFoundError:
        print(f"Error: The file {file_name} was not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def find_combinations_for_players(players, max_courts, rest_queue):
    """Finds possible combinations of players for the courts."""
    if not players or max_courts * 4 > len(players):
        return []

    if not rest_queue or len(rest_queue) < len(players):
        rest_queue.extend(players)

    selected_combinations = []
    used_players = set()

    num_active_players = max_courts * 4
    rest_players = [rest_queue[i] for i in range(len(players) - num_active_players) if i < len(rest_queue)]
    available_players = set(players) - set(rest_players)

    all_combinations = list(itertools.combinations(available_players, 4))
    random.shuffle(all_combinations)

    for comb in all_combinations:
        if len(selected_combinations) == max_courts:
            break
        if not set(comb).intersection(used_players):
            selected_combinations.append(comb)
            used_players.update(comb)

    rest_queue.rotate(-num_active_players)

    return selected_combinations

def print_round(round_number, round_combinations, players):
    """Prints the details of the current round."""
    if not round_combinations:
        print(f"Round {round_number} cannot be played due to insufficient players.")
        return

    # Determine the active and resting players
    active_players = set()
    for court_players in round_combinations:
        active_players.update(court_players)

    resting_players = set(players) - active_players

    # Prepare the round information string
    round_info = f"Round {round_number} Resting Players:"
    underlined_info = "\u0332".join(round_info) + "\u0332"  # Underline up to "Resting Players:"
    print(underlined_info + " " + ', '.join(resting_players))

    # Print the details for each court
    for court_number, court_players in enumerate(round_combinations, 1):
        # Split the team into two pairs and format the output
        team1 = f"{court_players[0]}, {court_players[1]}"
        team2 = f"{court_players[2]}, {court_players[3]}"
        print(f"Court {court_number}: {team1}  vs  {team2}")

    print()  # Adds a newline for better readability



def main():
    """Main function to drive the program."""
    file_name = 'players.txt'  # Replace with your actual file path
    players = read_players(file_name)
    if not players:
        return

    max_rounds = 10
    max_courts = min(4, len(players) // 4)

    if max_courts == 0:
        print("Not enough players to form a court.")
        return

    rest_queue = deque()

    for round_number in range(1, max_rounds + 1):
        round_combinations = find_combinations_for_players(players, max_courts, rest_queue)
        print_round(round_number, round_combinations, players)

if __name__ == "__main__":
    main()
