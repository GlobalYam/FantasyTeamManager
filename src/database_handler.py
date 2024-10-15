from sqlalchemy.sql import text
from db import db
from datetime import datetime


def get_user_by_username(username):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    return result.fetchone()


def create_user(username, hashed_password):
    sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
    db.session.execute(sql, {"username": username, "password": hashed_password})
    db.session.commit()


def check_if_username_exists(username):
    sql = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    return result.fetchone()


def get_team_name_by_id(team_id):
    sql = text("SELECT name FROM teams WHERE id = :team_id")
    result = db.session.execute(sql, {"team_id": team_id}).fetchone()
    if result:
        return result.name
    return None


def get_team_by_user_id(user_id):
    # get the team of the user based on current_team in users table
    sql = text(
        """
        SELECT teams.id, teams.name, teams.location 
        FROM teams 
        JOIN users ON users.current_team = teams.id 
        WHERE users.id = :user_id
    """
    )
    result = db.session.execute(sql, {"user_id": user_id})
    return result.fetchone()  # Return None if no team is found


# Get all available teams
def get_all_teams():
    sql = text("SELECT id, name, location FROM teams")
    result = db.session.execute(sql)
    return result.fetchall()


def get_all_teams_owned_by_user_id(user_id):
    """
    Fetch all teams owned by a specific user by user ID.
    """
    sql = text(
        """
        SELECT id, name, location 
        FROM teams 
        WHERE owner = :user_id
        """
    )
    return db.session.execute(sql, {"user_id": user_id}).fetchall()


def get_player_by_id(player_id):
    """
    Fetch player statistics by player ID.
    """
    sql = text(
        """
        SELECT 
            id, name, power, accuracy, speed, volatility, luck,
            hit_average, strikeout_average, out_average, 
            mvps, games, wins, losses, games_tied 
        FROM players
        WHERE id = :player_id
        """
    )
    return db.session.execute(sql, {"player_id": player_id}).fetchone()


def get_all_players_by_team_id(team_id):
    """
    Fetch all players belonging to a specific team by team ID.
    """
    sql = text(
        """
        SELECT players.id, players.name 
        FROM players
        JOIN teams ON teams.batter = players.id OR teams.pitcher = players.id OR teams.catcher = players.id
        WHERE teams.id = :team_id
        """
    )
    return db.session.execute(sql, {"team_id": team_id}).fetchall()


# Set the user's current team
def set_user_team(username, team_id):
    sql = text("UPDATE users SET current_team=:team_id WHERE username=:username")
    db.session.execute(sql, {"team_id": team_id, "username": username})
    db.session.commit()


def create_new_team(name, location, batter_id, pitcher_id, fielder_id, username):
    user = get_user_by_username(username)

    if user:
        user_id = user.id
        # Insert the new team with player roles
        team_sql = text(
            "INSERT INTO teams (name, owner, location, batter, pitcher, catcher) VALUES (:name, :owner, :location, :batter, :pitcher, :fielder)"
        )
        db.session.execute(
            team_sql,
            {
                "name": name,
                "owner": user_id,
                "location": location,
                "batter": batter_id,
                "pitcher": pitcher_id,
                "fielder": fielder_id,
            },
        )
        db.session.commit()


def get_all_players():
    # Get all players, pretty self explanatory
    players_sql = text("SELECT id, name FROM players")
    players_result = db.session.execute(players_sql)
    return players_result.fetchall()


def get_all_free_players():
    # Get all players not in teams
    players_sql = text(
        "SELECT id, name FROM players WHERE id NOT IN (SELECT batter FROM teams) AND id NOT IN (SELECT pitcher FROM teams) AND id NOT IN (SELECT catcher FROM teams)"
    )
    players_result = db.session.execute(players_sql)
    return players_result.fetchall()


def get_batter_by_team_id(team_id):
    """
    Fetch the batter of a given team by team ID.
    """
    # First, check if the team exists and has a batter set
    team_sql = text(
        """
        SELECT batter FROM teams WHERE id = :team_id
        """
    )
    team_result = db.session.execute(team_sql, {"team_id": team_id}).fetchone()

    if not team_result or team_result.batter == 0:
        # If no team or no batter is set, return None
        print(f"Team {team_id} either does not exist or has no batter set.")
        return None

    # Query to get the batter's details from the players table
    player_sql = text(
        """
        SELECT id, name 
        FROM players
        WHERE id = :batter_id
        """
    )

    # Fetch the batter's details
    player_result = db.session.execute(
        player_sql, {"batter_id": team_result.batter}
    ).fetchone()

    if not player_result:
        print(f"No player found with id {team_result.batter}.")
    return player_result


