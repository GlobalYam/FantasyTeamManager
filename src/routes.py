from os import getenv
from app import app
from flask import Flask
from flask import redirect, render_template, request, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from database_handler import (
    get_user_by_username,
    create_user,
    check_if_username_exists,
)  # Assuming helper functions are in a file named db_helpers.py


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    # Call the helper function to get the user data
    user = get_user_by_username(username)

    if not user:
        # Invalid username
        flash("Invalid username.")
        return redirect("/")
    else:
        # Verify the password
        hash_value = user.password
        if check_password_hash(hash_value, password):
            # Correct username and password
            session["username"] = username
            flash("Login successful.")
            return redirect("/")
        else:
            # Invalid password
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

        # Call the helper function to check if the username already exists
        if check_if_username_exists(username):
            flash("Username already taken.")
            return redirect("/register")

        # Hash the password and call the helper function to create the user
        hash_value = generate_password_hash(password)
        create_user(username, hash_value)

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
