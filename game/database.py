import sqlite3

def initialise_db():
    # Connect to (or create) the database file
    conn = sqlite3.connect("game_data.db")  # Saves locally in the game folder
    cursor = conn.cursor()

    # Create a table for player statistics if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS player_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            wins INTEGER DEFAULT 0,
            losses INTEGER DEFAULT 0
        )
    ''')

    conn.commit()  # Save changes
    conn.close()   # Close connection

def update_player_stats(name, win):
    conn = sqlite3.connect("game_data.db")
    cursor = conn.cursor()

    # Check if the player exists
    cursor.execute("SELECT * FROM player_stats WHERE name = ?", (name,))
    player = cursor.fetchone()

    if player:
        # Update existing player's stats
        if win:
            cursor.execute("UPDATE player_stats SET wins = wins + 1 WHERE name = ?", (name,))
        else:
            cursor.execute("UPDATE player_stats SET losses = losses + 1 WHERE name = ?", (name,))
    else:
        # Create new player record
        cursor.execute("INSERT INTO player_stats (name, wins, losses) VALUES (?, ?, ?)",
                       (name, 1 if win else 0, 0 if win else 1))

    conn.commit()
    conn.close()

def get_player_stats(name):
    conn = sqlite3.connect("game_data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM player_stats WHERE name = ?", (name,))
    player = cursor.fetchone()
    
    conn.close()
    return player  # Returns (id, name, wins, losses, money) or None


