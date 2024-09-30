from os import getenv
from app import app
from flask import Flask
from flask import redirect, render_template, request, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from database_handler import (
    get_user_by_username,
    create_user,
    check_if_username_exists,
    get_team_by_user_id,
    get_all_teams,
    set_user_team,
    create_new_team,
    get_all_players,
    get_batter_by_team_id,
    get_pitcher_by_team_id,
    get_fielder_by_team_id,
    get_player_by_id,
    get_all_players_by_team_id,
)


@app.route("/")
def index():
    if "username" not in session:
        return render_template("index.html")

    # Get user info from session
    username = session["username"]
    user = get_user_by_username(username)

    # Get the user's current team
    current_team = get_team_by_user_id(user.id)
    if current_team:
        current_batter = get_batter_by_team_id(current_team.id)
        current_pitcher = get_pitcher_by_team_id(current_team.id)
        current_fielder = get_fielder_by_team_id(current_team.id)

        # Pass the current team and players to the template
        return render_template(
            "index.html",
            current_team=current_team,
            current_batter=current_batter,
            current_pitcher=current_pitcher,
            current_fielder=current_fielder,
        )
    return render_template("index.html", current_team=current_team)


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


@app.route("/choose_team", methods=["GET", "POST"])
def choose_team():
    if request.method == "POST":
        # Save the selected team to the user's profile
        if "username" not in session:
            flash("You need to be logged in to select a team.")
            return redirect("/")

        # Get the selected team ID from the form
        team_id = request.form.get("team_id")

        if not team_id:
            flash("Please select a valid team.")
            return redirect("/choose_team")

        # Get the user from the session
        username = session["username"]

        # Update the user's current team in the database
        set_user_team(username, team_id)

        # Redirect to the homepage after team selection
        flash("Team successfully selected.")
        return redirect("/")

    # GET request: Show the team selection form
    teams = get_all_teams()
    return render_template("choose_team.html", teams=teams)


@app.route("/create_team", methods=["GET", "POST"])
def create_team():

    if "username" not in session:
        flash("You need to be logged in to create a team.")
        return redirect("/")

    if request.method == "GET":
        # Render the form to create a new team
        players = get_all_players()
        return render_template("create_team.html", players=players)

    if request.method == "POST":
        # Get the team details and selected players from the form
        team_name = request.form.get("team_name")
        location = request.form.get("location")
        batter_id = request.form.get("batter_id")
        pitcher_id = request.form.get("pitcher_id")
        fielder_id = request.form.get("fielder_id")

        if (
            not team_name
            or not location
            or not batter_id
            or not pitcher_id
            or not fielder_id
        ):
            flash("All fields are required.")
            return redirect("/choose_team")

        # Create the team in the database
        create_new_team(
            team_name, location, batter_id, pitcher_id, fielder_id, session["username"]
        )

        flash("Team created successfully!")
        return redirect("/choose_team")


@app.route("/player/<int:player_id>")
def player_stats(player_id):
    """
    View the statistics of a player by their player ID.
    """
    player = get_player_by_id(player_id)

    if player is None:
        return (
            "Player not found",
            404,
        )  # Handle the case where the player does not exist

    # Render the player stats template
    return render_template("player_stats.html", player=player)
