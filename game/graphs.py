import matplotlib.pyplot as plt
import sqlite3
import pandas as pd


def plot_elo_progression():
    conn = sqlite3.connect("game/game_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT player_id, games_played, starting_elo, elo_change
        FROM game_results
        WHERE games_played BETWEEN 1 AND 15
        ORDER BY player_id, games_played
    """)
    results = cursor.fetchall()
    conn.close()

    players = {}
    for player_id, games_played, starting_elo, elo_change in results:
        new_score = starting_elo + elo_change
        if player_id not in players:
            players[player_id] = {"games": [], "elo": []}
        players[player_id]["games"].append(games_played)
        players[player_id]["elo"].append(new_score)

    plt.figure(figsize=(10, 6))
    for player_id, data in players.items():
        if len(data["games"]) > 1:
            plt.plot(data["games"], data["elo"], marker='o', linestyle='-', label=f"Player {player_id}")

    plt.xlabel("Games Played")
    plt.ylabel("Score")
    plt.xticks(range(1, 16))
    plt.legend(title="Player ID", fontsize="small")
    plt.grid(True)
    plt.show()


def plot_playstyles():
    conn = sqlite3.connect("game/game_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, wins, losses, folds, all_ins, raises
        FROM player_stats
    """)
    data = cursor.fetchall()
    conn.close()

    df = pd.DataFrame(data, columns=["Player ID", "Wins", "Losses", "Folds", "All-ins", "Raises"])

    df["Games Played"] = df["Wins"] + df["Losses"]

    def categorize_playstyle(row):    
        if row["Folds"] > row["Raises"] and row["Folds"] > row["All-ins"]:
            return "Safe"
        elif row["Raises"] > row["Folds"] and row["All-ins"] > row["Raises"]:
            return "Risky"
        else:
            return "Neutral"

    df["Playstyle"] = df.apply(categorize_playstyle, axis=1)

    df["Win %"] = (df["Wins"] / df["Games Played"]) * 100

    playstyle_stats = df.groupby("Playstyle").agg(average_win_pct=("Win %", "mean"), player_count=("Player ID", "count"))

    playstyle_labels = [f"{playstyle} ({count})" for playstyle, count in playstyle_stats["player_count"].items()]

    plt.figure(figsize=(6, 4))

    ax = playstyle_stats["average_win_pct"].plot(kind="bar", color=["blue", "red", "green"])
    ax.set_xticklabels(playstyle_labels, rotation=0)

    plt.xlabel("Playstyle")
    plt.ylabel("Win %")

    plt.grid(axis="y", linestyle="--")
    plt.show()

def plot_winrate_progression():
    conn = sqlite3.connect("game/game_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT player_id, result
        FROM game_results
        ORDER BY id
    """)
    game_results = cursor.fetchall()
    conn.close()

    players = {}

    for player_id, result in game_results:
        if player_id not in players:
            players[player_id] = {"wins": 0, "losses": 0, "games": []}
        if result == "win":
            players[player_id]["wins"] += 1
        elif result == "loss":
            players[player_id]["losses"] += 1

        total_games = players[player_id]["wins"] + players[player_id]["losses"]
        winrate = (players[player_id]["wins"] / total_games) * 100 if total_games > 0 else 0
        players[player_id]["games"].append(winrate)

    global_games = []
    global_winrate = []
    max_games = 15

    for game_num in range(1, max_games + 1):
        total_wins = 0
        total_players = 0

        for player_id, data in players.items():
            if game_num <= len(data["games"]):
                total_wins += data["games"][game_num - 1]
                total_players += 1

        if total_players > 0:
            global_games.append(game_num)
            global_winrate.append(total_wins / total_players)

    plt.figure(figsize=(10, 6))
    plt.plot(global_games, global_winrate, marker='o', linestyle='-', color='purple')
    plt.xlabel("Games Played")
    plt.ylabel("Win Rate (%)")
    plt.xticks(range(1, max_games + 1))
    plt.grid(True)
    plt.show()

    
def plot_win_rate_per_difficulty():
    conn = sqlite3.connect("game/game_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT starting_elo, result
        FROM game_results
        WHERE starting_elo >= 25
    """)
    game_results = cursor.fetchall()
    conn.close()

    game_results_with_difficulty = [
    (('Easy' if starting_elo < 100 else 'Medium' if 100 <= starting_elo < 200 else 'Hard'), result) 
    for starting_elo, result in game_results
    ]


    df = pd.DataFrame(game_results_with_difficulty, columns=["Difficulty", "Result"])

    win_rates = df.groupby("Difficulty")["Result"].value_counts(normalize=True).unstack(fill_value=0)

    win_rates["win_rate"] = win_rates["win"] * 100

    difficulty_order = ["Easy", "Medium", "Hard"]
    win_rates = win_rates.loc[difficulty_order]

    difficulty_counts = df["Difficulty"].value_counts()

    difficulty_labels = [f"{difficulty} ({difficulty_counts[difficulty]})" for difficulty in difficulty_order]

    colors = {"Easy": "green", "Medium": "orange", "Hard": "red"}

    plt.figure(figsize=(8, 5))
    win_rates["win_rate"].plot(kind="bar", color=[colors[difficulty] for difficulty in win_rates.index])
    plt.xticks(range(len(difficulty_labels)), difficulty_labels, rotation=0)
    plt.xlabel("Difficulty (Games Played)")
    plt.ylabel("Win Rate (%)")
    plt.grid(axis="y")
    plt.show()


plot_elo_progression()
plot_playstyles()
plot_winrate_progression()
plot_win_rate_per_difficulty()
