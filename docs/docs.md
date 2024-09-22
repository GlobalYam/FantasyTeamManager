# Plan for database structure

# SQL database:

## Users
- user_id: (SERIAL PRIMARY KEY)
- username: (TEXT UNIQUE)
- password: (TEXT) "(hidden)"
- is_admin: (boolean)

- current_team: (team_id)
- wins: (int)
- losses: (int)
- ties: (int)

## Players
- player_id: (id)
- name: (str) 
- retired: (bool) "True if retired"
- born: (date) "date of birth"

- power: (int) "(hidden) used to calc hits"
- accuracy: (int) "(hidden) used to calc strikeouts"
- speed: (int) "(hidden) used to calc outs"
- volatility: (int) "(hidden) adds randomness"

- hit_average: (int) "average hits when batting"
- strikeout_average: (int) "average stikeouts when pitching"
- out_average: (int) "average outs when fielding"

- mvps: (int) "times this player has been mvp"
- games: (int) "equals to: wins + losses + ties"
- wins: (int)
- losses: (int)
- ties: (int)

## Teams
- team_id: (id)
- name: (str)
- owner: (user_id)
- location: (str)

- wins: (int)
- losses: (int)
- ties: (int)

- batter: (player_id)
- pitcher: (player_id)
- catcher: (player_id)

## Games
- game_id: (id)
- date: (date)

- home_team: (team_id)
- home_batter: (player_id)
- home_pitcher: (player_id)
- home_fielder: (player_id)

- visiting_team: (team_id)
- visiting_batter: (player_id)
- visiting_pitcher: (player_id)
- visiting_fielder: (player_id)

- home_hits: (int) "home_batters hit_calc function"
- visiting_hits: (int) "visiting_batters hit_calc function"

- home_strikeouts: (int) "home_pitchers stikeout_calc function"
- visiting_strikeouts: (int) "visiting_pitchers strikeout_calc function"

- home_outs: (int) "home_fielders out_calc function"
- visiting_outs: (int) "visiting_fielders out_calc function"

- home_points: (int) "home_team"
- visiting_points: (int) "visiting_team"

- mvp: (player_id) "player with the highest score in the game"

- winner: (team_id) "if the game is a tie, winner is None"

# Calculations
- hit_calc "power + accuracy * volatility_score"
- stikeout_calc "power + speed * volatility_score"
- out_calc  "accuracy + speed * volatility_score"

