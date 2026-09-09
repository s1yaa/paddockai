import type { Metadata } from "next";
import Link from "next/link";
import { getRaces, getCurrentSeason, getDriverChampionship } from "@/lib/api";
import {
  formatDateShort, getCountryFlagByCountry, getRoundLabel,
} from "@/lib/utils";
import { ChevronRight, AlertCircle } from "lucide-react";

export const metadata: Metadata = { title: "Season Hub — PaddockAI" };

export default async function SeasonHubPage() {
  const [seasonRes, racesRes, standingsRes] = await Promise.allSettled([
    getCurrentSeason(),
    getRaces(2026),
    getDriverChampionship(2026),
  ]);

  const season   = seasonRes.status === "fulfilled" ? seasonRes.value : null;
  const races    = racesRes.status === "fulfilled" ? racesRes.value : [];
  const standings = standingsRes.status === "fulfilled" ? standingsRes.value : [];

  const leader   = standings[0] ?? null;
  const completed = races.filter((r) => r.status === "completed").length;
  const total     = season?.total_rounds ?? 24;
  const progressPct = total > 0 ? (completed / total) * 100 : 0;

  const noData = races.length === 0;

  return (
    <div className="min-h-screen bg-bg">
      {/* Header */}
      <div className="border-b border-border px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <div className="text-2xs text-muted uppercase tracking-widest mb-1">
              {season ? `${season.year} Formula 1 Season` : "Formula 1 Season"}
            </div>
            <h1 className="text-xl font-bold text-white tracking-tight">Season Hub</h1>
          </div>
          {leader && (
            <div className="hidden sm:flex items-center gap-3 text-sm">
              <span className="text-muted text-xs">Championship leader</span>
              <div className="flex items-center gap-2">
                {leader.constructor?.color && (
                  <div
                    className="w-1.5 h-4 rounded-sm"
                    style={{ background: leader.constructor.color }}
                  />
                )}
                <span className="font-semibold text-white">{leader.driver.name}</span>
                <span className="font-mono text-secondary text-xs">
                  {leader.points} pts
                </span>
              </div>
            </div>
          )}
        </div>
      </div>

      <div className="p-6 space-y-5">

        {/* Season progress */}
        {!noData && (
          <div className="card p-5">
            <div className="flex flex-wrap gap-6 mb-4">
              <Stat label="Races Completed" value={`${completed} / ${total}`} mono />
              <Stat label="Season Progress" value={`${progressPct.toFixed(0)}%`} mono />
              {leader && (
                <Stat
                  label="Championship Leader"
                  value={leader.driver.name.split(" ")[1]}
                  sub={`${leader.points} pts`}
                  color={leader.constructor?.color}
                />
              )}
              <Stat label="Rounds Remaining" value={`${total - completed}`} mono />
            </div>
            <div className="progress-bar">
              <div
                className="progress-fill"
                style={{ width: `${progressPct}%` }}
              />
            </div>
          </div>
        )}

        {noData && (
          <div className="card p-5 border-border-2">
            <div className="flex items-start gap-3">
              <AlertCircle size={16} className="text-gold mt-0.5 flex-shrink-0" />
              <div>
                <div className="text-sm font-medium text-gold mb-1">Backend not connected</div>
                <p className="text-xs text-secondary">
                  Run <code className="font-mono bg-bg-3 px-1 rounded">make setup</code> to
                  start all services and seed data. The calendar will appear below once the
                  database is running.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Race calendar */}
        <div>
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-sm font-semibold text-white">2026 Season Calendar</h2>
            <span className="text-2xs text-muted">{total} races</span>
          </div>

          <div className="space-y-1.5">
            {noData
              ? Array.from({ length: 6 }).map((_, i) => <SkeletonRaceCard key={i} />)
              : races.map((race) => <RaceCard key={race.id} race={race} />)}
          </div>
        </div>
      </div>
    </div>
  );
}

// ── Sub-components ────────────────────────────────────────────────────────────

function Stat({
  label, value, sub, mono, color,
}: {
  label: string;
  value: string;
  sub?: string;
  mono?: boolean;
  color?: string | null;
}) {
  return (
    <div className="flex items-center gap-3">
      {color && (
        <div className="w-1.5 h-8 rounded-sm flex-shrink-0" style={{ background: color }} />
      )}
      <div>
        <div className="text-2xs text-muted uppercase tracking-widest">{label}</div>
        <div className={`text-lg font-bold text-white ${mono ? "font-mono" : ""}`}>
          {value}
        </div>
        {sub && <div className="text-xs text-muted">{sub}</div>}
      </div>
    </div>
  );
}

function RaceCard({ race }: { race: Awaited<ReturnType<typeof getRaces>>[0] }) {
  const flag = getCountryFlagByCountry(race.country);
  const isActive    = race.status === "active";
  const isCompleted = race.status === "completed";

  const statusConfig: Record<string, { label: string; cls: string }> = {
    completed: { label: "Completed",  cls: "badge-completed" },
    active:    { label: "Active",     cls: "badge-active" },
    upcoming:  { label: "Upcoming",   cls: "badge-upcoming" },
    cancelled: { label: "Cancelled",  cls: "badge-missing" },
  };
  const sc = statusConfig[race.status] ?? statusConfig.upcoming;

  return (
    <Link href={`/season-hub/${race.id}`} className="block">
      <div
        className={`
          flex items-center gap-3 px-4 py-3 rounded-md border transition-all
          ${isActive
            ? "bg-bg-2 border-[#9333ea]/30 shadow-[0_0_12px_rgba(139,92,246,0.08)]"
            : "card card-hover"
          }
        `}
      >
        {/* Round number */}
        <div className="w-8 flex-shrink-0 text-center">
          <div className="font-mono text-lg font-bold leading-none text-muted/60">
            {getRoundLabel(race.round_number)}
          </div>
        </div>

        {/* Active indicator */}
        <div className="w-1.5 flex-shrink-0">
          {isActive && (
            <div className="w-1.5 h-1.5 rounded-full bg-[#A78BFA] animate-pulse-slow" />
          )}
        </div>

        {/* Flag + GP Name */}
        <div className="w-6 text-lg flex-shrink-0 text-center leading-none">
          {flag}
        </div>

        <div className="flex-1 min-w-0">
          <div className={`font-semibold text-sm truncate ${isActive ? "text-white" : isCompleted ? "text-secondary" : "text-white"}`}>
            {race.gp_name}
          </div>
          <div className="text-xs text-muted truncate">
            {race.circuit?.name ?? race.country}
            {race.has_sprint && " · Sprint"}
          </div>
        </div>

        {/* Date */}
        <div className="flex-shrink-0 text-right hidden sm:block">
          <div className="text-xs font-mono text-secondary">
            {formatDateShort(race.date)}
          </div>
        </div>

        {/* Status badge */}
        <div className="flex-shrink-0">
          <span className={`badge ${sc.cls}`}>
            {isActive && (
              <span className="w-1.5 h-1.5 rounded-full bg-current animate-pulse-slow" />
            )}
            {sc.label}
          </span>
        </div>

        <ChevronRight size={14} className="text-muted flex-shrink-0" />
      </div>
    </Link>
  );
}

function SkeletonRaceCard() {
  return (
    <div className="card px-4 py-3 animate-pulse">
      <div className="flex items-center gap-3">
        <div className="w-8 h-5 bg-bg-3 rounded" />
        <div className="w-1.5" />
        <div className="w-6 h-5 bg-bg-3 rounded" />
        <div className="flex-1 space-y-1.5">
          <div className="h-3.5 bg-bg-3 rounded w-1/3" />
          <div className="h-2.5 bg-bg-4 rounded w-1/2" />
        </div>
        <div className="w-16 h-3 bg-bg-3 rounded hidden sm:block" />
        <div className="w-16 h-5 bg-bg-3 rounded" />
      </div>
    </div>
  );
}
