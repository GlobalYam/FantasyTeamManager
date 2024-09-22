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
