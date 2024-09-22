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
