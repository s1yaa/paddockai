-- PaddockAI — Initial Database Schema
-- Migration 001

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ────────────────────────────────────────────────────────────────────────────
-- CIRCUITS
-- ────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS circuits (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    slug            VARCHAR(64) UNIQUE NOT NULL,
    name            VARCHAR(128) NOT NULL,
    short_name      VARCHAR(64),
    city            VARCHAR(64),
    country         VARCHAR(64) NOT NULL,
    country_code    CHAR(3),
    latitude        DECIMAL(10, 6),
    longitude       DECIMAL(10, 6),
    length_km       DECIMAL(6, 3),
    corners         INTEGER,
    lap_record      VARCHAR(16),
    lap_record_driver VARCHAR(64),
    lap_record_year INTEGER,
    circuit_type    VARCHAR(32),        -- permanent / street / hybrid
    overtaking_difficulty INTEGER,      -- 1–10
    altitude_m      INTEGER,
    time_zone       VARCHAR(64),
    first_gp_year   INTEGER,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ────────────────────────────────────────────────────────────────────────────
-- CONSTRUCTORS
-- ────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS constructors (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    slug            VARCHAR(64) UNIQUE NOT NULL,
    name            VARCHAR(128) NOT NULL,
    short_name      VARCHAR(32),
    nationality     VARCHAR(64),
    base            VARCHAR(128),
    principal       VARCHAR(128),
    color_primary   VARCHAR(7),         -- hex
    color_secondary VARCHAR(7),
    engine_supplier VARCHAR(64),
    first_season    INTEGER,
    championships   INTEGER DEFAULT 0,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ────────────────────────────────────────────────────────────────────────────
-- DRIVERS
-- ────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS drivers (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    slug            VARCHAR(64) UNIQUE NOT NULL,
    first_name      VARCHAR(64) NOT NULL,
    last_name       VARCHAR(64) NOT NULL,
    abbreviation    CHAR(3),
    number          INTEGER,
    nationality     VARCHAR(64),
    country_code    CHAR(3),
    date_of_birth   DATE,
    constructor_id  UUID REFERENCES constructors(id) ON DELETE SET NULL,
    active          BOOLEAN DEFAULT TRUE,
    championships   INTEGER DEFAULT 0,
    career_wins     INTEGER DEFAULT 0,
    career_podiums  INTEGER DEFAULT 0,
    career_poles    INTEGER DEFAULT 0,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ────────────────────────────────────────────────────────────────────────────
-- SEASONS
-- ────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS seasons (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    year            INTEGER UNIQUE NOT NULL,
    total_rounds    INTEGER NOT NULL,
    current         BOOLEAN DEFAULT FALSE,
    status          VARCHAR(32) DEFAULT 'active', -- active / completed
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ────────────────────────────────────────────────────────────────────────────
-- RACES
-- ────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS races (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    season_id       UUID NOT NULL REFERENCES seasons(id) ON DELETE CASCADE,
    circuit_id      UUID REFERENCES circuits(id) ON DELETE SET NULL,
    round_number    INTEGER NOT NULL,
    gp_name         VARCHAR(128) NOT NULL,
    official_name   VARCHAR(256),
    country         VARCHAR(64),
    date            DATE,
    status          VARCHAR(32) DEFAULT 'upcoming',
    -- upcoming / active / completed / cancelled
    has_sprint      BOOLEAN DEFAULT FALSE,
    openf1_meeting_key INTEGER,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(season_id, round_number)
);

-- ────────────────────────────────────────────────────────────────────────────
-- SESSIONS (FP1 / FP2 / FP3 / Q / R / Sprint Q / Sprint)
-- ────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS sessions (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    race_id         UUID NOT NULL REFERENCES races(id) ON DELETE CASCADE,
    session_type    VARCHAR(32) NOT NULL,
    -- fp1 / fp2 / fp3 / qualifying / race / sprint_qualifying / sprint
    scheduled_at    TIMESTAMPTZ,
    status          VARCHAR(32) DEFAULT 'upcoming',
    -- upcoming / active / completed / cancelled
    openf1_session_key INTEGER,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(race_id, session_type)
);

-- ────────────────────────────────────────────────────────────────────────────
-- PRACTICE RESULTS
-- ────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS practice_results (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id      UUID NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    driver_id       UUID NOT NULL REFERENCES drivers(id),
    constructor_id  UUID NOT NULL REFERENCES constructors(id),
    position        INTEGER,
    best_lap_time   VARCHAR(16),        -- "1:23.456"
    best_lap_ms     INTEGER,            -- milliseconds
    gap_to_first_ms INTEGER,
    laps_completed  INTEGER,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ────────────────────────────────────────────────────────────────────────────
-- QUALIFYING RESULTS
-- ────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS qualifying_results (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id      UUID NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    driver_id       UUID NOT NULL REFERENCES drivers(id),
    constructor_id  UUID NOT NULL REFERENCES constructors(id),
    position        INTEGER NOT NULL,
    q1_time         VARCHAR(16),
    q1_ms           INTEGER,
    q2_time         VARCHAR(16),
    q2_ms           INTEGER,
    q3_time         VARCHAR(16),
    q3_ms           INTEGER,
    best_time       VARCHAR(16),
    best_ms         INTEGER,
    gap_to_pole_ms  INTEGER,
    eliminated_in   VARCHAR(4),         -- Q1 / Q2 / NULL (made Q3)
    penalty         VARCHAR(256),
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(session_id, driver_id)
);

-- ────────────────────────────────────────────────────────────────────────────
-- RACE RESULTS
-- ────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS race_results (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id      UUID NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    driver_id       UUID NOT NULL REFERENCES drivers(id),
    constructor_id  UUID NOT NULL REFERENCES constructors(id),
    grid_position   INTEGER,
    finishing_position INTEGER,
    status          VARCHAR(64) DEFAULT 'Finished',
    -- Finished / DNF / DNS / DSQ / ...
    dnf_reason      VARCHAR(256),
    points          DECIMAL(4, 1) DEFAULT 0,
    fastest_lap     BOOLEAN DEFAULT FALSE,
    fastest_lap_time VARCHAR(16),
    laps_completed  INTEGER,
    gap_to_winner   VARCHAR(32),
    penalty         VARCHAR(256),
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(session_id, driver_id)
);

-- ────────────────────────────────────────────────────────────────────────────
-- DRIVER CHAMPIONSHIP STANDINGS
-- ────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS driver_standings (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    season_id       UUID NOT NULL REFERENCES seasons(id) ON DELETE CASCADE,
    driver_id       UUID NOT NULL REFERENCES drivers(id),
    constructor_id  UUID REFERENCES constructors(id),
    position        INTEGER,
    points          DECIMAL(6, 1) DEFAULT 0,
    wins            INTEGER DEFAULT 0,
    podiums         INTEGER DEFAULT 0,
    poles           INTEGER DEFAULT 0,
    dnfs            INTEGER DEFAULT 0,
    races_entered   INTEGER DEFAULT 0,
    updated_at      TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(season_id, driver_id)
);

-- ────────────────────────────────────────────────────────────────────────────
-- CONSTRUCTOR CHAMPIONSHIP STANDINGS
-- ────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS constructor_standings (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    season_id       UUID NOT NULL REFERENCES seasons(id) ON DELETE CASCADE,
    constructor_id  UUID NOT NULL REFERENCES constructors(id),
    position        INTEGER,
    points          DECIMAL(6, 1) DEFAULT 0,
    wins            INTEGER DEFAULT 0,
    podiums         INTEGER DEFAULT 0,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(season_id, constructor_id)
);

-- ────────────────────────────────────────────────────────────────────────────
-- MODEL VERSIONS
-- ────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS model_versions (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name            VARCHAR(64) NOT NULL,
    version         VARCHAR(32) NOT NULL,
    model_type      VARCHAR(32) NOT NULL,
    -- qualifying / race / dnf / points / championship
    training_started_at  TIMESTAMPTZ,
    training_finished_at TIMESTAMPTZ,
    dataset_version VARCHAR(64),
    training_seasons VARCHAR(64),       -- e.g. "2018-2024"
    validation_season INTEGER,
    features        JSONB,
    metrics         JSONB,
    active          BOOLEAN DEFAULT FALSE,
    notes           TEXT,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ────────────────────────────────────────────────────────────────────────────
-- PREDICTION SNAPSHOTS
-- ────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS prediction_snapshots (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    race_id         UUID NOT NULL REFERENCES races(id) ON DELETE CASCADE,
    session_id      UUID REFERENCES sessions(id),
    model_version_id UUID REFERENCES model_versions(id),
    prediction_type VARCHAR(32) NOT NULL,
    -- qualifying / race / championship_driver / championship_constructor
    stage           VARCHAR(64) NOT NULL,
    -- pre_weekend / after_fp1 / after_fp2 / after_fp3 / after_qualifying / pre_race
    predicted_at    TIMESTAMPTZ DEFAULT NOW(),
    data_version    VARCHAR(64),
    predictions     JSONB NOT NULL,     -- full prediction payload
    probabilities   JSONB,
    expected_points JSONB,
    metadata        JSONB,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ────────────────────────────────────────────────────────────────────────────
-- SIMULATION RUNS (Monte Carlo)
-- ────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS simulation_runs (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    season_id       UUID NOT NULL REFERENCES seasons(id),
    model_version_id UUID REFERENCES model_versions(id),
    from_race_id    UUID REFERENCES races(id),
    n_simulations   INTEGER NOT NULL,
    scenario_type   VARCHAR(32) DEFAULT 'baseline',
    -- baseline / what-if
    scenario_params JSONB,
    results         JSONB NOT NULL,
    ran_at          TIMESTAMPTZ DEFAULT NOW()
);

-- ────────────────────────────────────────────────────────────────────────────
-- FEATURE SNAPSHOTS (for ML)
-- ────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS feature_snapshots (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    race_id         UUID NOT NULL REFERENCES races(id),
    driver_id       UUID NOT NULL REFERENCES drivers(id),
    snapshot_type   VARCHAR(32) DEFAULT 'pre_race',
    features        JSONB NOT NULL,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(race_id, driver_id, snapshot_type)
);

-- ────────────────────────────────────────────────────────────────────────────
-- INDEXES
-- ────────────────────────────────────────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_races_season      ON races(season_id);
CREATE INDEX IF NOT EXISTS idx_races_date        ON races(date);
CREATE INDEX IF NOT EXISTS idx_sessions_race     ON sessions(race_id);
CREATE INDEX IF NOT EXISTS idx_race_results_session ON race_results(session_id);
CREATE INDEX IF NOT EXISTS idx_qual_results_session ON qualifying_results(session_id);
CREATE INDEX IF NOT EXISTS idx_predictions_race  ON prediction_snapshots(race_id);
CREATE INDEX IF NOT EXISTS idx_driver_standings_season ON driver_standings(season_id);
CREATE INDEX IF NOT EXISTS idx_constructor_standings_season ON constructor_standings(season_id);
