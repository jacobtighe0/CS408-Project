import sqlite3
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
# Saves the database and text files in the same directory as this file
database = os.path.join(current_directory, "game_data.db")
player_stats_file = os.path.join(current_directory, "player_stats.txt")
game_results_file = os.path.join(current_directory, "game_results.txt")

def initialise_db():
    # Connect to (or create) the database file
    conn = sqlite3.connect(database)  # Saves locally in the game folder
    cursor = conn.cursor()

    # Enable foreign key support in SQLite
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Create a table for player statistics if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS player_stats (
            name TEXT PRIMARY KEY,
            wins INTEGER DEFAULT 0,
            losses INTEGER DEFAULT 0,
            checks INTEGER DEFAULT 0,
            calls INTEGER DEFAULT 0,
            raises INTEGER DEFAULT 0,
            folds INTEGER DEFAULT 0,
            all_ins INTEGER DEFAULT 0,
            total_actions INTEGER DEFAULT 0,
            elo INTEGER DEFAULT 0,
            initial_difficulty TEXT,
            win_streak INTEGER DEFAULT 0
        )
    ''')

    # Create a table for game results if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS game_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT,
            games_played INTEGER DEFAULT 0,
            result TEXT CHECK(result IN ('win', 'loss')),
            elo_change INTEGER,
            FOREIGN KEY (player_name) REFERENCES player_stats(name)
        )
    ''')

    conn.commit()  # Save changes
    conn.close()   # Close connection

def add_initial_difficulty(name, difficulty, elo):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    # Check if the player exists
    cursor.execute("SELECT * FROM player_stats WHERE name = ?", (name,))
    player = cursor.fetchone()
        
    if player:
        cursor.execute("UPDATE player_stats SET initial_difficulty = ?, elo = ? WHERE name = ?", (difficulty, elo, name))
    else:
        cursor.execute("INSERT INTO player_stats (name, initial_difficulty, elo) VALUES (?, ?, ?)", (name, difficulty, elo))

    conn.commit()
    conn.close()

def update_player_wins(name, win, elo):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    # Check if the player exists
    cursor.execute("SELECT * FROM player_stats WHERE name = ?", (name,))
    player = cursor.fetchone()

    # If player has a win streak, scale Elo accordingly
    cursor.execute("SELECT win_streak FROM player_stats WHERE name = ?", (name,))
    x = cursor.fetchone()
    win_streak = x[0] if x else 0
    elo_change = elo * (win_streak + 1)

    if player:
        # Update existing player's stats
        if win:
            cursor.execute("UPDATE player_stats SET wins = wins + 1, win_streak = win_streak + 1, elo = elo + ? WHERE name = ?", (elo_change, name))
        else:
            cursor.execute("UPDATE player_stats SET losses = losses + 1, win_streak = 0, elo = elo + ? WHERE name = ?", (elo, name,))

        # Insert into game_results
        cursor.execute("INSERT INTO game_results (player_name, games_played, result, elo_change) VALUES (?, ?, ?, ?)",
            (name, (player[1]+player[2])+1, 'win' if win else 'loss', elo_change if win else elo))
        # Update games_played by 1 and add the result to the game_results table
        #cursor.execute("UPDATE game_results SET games_played = games_played + 1 WHERE player_name = ?", (name,))
    else:
        # Create new player record
        cursor.execute("INSERT INTO player_stats (name, wins, losses) VALUES (?, ?, ?)",
                       (name, 1 if win else 0, 0 if win else 1))

    conn.commit()
    conn.close()

def update_player_action(name, action):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    # Check if the player exists
    cursor.execute("SELECT * FROM player_stats WHERE name = ?", (name,))
    player = cursor.fetchone()

    if player:
        # Update existing player's stats
        if action == 1:
            cursor.execute("UPDATE player_stats SET checks = checks + 1 WHERE name = ?", (name,))
        elif action == 2:
            cursor.execute("UPDATE player_stats SET calls = calls + 1 WHERE name = ?", (name,))
        elif action == 3:
            cursor.execute("UPDATE player_stats SET raises = raises + 1 WHERE name = ?", (name,))
        elif action == 4:
            cursor.execute("UPDATE player_stats SET folds = folds + 1 WHERE name = ?", (name,))
        elif action == 5:
            cursor.execute("UPDATE player_stats SET all_ins = all_ins + 1 WHERE name = ?", (name,))

        cursor.execute("UPDATE player_stats SET total_actions = total_actions + 1 WHERE name = ?", (name,))
    else:
        # Create new player record
        cursor.execute("INSERT INTO player_stats (name, checks, calls, raises, folds, all_ins, total_actions) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (name, 1 if action == 1 else 0, 1 if action == 2 else 0, 1 if action == 3 else 0, 1 if action == 4 else 0, 1 if action == 5 else 0, 1))

    conn.commit()
    conn.close()

def get_player_stats(name):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM player_stats WHERE name = ?", (name,))
    player = cursor.fetchone()
    
    conn.close()
    return player

def get_game_results(name):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM game_results WHERE player_name = ?", (name,))
    player = cursor.fetchall()
    
    conn.close()
    return player

def write_player_stats():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    # Fetch all player statistics
    cursor.execute("SELECT * FROM player_stats ORDER BY name")
    player_stats = cursor.fetchall()

    # Open a text file for writing (or create it if it doesn't exist)
    with open(player_stats_file, "w") as file:
        if player_stats:
            file.write(f"{'Name':<10}{'Wins':<6}{'Losses':<8}{'Checks':<8}{'Calls':<8}{'Raises':<8}{'Folds':<8}{'All-ins':<10}{'Total actions':<15}{'Elo':<6}{'Initial difficulty':<20}{'Win Streak'}\n")
            # Write each player's statistics
            for player in player_stats:
                file.write(f"{player[0]:<10}{player[1]:<6}{player[2]:<8}{player[3]:<8}{player[4]:<8}{player[5]:<8}{player[6]:<8}{player[7]:<10}{player[8]:<15}{player[9]:<6}{player[10]:<20}{player[11]}\n")
        else:
            file.write("No player statistics found.\n")

    conn.close()
    
def write_game_results():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    # Fetch all game results for the player
    cursor.execute("SELECT * FROM game_results ORDER BY player_name")
    game_results = cursor.fetchall()

    # Open a text file for writing (or create it if it doesn't exist)
    with open(game_results_file, "w") as file:
        if game_results:
            file.write(f"{'ID':<5}{'Name':<10}{'Played':<8}{'Result':<8}{'Elo change'}\n")
            # Write each game result (ID, Player name, Result, Elo change)
            for result in game_results:
                file.write(f"{result[0]:<5}{result[1]:<10}{result[2]:<8}{result[3]:<8}{result[4]}\n")
        else:
            file.write("No game results found.\n")

    conn.close()

