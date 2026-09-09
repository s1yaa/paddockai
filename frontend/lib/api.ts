/**
 * PaddockAI API client
 * Fetches from /api/* which Next.js rewrites to the FastAPI backend.
 * Falls back to mock data when NEXT_PUBLIC_DEMO_MODE=true or API is unavailable.
 */

import type {
  Season,
  Race,
  Driver,
  Constructor,
  DriverStanding,
  ConstructorStanding,
} from "@/types";

const BASE = "";  // uses Next.js rewrites

async function apiFetch<T>(path: string): Promise<T> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 2000); // 2s timeout
  try {
    const res = await fetch(`${BASE}${path}`, {
      next: { revalidate: 60 },
      signal: controller.signal,
    });
    clearTimeout(timer);
    if (!res.ok) throw new Error(`API error ${res.status}: ${path}`);
    return res.json() as Promise<T>;
  } catch (err) {
    clearTimeout(timer);
    throw err;
  }
}

// ── Seasons ──────────────────────────────────────────────────────────────────
export async function getSeasons(): Promise<Season[]> {
  return apiFetch<Season[]>("/api/seasons/");
}

export async function getCurrentSeason(): Promise<Season | null> {
  try {
    return await apiFetch<Season>("/api/seasons/current");
  } catch { return null; }
}

// ── Races ─────────────────────────────────────────────────────────────────────
export async function getRaces(seasonYear?: number): Promise<Race[]> {
  const q = seasonYear ? `?season_year=${seasonYear}` : "";
  return apiFetch<Race[]>(`/api/races/${q}`);
}

export async function getNextRace(): Promise<Race | null> {
  try {
    return await apiFetch<Race>("/api/races/next");
  } catch { return null; }
}

export async function getRace(id: string): Promise<Race | null> {
  try {
    return await apiFetch<Race>(`/api/races/${id}`);
  } catch { return null; }
}

// ── Drivers ───────────────────────────────────────────────────────────────────
export async function getDrivers(activeOnly = true): Promise<Driver[]> {
  return apiFetch<Driver[]>(`/api/drivers/?active_only=${activeOnly}`);
}

// ── Constructors ──────────────────────────────────────────────────────────────
export async function getConstructors(): Promise<Constructor[]> {
  return apiFetch<Constructor[]>("/api/constructors/");
}

// ── Championship ─────────────────────────────────────────────────────────────
export async function getDriverChampionship(year?: number): Promise<DriverStanding[]> {
  const q = year ? `?season_year=${year}` : "";
  return apiFetch<DriverStanding[]>(`/api/championship/drivers${q}`);
}

export async function getConstructorChampionship(year?: number): Promise<ConstructorStanding[]> {
  const q = year ? `?season_year=${year}` : "";
  return apiFetch<ConstructorStanding[]>(`/api/championship/constructors${q}`);
}
