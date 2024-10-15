import random


def resolve_match(home_team_players, home_team, visiting_team_players, visiting_team):
    # returns the winning team and

    home_batter, home_pitcher, home_fielder = home_team_players
    visiting_batter, visiting_pitcher, visiting_fielder = visiting_team_players

    # print(
    #     f"home_batter: {home_batter}, home_pitcher: {home_pitcher}, home_fielder: {home_fielder}"
    # )
    # print()
    # print(
    #     f"visiting_batter: {visiting_batter}, visiting_pitcher: {visiting_pitcher}, visiting_fielder: {visiting_fielder}"
    # )

    # STATS
    home_hits = 0  # "home_batter's hit_calc function"
    visiting_hits = 0  # "visiting_batter's hit_calc function"

    home_strikeouts = 0  # "home_pitcher's strikeout_calc function"
    visiting_strikeouts = 0  # "visiting_pitcher's strikeout_calc function"

    home_outs = 0  # "home_fielder's out_calc function"
    visiting_outs = 0  # "visiting_fielder's out_calc function"

    home_points = 0  # "home_team's points"
    visiting_points = 0  # "visiting_team's points"

    mvp = None  # "Player with the highest score in the game"
    winner = None  # "The winning team"

    # ROUNDS
    for round_num in range(1, 4):
        home_team_result, home_team_runs = round(
            home_team_players, visiting_team_players
        )
        home_points += home_team_runs

        match home_team_result:
            case "Out-Of-Park-Home-Run":
                home_hits += 1
            case "Home-Run":
                home_hits += 1
            case "Hit":
                home_hits += 1
            case "Strike-Out":
                visiting_strikeouts += 1
            case "Catch":
                visiting_outs += 1
            case "Out":
                visiting_outs += 1

    for round_num in range(1, 4):
        visiting_team_result, visiting_team_runs = round(
            home_team_players, visiting_team_players
        )
        visiting_points += visiting_team_runs

        match visiting_team_result:
            case "Out-Of-Park-Home-Run":
                visiting_hits += 1
            case "Home-Run":
                visiting_hits += 1
            case "Hit":
                visiting_hits += 1
            case "Strike-Out":
                home_strikeouts += 1
            case "Catch":
                home_outs += 1
            case "Out":
                home_outs += 1

    if home_points > visiting_points:
        winner = home_team
    else:
        winner = visiting_team

    match_results = {
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
    }

    return match_results


def round(batting_team, fielding_team):
    # returns the result of a round as a tuple, (result, runs)
    batter = batting_team[0]
    pitcher = fielding_team[1]
    fielder = fielding_team[2]

    exit_velocity, hit_accuracy = pitcher_vs_batter(pitcher, batter)

    if exit_velocity == 0:
        # if the batter strikes out, the round ends
        return "Strike-Out", 0

    if exit_velocity > 15 and hit_accuracy > 7:
        # if the batter hits a home run, the round ends
        return "Out-Of-Park-Home-Run", 1

    runs, catch = runners_vs_fielder(batting_team, fielder, exit_velocity, hit_accuracy)

    if catch:
        return "Catch", 0
    if runs == 3:
        return "Home-Run", runs
    if runs > 0:
        return "Hit", runs
    else:
        return "Out", 0


def pitcher_vs_batter(pitcher, batter):
    # returns the result of a pitching round
    ball_speed, pitch_accuracy = simulate_pitch(pitcher)
    exit_velocity, hit_accuracy = simulate_batting(batter, ball_speed, pitch_accuracy)

    return exit_velocity, hit_accuracy


def runners_vs_fielder(runners, fielder, exit_velocity, hit_accuracy):
    # returns the result of a fielding round
    return_time = simulate_fielding(fielder, exit_velocity, hit_accuracy)

    # If return time is 0, the fielder has caught the ball
    if return_time == 0:
        return 0, True

    runs = 0
    total_runners = len(runners)
    time_per_next_run = simulate_run_time(runners[total_runners - 1])

    while time_per_next_run < return_time:
        runs += 1
        return_time -= time_per_next_run

        # if all runners have scored, the round ends
        if runs == total_runners:
            return runs, False

        time_per_next_run = simulate_run_time(runners[total_runners - 1 - runs])

    return runs, False


