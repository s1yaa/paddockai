// ── API Types ─────────────────────────────────────────────────────────────

export interface Season {
  id: string;
  year: number;
  total_rounds: number;
  current: boolean;
  status: "active" | "completed";
}

export interface Circuit {
  id: string;
  slug: string;
  name: string;
  short_name: string | null;
  city: string | null;
  country: string;
  country_code: string | null;
  length_km: number | null;
  corners: number | null;
  circuit_type: "permanent" | "street" | "hybrid" | null;
  overtaking_difficulty: number | null;
  lap_record: string | null;
  lap_record_driver: string | null;
  lap_record_year: number | null;
  first_gp_year: number | null;
  latitude: number | null;
  longitude: number | null;
}

export interface Constructor {
  id: string;
  slug: string;
  name: string;
  short_name: string | null;
  nationality: string | null;
  color_primary: string | null;
  color_secondary: string | null;
  engine_supplier: string | null;
  championships: number;
  base?: string | null;
  principal?: string | null;
  first_season?: number | null;
}

export interface Driver {
  id: string;
  slug: string;
  first_name: string;
  last_name: string;
  abbreviation: string | null;
  number: number | null;
  nationality: string | null;
  country_code: string | null;
  active: boolean;
  constructor: {
    id: string;
    slug: string;
    name: string;
    short_name: string | null;
    color_primary: string | null;
  } | null;
  championships?: number;
  career_wins?: number;
  career_podiums?: number;
  career_poles?: number;
}

export interface SessionData {
  id: string;
  session_type: SessionType;
  scheduled_at: string | null;
  status: SessionStatus;
}

export type SessionType =
  | "fp1" | "fp2" | "fp3"
  | "qualifying" | "race"
  | "sprint_qualifying" | "sprint";

export type SessionStatus = "upcoming" | "active" | "completed" | "cancelled";

export type RaceStatus =
  | "upcoming" | "active" | "completed" | "cancelled";

export interface Race {
  id: string;
  round_number: number;
  gp_name: string;
  official_name: string | null;
  country: string | null;
  date: string | null;
  status: RaceStatus;
  has_sprint: boolean;
  circuit: Circuit | null;
  season_id?: string;
  sessions?: SessionData[];
}

export interface DriverStanding {
  id: string;
  position: number | null;
  points: number;
  wins: number;
  podiums: number;
  poles: number;
  dnfs: number;
  races_entered: number;
  driver: {
    id: string;
    slug: string;
    name: string;
    abbreviation: string | null;
    number: number | null;
    nationality: string | null;
  };
  constructor: {
    id: string | null;
    name: string | null;
    slug: string | null;
    color: string | null;
  } | null;
}

export interface ConstructorStanding {
  id: string;
  position: number | null;
  points: number;
  wins: number;
  podiums: number;
  constructor: {
    id: string;
    name: string;
    slug: string;
    color: string | null;
  };
}

// ── UI Types ─────────────────────────────────────────────────────────────────

export type NavItem = {
  label: string;
  href: string;
  icon: string;
  group?: string;
};

export type ModelStatus = "updated" | "new_data" | "unavailable";

export interface PredictionEntry {
  position: number;
  driver_name: string;
  driver_abbr: string;
  team_name: string;
  team_color: string;
  win_prob: number;
  podium_prob: number;
  top5_prob: number;
  top10_prob: number;
  dnf_prob: number;
  expected_points: number;
}

export interface PredictionSnapshot {
  id: string;
  stage: string;
  predicted_at: string;
  model_version: string;
  predictions: PredictionEntry[];
}