def get_player_batting_stats(player_id):
    """
    Fetch batting average of a player from games where they were the batter.
    """
    sql = text(
        """
        SELECT 
            COUNT(*) AS games_played, 
            SUM(home_points) + SUM(visiting_points) AS total_runs, 
            SUM(home_hits) + SUM(visiting_hits) AS total_hits, 
            SUM(home_outs) + SUM(visiting_outs) AS total_outs
        FROM games
        WHERE home_batter = :player_id OR visiting_batter = :player_id
        """
    )
    result = db.session.execute(sql, {"player_id": player_id}).fetchone()
    if result.games_played == 0:
        return {"batting_average": 0}
    return {
        "batting_average": result.total_hits / (result.total_hits + result.total_outs)
    }


def get_player_pitching_stats(player_id):
    """
    Fetch pitching average of a player from games where they were the pitcher.
    """
    sql = text(
        """
        SELECT 
            COUNT(*) AS games_played, 
            SUM(home_points) + SUM(visiting_points) AS total_runs, 
            SUM(home_hits) + SUM(visiting_hits) AS total_hits, 
            SUM(home_strikeouts) + SUM(visiting_strikeouts) AS total_strikeouts
        FROM games
        WHERE home_pitcher = :player_id OR visiting_pitcher = :player_id
        """
    )
    result = db.session.execute(sql, {"player_id": player_id}).fetchone()
    if result.games_played == 0:
        return {"pitching_average": 0}
    return {
        "pitching_average": result.total_strikeouts
        / (result.total_hits + result.total_strikeouts)
    }


def get_player_fielding_stats(player_id):
    """
    Fetch fielding average of a player from games where they were the fielder.
    """
    sql = text(
        """
        SELECT 
            COUNT(*) AS games_played, 
            SUM(home_points) + SUM(visiting_points) AS total_runs, 
            SUM(home_hits) + SUM(visiting_hits) AS total_hits, 
            SUM(home_outs) + SUM(visiting_outs) AS total_outs
        FROM games
        WHERE home_fielder = :player_id OR visiting_fielder = :player_id
        """
    )
    result = db.session.execute(sql, {"player_id": player_id}).fetchone()
    if result.games_played == 0:
        return {"fielding_average": 0}
    return {
        "fielding_average": result.total_hits / (result.total_hits + result.total_outs)
    }


def get_pitcher_by_team_id(team_id):
    """
    Fetch the pitcher of a given team by team ID.
    """
    # First, check if the team exists and has a pitcher set
    team_sql = text(
        """
        SELECT pitcher FROM teams WHERE id = :team_id
        """
    )
    team_result = db.session.execute(team_sql, {"team_id": team_id}).fetchone()

    if not team_result or team_result.pitcher == 0:
        # If no team or no pitcher is set, return None
        print(f"Team {team_id} either does not exist or has no pitcher set.")
        return None

    # Query to get the pitcher's details from the players table
    player_sql = text(
        """
        SELECT id, name 
        FROM players
        WHERE id = :pitcher_id
        """
    )

    # Fetch the pitcher's details
    player_result = db.session.execute(
        player_sql, {"pitcher_id": team_result.pitcher}
    ).fetchone()

    if not player_result:
        print(f"No player found with id {team_result.pitcher}.")
    return player_result


def get_team_stats_by_team_id(team_id):
    """
    Fetch team statistics by team ID.
    """
    sql = text(
        """
        SELECT 
            wins, losses, games_tied AS ties
        FROM teams
        WHERE id = :team_id
        """
    )
    result = db.session.execute(sql, {"team_id": team_id}).fetchone()
    if result:
        return {"wins": result.wins, "losses": result.losses, "ties": result.ties}
    return {"wins": 0, "losses": 0, "ties": 0}


def get_all_other_users(exclude_user_id):
    """
    Fetch all other users, returning their ID, name, and current team ID and name.
    """
    sql = text(
        """
        SELECT 
            users.id AS user_id, 
            users.username, 
            users.current_team,
            teams.name AS team_name
        FROM users
        LEFT JOIN teams ON users.current_team = teams.id
        WHERE users.id != :exclude_user_id
        """
    )
    result = db.session.execute(sql, {"exclude_user_id": exclude_user_id}).fetchall()
    return [
        {
            "user_id": row.user_id,
            "username": row.username,
            "current_team": row.current_team,
            "team_name": row.team_name,
        }
        for row in result
    ]