def simulate_run_time(player):
    # returns the time it takes for a runner to run to the next base
    runner_speed = player_speed(player)
    runner_volatility = player_volatility(player)
    runner_luck = player_luck(player)

    volatility = calculate_volatility(runner_volatility, runner_luck)

    run_time = runner_speed + volatility * runner_speed

    return run_time


def simulate_fielding(fielder, exit_velocity, hit_accuracy):
    # returns the amount of time it takes for the fielder to catch and return the ball
    fielding_speed = get_raw_fielding_speed(fielder)
    fielding_accuracy = get_raw_fielding_accuracy(fielder)

    speed_diff = fielding_speed - exit_velocity
    speed_modifer = speed_diff / 2 if abs(speed_diff) > 2 else speed_diff / 4

    if fielding_accuracy > hit_accuracy:
        # if the fielder has high accuracy, the fielder will have a chance to catch the ball
        if speed_diff > -2:
            return 0

    return_time = (
        (exit_velocity + hit_accuracy / 2)
        - (fielding_speed + hit_accuracy) / 2
        + speed_modifer
    )

    # the ball has to be fetched and returned to the pitcher
    return return_time * 2


def get_raw_fielding_speed(fielder):
    # returns randomized fielding score
    fielder_strength = player_strength(fielder)
    fielder_accuracy = player_accuracy(fielder)
    fielder_speed = player_speed(fielder)
    fielder_volatility = player_volatility(fielder)
    fielder_luck = player_luck(fielder)

    volatility = calculate_volatility(fielder_volatility, fielder_luck)

    fielding_speed = fielder_speed + volatility * fielder_speed

    return fielding_speed


def get_raw_fielding_accuracy(fielder):
    # returns randomized fielding score
    fielder_strength = player_strength(fielder)
    fielder_accuracy = player_accuracy(fielder)
    fielder_speed = player_speed(fielder)
    fielder_volatility = player_volatility(fielder)
    fielder_luck = player_luck(fielder)

    volatility = calculate_volatility(fielder_volatility, fielder_luck)

    fielding_accuracy = fielder_accuracy + volatility * fielder_accuracy

    return fielding_accuracy


def simulate_batting(batter, ball_speed, ball_accuracy):
    # returns the result of a batting round
    bat_speed = get_raw_batting_speed(batter)

    # Bat_Speed vs ball_speed
    speed_diff = bat_speed - ball_speed

    bat_accuracy = get_raw_batting_accuracy(batter, speed_diff)

    # set hit_power and exit velocity to be 0 by default
    hit_power = 0
    exit_velocity = 0

    accuracy_diff = bat_accuracy - ball_accuracy

    if accuracy_diff < -2:
        # if the accuracy difference is too large, the batter will strike out
        accuracy_mod = 0
    elif accuracy_diff < 0:
        # if the accuracy difference is negative, the exit velocity will be reduced
        accuracy_mod = 0.5
    elif accuracy_diff < 6:
        # if the accuracy difference is positive, the exit velocity will be increased
        accuracy_mod = 1 + accuracy_diff / 10
    else:
        # if the accuracy difference is too large, the exit velocity will be doubled
        accuracy_mod = 2

    hit_power = get_raw_batting_power(batter, bat_speed)
    raw_exit_velocity = calculate_exit_velocity(bat_speed, ball_speed)
    exit_velocity = (hit_power + raw_exit_velocity / 2) * accuracy_mod

    return exit_velocity, bat_accuracy


def calculate_exit_velocity(bat_speed, ball_speed, bat_mass=5, ball_mass=1):
    # returns the exit velocity of the ball
    return (bat_mass * bat_speed + ball_mass * ball_speed) / (bat_mass + ball_mass)


