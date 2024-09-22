from os import getenv
from app import app
from flask import Flask
from flask import redirect, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from db import db


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    # check username and password
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        # invalid username
        flash("Invalid username.")
        return redirect("/")
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            # correct username and password
            session["username"] = username
            flash("Login successful.")
            return redirect("/")
        else:
            # invalid password
            flash("Invalid password.")
            return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check if both fields are filled
        if not username or not password:
            flash("Username and password are required.")
            return redirect("/register")

        # Check if the username already exists
        sql = text("SELECT id FROM users WHERE username=:username")
        result = db.session.execute(sql, {"username": username})
        if result.fetchone():
            flash("Username already taken.")
            return redirect("/register")

        # Hash the password and insert the new user into the database
        hash_value = generate_password_hash(password)
        sql = text(
            "INSERT INTO users (username, password) VALUES (:username, :password)"
        )
        db.session.execute(sql, {"username": username, "password": hash_value})
        db.session.commit()

        # Automatically log in the user after registration
        session["username"] = username
        flash("Account created and logged in.")
        return redirect("/")

    # Render the registration form
    return render_template("register.html")


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")