def get_fielder_by_team_id(team_id):
    """
    Fetch the fielder of a given team by team ID.
    """
    # First, check if the team exists and has a fielder set
    team_sql = text(
        """
        SELECT catcher FROM teams WHERE id = :team_id
        """
    )
    team_result = db.session.execute(team_sql, {"team_id": team_id}).fetchone()

    if not team_result or team_result.catcher == 0:
        # If no team or no fielder is set, return None
        print(f"Team {team_id} either does not exist or has no fielder set.")
        return None

    # Query to get the fielder's details from the players table
    player_sql = text(
        """
        SELECT id, name 
        FROM players
        WHERE id = :fielder_id
        """
    )

    # Fetch the fielder's details
    player_result = db.session.execute(
        player_sql, {"fielder_id": team_result.catcher}
    ).fetchone()

    if not player_result:
        print(f"No player found with id {team_result.catcher}.")
    return player_result


def create_match(challenger_id, challenged_id, results):
    """
    Create a new match between two teams.
    """
    home_hits = results["home_hits"]
    visiting_hits = results["visiting_hits"]
    home_strikeouts = results["home_strikeouts"]
    visiting_strikeouts = results["visiting_strikeouts"]
    home_outs = results["home_outs"]
    visiting_outs = results["visiting_outs"]
    home_points = results["home_points"]
    visiting_points = results["visiting_points"]
    mvp = results["mvp"]
    winner = results["winner"]

    # Get the players' IDs
    visiting_batter = get_batter_by_team_id(challenger_id)[0]
    visiting_pitcher = get_pitcher_by_team_id(challenger_id)[0]
    visiting_fielder = get_fielder_by_team_id(challenger_id)[0]

    home_batter = get_batter_by_team_id(challenged_id)[0]
    home_pitcher = get_pitcher_by_team_id(challenged_id)[0]
    home_fielder = get_fielder_by_team_id(challenged_id)[0]

    date = datetime.now()

    sql = text(  # Insert the match into the database
        """
        INSERT INTO games (
            home_team, home_batter, home_pitcher, home_fielder,
            visiting_team, visiting_batter, visiting_pitcher, visiting_fielder,
            home_hits, visiting_hits,
            home_strikeouts, visiting_strikeouts,
            home_outs, visiting_outs,
            home_points, visiting_points,
            mvp, winner, date
        ) VALUES (
            :home_team, :home_batter, :home_pitcher, :home_fielder,
            :visiting_team, :visiting_batter, :visiting_pitcher, :visiting_fielder,
            :home_hits, :visiting_hits,
            :home_strikeouts, :visiting_strikeouts,
            :home_outs, :visiting_outs,
            :home_points, :visiting_points,
            :mvp, :winner, :date
        )
        """
    )
    db.session.execute(
        sql,
        {
            "home_team": challenger_id,
            "home_batter": home_batter,
            "home_pitcher": home_pitcher,
            "home_fielder": home_fielder,
            "visiting_team": challenged_id,
            "visiting_batter": visiting_batter,
            "visiting_pitcher": visiting_pitcher,
            "visiting_fielder": visiting_fielder,
            "home_hits": home_hits,
            "visiting_hits": visiting_hits,
            "home_strikeouts": home_strikeouts,
            "visiting_strikeouts": visiting_strikeouts,
            "home_outs": home_outs,
            "visiting_outs": visiting_outs,
            "home_points": home_points,
            "visiting_points": visiting_points,
            "mvp": mvp,
            "winner": winner,
            "date": date,
        },
    )

    db.session.commit()

    # Update the teams' stats
    if winner == challenger_id:
        # Challenger won
        sql = text(
            """
            UPDATE teams
            SET wins = wins + 1
            WHERE id = :team_id
            """
        )
        db.session.execute(sql, {"team_id": challenger_id})
        sql = text(
            """
            UPDATE teams
            SET losses = losses + 1
            WHERE id = :team_id
            """
        )
        db.session.execute(sql, {"team_id": challenged_id})
    elif winner == challenged_id:
        # Challenged team won
        sql = text(
            """
            UPDATE teams
            SET wins = wins + 1
            WHERE id = :team_id
            """
        )
        db.session.execute(sql, {"team_id": challenged_id})
        sql = text(
            """
            UPDATE teams
            SET losses = losses + 1
            WHERE id = :team_id
            """
        )
        db.session.execute(sql, {"team_id": challenger_id})
    else:
        # Tie
        sql = text(
            """
            UPDATE teams
            SET games_tied = games_tied + 1
            WHERE id = :team_id
            """
        )
        db.session.execute(sql, {"team_id": challenger_id})
        db.session.execute(sql, {"team_id": challenged_id})
    db.session.commit()