def get_raw_batting_speed(batter):
    # returns randomized batting score
    batter_strength = player_strength(batter)
    batter_accuracy = player_accuracy(batter)
    batter_speed = player_speed(batter)
    batter_volatility = player_volatility(batter)
    batter_luck = player_luck(batter)

    volatility = calculate_volatility(batter_volatility, batter_luck)

    volatility = calculate_volatility(batter_volatility, player_luck(batter))

    batting_speed = batter_speed + volatility * batter_speed

    return batting_speed


def get_raw_batting_accuracy(batter, speed_diff):
    # returns randomized batting score
    batter_strength = player_strength(batter)
    batter_accuracy = player_accuracy(batter)
    batter_speed = player_speed(batter)
    batter_volatility = player_volatility(batter)
    batter_luck = player_luck(batter)

    volatility = calculate_volatility(batter_volatility, batter_luck)

    # if the gap in speed is large, strikeout is more likely
    speed_modifier = speed_diff / 2 if abs(speed_diff) > 3 else speed_diff / 4
    batting_accuracy = batter_accuracy + volatility * batter_accuracy + speed_modifier

    return batting_accuracy


def get_raw_batting_power(batter, bat_speed):
    # returns randomized batting score
    batter_strength = player_strength(batter)
    batter_accuracy = player_accuracy(batter)
    batter_speed = player_speed(batter)
    batter_volatility = player_volatility(batter)
    batter_luck = player_luck(batter)

    volatility = calculate_volatility(batter_volatility, batter_luck)

    batting_power = batter_strength + volatility * batter_strength + bat_speed / 2

    return batting_power


def simulate_pitch(pitcher):
    # returns the result of a batting round
    pitch_speed = get_raw_pitching_speed(pitcher)
    pitch_accuracy = get_raw_pitching_accuracy(pitcher, pitch_speed)

    return pitch_speed, pitch_accuracy


def get_raw_pitching_speed(pitcher):
    # returns randomized pitching score
    pitcher_strength = player_strength(pitcher)
    pitcher_accuracy = player_accuracy(pitcher)
    pitcher_speed = player_speed(pitcher)
    pitcher_volatility = player_volatility(pitcher)
    pitcher_luck = player_luck(pitcher)

    volatility = calculate_volatility(pitcher_volatility, pitcher_luck)

    pitch_speed = pitcher_speed + volatility * pitcher_speed

    return pitch_speed


def get_raw_pitching_accuracy(pitcher, pitch_speed):
    # returns randomized pitching score
    pitcher_strength = player_strength(pitcher)
    pitcher_accuracy = player_accuracy(pitcher)
    pitcher_speed = player_speed(pitcher)
    pitcher_volatility = player_volatility(pitcher)
    pitcher_luck = player_luck(pitcher)

    volatility = calculate_volatility(pitcher_volatility, pitcher_luck)

    speed_modifier = -pitch_speed / 4 if pitch_speed > 5 else pitch_speed / 4
    pitch_accuracy = pitcher_accuracy + volatility * pitcher_accuracy + speed_modifier

    return pitch_accuracy


def calculate_volatility(volatility, luck):
    # returns a positive or negative volatility score, between -1 and 1
    volatility_factor = random.randint(0, volatility)
    luck_factor = random.randint(0, luck) - luck // 2
    luck_factor = 1 if luck_factor > 0 else -1
    volatility_factor *= luck_factor
    volatility_factor /= 100
    return volatility_factor


def player_strength(player):
    # returns the strength of a player
    return player[2]


def player_accuracy(player):
    # returns the accuracy of a player
    return player[3]


def player_speed(player):
    # returns the speed of a player
    return player[4]


def player_volatility(player):
    # returns the volatility of a player
    return player[5]


def player_luck(player):
    # returns the luck of a player
    return player[6]
