-- Users Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,  -- "(hidden)"
    is_admin BOOLEAN DEFAULT FALSE, 

    current_team INT DEFAULT 0, -- REFERENCES teams(id),  -- Reference to id in Teams table
    wins INT DEFAULT 0,
    losses INT DEFAULT 0,
    games_tied INT DEFAULT 0
);

-- Players Table
CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    retired BOOLEAN DEFAULT FALSE,  -- "True if retired"
    born DATE,  -- "date of birth"

    power INT DEFAULT 0,  -- "(hidden) used to calc hits"
    accuracy INT DEFAULT 0,  -- "(hidden) used to calc strikeouts"
    speed INT DEFAULT 0,  -- "(hidden) used to calc outs"
    volatility INT DEFAULT 0,  -- "(hidden) adds randomness"

    hit_average INT DEFAULT 0,  -- "average hits when batting"
    strikeout_average INT DEFAULT 0,  -- "average strikeouts when pitching"
    out_average INT DEFAULT 0,  -- "average outs when fielding"

    mvps INT DEFAULT 0,  -- "times this player has been MVP"
    games INT DEFAULT 0,  -- Equals to wins + losses + games_tied
    wins INT DEFAULT 0,
    losses INT DEFAULT 0,
    games_tied INT DEFAULT 0
);

-- Teams Table
CREATE TABLE teams (
    id SERIAL PRIMARY KEY, 
    name TEXT NOT NULL,
    owner INT DEFAULT 0, --REFERENCES users(id),  -- Reference to id in Users table
    location TEXT,

    games INT DEFAULT 0,
    wins INT DEFAULT 0,
    losses INT DEFAULT 0,
    games_tied INT DEFAULT 0,

    batter INT DEFAULT 0, --REFERENCES players(id),   -- Reference to id in Players table
    pitcher INT DEFAULT 0, --REFERENCES players(id),
    catcher INT DEFAULT 0 --REFERENCES players(id)
);

-- Games Table
CREATE TABLE games (
    id SERIAL PRIMARY KEY, 
    date DATE NOT NULL,

    home_team INT DEFAULT 0, --REFERENCES teams(id),  -- Reference to id in Teams table
    home_batter INT DEFAULT 0, --REFERENCES players(id),  -- Reference to id in Players table
    home_pitcher INT DEFAULT 0, --REFERENCES players(id),
    home_fielder INT DEFAULT 0, --REFERENCES players(id),

    visiting_team INT DEFAULT 0, --REFERENCES teams(id),  -- Reference to id in Teams table
    visiting_batter INT DEFAULT 0, --REFERENCES players(id),
    visiting_pitcher INT DEFAULT 0, --REFERENCES players(id),
    visiting_fielder INT DEFAULT 0, --REFERENCES players(id),

    home_hits INT DEFAULT 0,  -- "home_batter's hit_calc function"
    visiting_hits INT DEFAULT 0,  -- "visiting_batter's hit_calc function"

    home_strikeouts INT DEFAULT 0,  -- "home_pitcher's strikeout_calc function"
    visiting_strikeouts INT DEFAULT 0,  -- "visiting_pitcher's strikeout_calc function"

    home_outs INT DEFAULT 0,  -- "home_fielder's out_calc function"
    visiting_outs INT DEFAULT 0,  -- "visiting_fielder's out_calc function"

    home_points INT DEFAULT 0,  -- "home_team's points"
    visiting_points INT DEFAULT 0,  -- "visiting_team's points"

    mvp INT DEFAULT 0, --REFERENCES players(id),  -- "Player with the highest score in the game"

    winner INT DEFAULT 0 --REFERENCES teams(id)  -- "if the game is a tie, winner is NULL"
);

INSERT INTO players (name, power, accuracy, speed) VALUES
    ('Player 1', FLOOR(RANDOM() * 11), FLOOR(RANDOM() * 11), FLOOR(RANDOM() * 11)),
    ('Player 2', FLOOR(RANDOM() * 11), FLOOR(RANDOM() * 11), FLOOR(RANDOM() * 11)),
    ('Player 3', FLOOR(RANDOM() * 11), FLOOR(RANDOM() * 11), FLOOR(RANDOM() * 11)),
    ('Player 4', FLOOR(RANDOM() * 11), FLOOR(RANDOM() * 11), FLOOR(RANDOM() * 11)),
    ('Player 5', FLOOR(RANDOM() * 11), FLOOR(RANDOM() * 11), FLOOR(RANDOM() * 11)),
    ('Player 6', FLOOR(RANDOM() * 11), FLOOR(RANDOM() * 11), FLOOR(RANDOM() * 11)),
    ('Player 7', FLOOR(RANDOM() * 11), FLOOR(RANDOM() * 11), FLOOR(RANDOM() * 11)),
    ('Player 8', FLOOR(RANDOM() * 11), FLOOR(RANDOM() * 11), FLOOR(RANDOM() * 11)),
    ('Player 9', FLOOR(RANDOM() * 11), FLOOR(RANDOM() * 11), FLOOR(RANDOM() * 11)),
    ('Player 10', FLOOR(RANDOM() * 11), FLOOR(RANDOM() * 11), FLOOR(RANDOM() * 11));