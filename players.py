import random
from itertools import combinations
from collections import defaultdict

class BadmintonManager:
    def __init__(self, max_courts=4, max_rounds=10, print_stats=False):
        self.max_courts = max_courts
        self.max_rounds = max_rounds
        self.print_stats = print_stats
        self.players = set()
        self.partner_history = defaultdict(lambda: defaultdict(int))
        self.opponent_history = defaultdict(lambda: defaultdict(int))
        self.court_history = defaultdict(lambda: defaultdict(int))
        self.rest_history = defaultdict(int)
        self.games_played = defaultdict(int)

    def load_players(self, filename):
        try:
            with open(filename, 'r') as f:
                self.players = set(line.strip() for line in f if line.strip())
        except FileNotFoundError:
            raise Exception(f"Player file {filename} not found")
        
        if len(self.players) < 4:
            raise Exception("Need at least 4 players")

    def update_history(self, team1, team2, court):
        # Update partnerships
        for p1, p2 in combinations(team1, 2):
            self.partner_history[p1][p2] += 1
            self.partner_history[p2][p1] += 1
        for p1, p2 in combinations(team2, 2):
            self.partner_history[p1][p2] += 1
            self.partner_history[p2][p1] += 1

        # Update oppositions
        for p1 in team1:
            for p2 in team2:
                self.opponent_history[p1][p2] += 1
                self.opponent_history[p2][p1] += 1

        # Update court history and games played
        for player in team1 | team2:
            self.court_history[player][court] += 1
            self.games_played[player] += 1

    def calculate_team_score(self, team1, team2):
        score = 0
        
        # Partnership score - penalize repeated partnerships
        for t1p1, t1p2 in combinations(team1, 2):
            score -= WEIGHTS['PARTNERSHIP'] * self.partner_history[t1p1][t1p2]
        for t2p1, t2p2 in combinations(team2, 2):
            score -= WEIGHTS['PARTNERSHIP'] * self.partner_history[t2p1][t2p2]

        # Opposition score - penalize repeated oppositions
        for p1 in team1:
            for p2 in team2:
                score -= WEIGHTS['OPPOSITION'] * self.opponent_history[p1][p2]

        # Game balance score - prefer players who played fewer games
        team1_games = sum(self.games_played[p] for p in team1)
        team2_games = sum(self.games_played[p] for p in team2)
        score -= WEIGHTS['GAME_BALANCE'] * abs(team1_games - team2_games)

        # New interaction score - encourage new partnerships and oppositions
        for p1 in team1:
            for p2 in team2:
                if self.opponent_history[p1][p2] == 0:
                    score += WEIGHTS['NEW_INTERACTION']

        return score

    def generate_round(self, round_num):
        available_players = list(self.players)
        num_players_needed = self.max_courts * 4
        
        if len(available_players) < num_players_needed:
            num_courts = len(available_players) // 4
        else:
            num_courts = self.max_courts

        num_players_needed = num_courts * 4
        resting_players = set()

        if len(available_players) > num_players_needed:
            # Select players who rested least to rest
            players_by_rest = sorted(available_players, 
                                   key=lambda p: (self.rest_history[p], random.random()))
            num_to_rest = len(available_players) - num_players_needed
            resting_players = set(players_by_rest[:num_to_rest])
            
            # Update rest history
            for player in resting_players:
                self.rest_history[player] += 1
            
            # Remove resting players from available players
            available_players = [p for p in available_players if p not in resting_players]

        # Generate all possible team combinations
        best_assignments = []
        players_per_court = len(available_players) // num_courts
        
        for court in range(num_courts):
            remaining_players = [p for p in available_players if not any(p in team 
                               for assignment in best_assignments 
                               for team in assignment[1:])]
            
            best_score = float('-inf')
            best_teams = None

            # Try different team combinations for this court
            possible_teams = list(combinations(remaining_players, players_per_court // 2))
            for team1 in possible_teams:
                team1_set = set(team1)
                remaining_for_team2 = [p for p in remaining_players if p not in team1_set]
                
                for team2 in combinations(remaining_for_team2, players_per_court // 2):
                    score = self.calculate_team_score(set(team1), set(team2))
                    if score > best_score:
                        best_score = score
                        best_teams = (team1, team2)

            if best_teams:
                best_assignments.append((court + 1, set(best_teams[0]), set(best_teams[1])))
                # Update history
                self.update_history(set(best_teams[0]), set(best_teams[1]), court + 1)

        return resting_players, best_assignments

    def get_player_stats(self, player):
        total_games = self.games_played[player]
        unique_partners = sum(1 for p, count in self.partner_history[player].items() if count > 0)
        unique_opponents = sum(1 for p, count in self.opponent_history[player].items() if count > 0)
        times_rested = self.rest_history[player]
        
        # Calculate court distribution
        court_distribution = {}
        total_court_games = sum(self.court_history[player].values())
        for court, count in self.court_history[player].items():
            percentage = (count / total_court_games * 100) if total_court_games > 0 else 0
            court_distribution[court] = {'count': count, 'percentage': percentage}

        return {
            'total_games': total_games,
            'unique_partners': unique_partners,
            'unique_opponents': unique_opponents,
            'times_rested': times_rested,
            'court_distribution': court_distribution
        }

    def print_detailed_stats(self):
        if not self.print_stats:
            return

        print("\nP̲l̲a̲y̲e̲r̲ ̲S̲t̲a̲t̲i̲s̲t̲i̲c̲s̲:")
        for player in sorted(self.players):
            stats = self.get_player_stats(player)
            print(f"\n{player}")
            print(f"Games Played: {stats['total_games']}")
            print(f"Unique Partners: {stats['unique_partners']}")
            print(f"Unique Opponents: {stats['unique_opponents']}")
            print(f"Times Rested: {stats['times_rested']}")
            
            print("\nC̲o̲u̲r̲t̲ ̲D̲i̲s̲t̲r̲i̲b̲u̲t̲i̲o̲n̲:")
            for court, data in sorted(stats['court_distribution'].items()):
                print(f"Court {court}: {data['count']} ({data['percentage']:.1f}%)")
            
            print("\nP̲a̲r̲t̲n̲e̲r̲ ̲H̲i̲s̲t̲o̲r̲y̲:")
            partners = sorted(
                [(p, c) for p, c in self.partner_history[player].items() if c > 0],
                key=lambda x: (-x[1], x[0])
            )
            for partner, count in partners:
                print(f"{partner}: {count}x")
            print("-" * 40)

    def print_schedule(self):
        print("\nB̲a̲d̲m̲i̲n̲t̲o̲n̲ ̲S̲c̲h̲e̲d̲u̲l̲e̲")
        print("-" * 40)

        for round_num in range(1, self.max_rounds + 1):
            resting_players, court_assignments = self.generate_round(round_num)
            print(f"\nR̲o̲u̲n̲d̲ ̲{round_num}")
            print(f"R̲e̲s̲t̲i̲n̲g̲ ̲P̲l̲a̲y̲e̲r̲s̲: {', '.join(sorted(resting_players))}")
            
            for court, team1, team2 in court_assignments:
                print(f"Court {court}: {', '.join(sorted(team1))} vs {', '.join(sorted(team2))}")
            print("-" * 40)
        
        if self.print_stats:
            self.print_detailed_stats()

WEIGHTS = {
    'PARTNERSHIP': 1000,
    'OPPOSITION': 500,
    'GAME_BALANCE': 200,
    'NEW_INTERACTION': 100
}

def main():
    try:
        manager = BadmintonManager(max_courts=4, max_rounds=10)
        manager.load_players("players.txt")
        manager.print_schedule()
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
