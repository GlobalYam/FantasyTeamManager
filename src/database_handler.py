from sqlalchemy.sql import text
from db import db


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


def get_player_by_id(player_id):
    """
    Fetch player statistics by player ID.
    """
    sql = text(
        """
        SELECT 
            id, name, power, accuracy, speed, 
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
