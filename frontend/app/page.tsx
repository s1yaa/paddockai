import { Suspense } from "react";
import type { Metadata } from "next";
import {
  getNextRace, getDriverChampionship, getConstructorChampionship,
} from "@/lib/api";
import {
  formatDateShort, getCountryFlagByCountry, daysUntil, formatPoints,
} from "@/lib/utils";
import { Calendar, Activity, Zap, TrendingUp, Clock, RefreshCw } from "lucide-react";

export const metadata: Metadata = { title: "Overview — PaddockAI" };

export default async function OverviewPage() {
  // Fetch in parallel; silently handle errors (backend may not be running)
  const [nextRace, driverStandings, constructorStandings] = await Promise.allSettled([
    getNextRace(),
    getDriverChampionship(),
    getConstructorChampionship(),
  ]);

  const race = nextRace.status === "fulfilled" ? nextRace.value : null;
  const drivers = driverStandings.status === "fulfilled" ? driverStandings.value : [];
  const constructors = constructorStandings.status === "fulfilled" ? constructorStandings.value : [];

  const daysToRace = race ? daysUntil(race.date) : null;
  const leader = drivers[0] ?? null;
  const conLeader = constructors[0] ?? null;

  return (
    <div className="min-h-screen bg-bg">
      {/* Page header */}
      <div className="border-b border-border px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <div className="text-2xs text-muted uppercase tracking-widest mb-1">
              F1 Prediction Intelligence
            </div>
            <h1 className="text-xl font-bold text-white tracking-tight">Overview</h1>
          </div>
          <div className="flex items-center gap-3">
            <ModelStatusBadge status="updated" updatedAt="2 hours ago" version="v1.00" />
          </div>
        </div>
      </div>

      <div className="p-6 space-y-6">

        {/* ── NEXT RACE HERO ─────────────────────────────────────────────── */}
        {race ? (
          <NextRaceHero race={race} daysToRace={daysToRace} />
        ) : (
          <BackendOfflineBanner />
        )}

        {/* ── HERO METRICS ROW ─────────────────────────────────────────────── */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
          <MetricCard
            label="Predicted Winner"
            value="L. Norris"
            sub="McLaren · 34.2%"
            accent
          />
          <MetricCard
            label="Predicted Pole"
            value="L. Norris"
            sub="McLaren · 28.7%"
          />
          <MetricCard
            label={leader ? `${leader.driver.name.split(" ")[1]}` : "—"}
            value={leader ? formatPoints(leader.points) + " pts" : "—"}
            sub="Championship Leader"
            highlight={leader?.constructor?.color ?? "#E8001D"}
          />
          <MetricCard
            label={conLeader ? conLeader.constructor.name : "—"}
            value={conLeader ? formatPoints(conLeader.points) + " pts" : "—"}
            sub="Constructor Leader"
            highlight={conLeader?.constructor?.color ?? "#FF8000"}
          />
        </div>

        {/* ── PREDICTED PODIUM ──────────────────────────────────────────────── */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          <div className="lg:col-span-2">
            <PredictedPodium />
          </div>
          <div>
            <ChampionshipSnapshot leader={leader} conLeader={conLeader} />
          </div>
        </div>

        {/* ── DRIVER STANDINGS PREVIEW ──────────────────────────────────────── */}
        {drivers.length > 0 && (
          <StandingsPreview drivers={drivers.slice(0, 8)} />
        )}

      </div>
    </div>
  );
}

// ── Components ────────────────────────────────────────────────────────────────

function NextRaceHero({ race, daysToRace }: { race: NonNullable<Awaited<ReturnType<typeof getNextRace>>>; daysToRace: number | null }) {
  const flag = getCountryFlagByCountry(race.country);
  const circuit = race.circuit;

  return (
    <div className="card relative overflow-hidden">
      {/* Background grid overlay */}
      <div className="absolute inset-0 grid-overlay opacity-60 pointer-events-none" />
      {/* Red accent bar */}
      <div className="absolute left-0 top-0 bottom-0 w-0.5 bg-red" />

      <div className="relative p-5 sm:p-6">
        <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <span className="badge badge-active">
                <span className="w-1.5 h-1.5 rounded-full bg-current animate-pulse-slow" />
                Next Race
              </span>
              <span className="text-2xs text-muted font-mono">
                RD {String(race.round_number).padStart(2, "0")} / 24
              </span>
            </div>

            <div>
              <div className="flex items-center gap-2 mb-1">
                <span className="text-xl">{flag}</span>
                <h2 className="text-2xl font-bold text-white tracking-tight">
                  {race.gp_name}
                </h2>
              </div>
              {circuit && (
                <div className="text-sm text-secondary">
                  {circuit.name}
                  {circuit.city && ` · ${circuit.city}`}
                </div>
              )}
            </div>

            <div className="flex flex-wrap gap-4 text-sm">
              <div className="flex items-center gap-1.5 text-secondary">
                <Calendar size={13} className="text-muted" />
                {formatDateShort(race.date)}
              </div>
              {circuit?.length_km && (
                <div className="text-secondary">
                  <span className="text-muted">Circuit </span>
                  <span className="font-mono">{circuit.length_km} km</span>
                </div>
              )}
              {circuit?.corners && (
                <div className="text-secondary">
                  <span className="text-muted">Corners </span>
                  <span className="font-mono">{circuit.corners}</span>
                </div>
              )}
              {circuit?.circuit_type && (
                <span className="badge badge-waiting capitalize">
                  {circuit.circuit_type}
                </span>
              )}
              {race.has_sprint && (
                <span className="badge" style={{ background: "rgba(139,92,246,0.15)", color: "#A78BFA" }}>
                  Sprint Weekend
                </span>
              )}
            </div>
          </div>

          {/* Countdown */}
          {daysToRace !== null && daysToRace >= 0 && (
            <div className="flex-shrink-0 text-right">
              <div className="text-5xl font-black font-mono text-white leading-none">
                {daysToRace}
              </div>
              <div className="text-sm text-muted mt-1">
                day{daysToRace !== 1 ? "s" : ""} away
              </div>
              <div className="text-2xs text-muted/60 mt-1 uppercase tracking-wider">
                Race Day Countdown
              </div>
            </div>
          )}
        </div>

        {/* Weekend progress */}
        <div className="mt-5 pt-4 border-t border-border">
          <div className="flex items-center gap-1 mb-3">
            <Activity size={12} className="text-muted" />
            <span className="text-2xs text-muted uppercase tracking-widest">
              Weekend Status
            </span>
          </div>
          <div className="flex gap-2">
            {["FP1", "FP2", "FP3", "Qualifying", "Race"].map((s, i) => (
              <div key={s} className="flex-1 min-w-0">
                <div className={`h-1 rounded-full mb-1.5 ${
                  race.status === "active" && i === 0
                    ? "bg-red"
                    : "bg-border-2"
                }`} />
                <div className="text-2xs text-muted text-center truncate">{s}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function BackendOfflineBanner() {
  return (
    <div className="card p-6 border-border-2">
      <div className="flex items-center gap-3 mb-3">
        <div className="w-2 h-2 rounded-full bg-gold animate-pulse" />
        <span className="text-sm font-medium text-gold">Backend Offline</span>
      </div>
      <p className="text-sm text-secondary">
        The FastAPI backend is not running. Start it with{" "}
        <code className="text-xs font-mono bg-bg-3 px-1.5 py-0.5 rounded">
          make start
        </code>{" "}
        or{" "}
        <code className="text-xs font-mono bg-bg-3 px-1.5 py-0.5 rounded">
          docker-compose up
        </code>
        . The UI displays live seeded data once connected.
      </p>
    </div>
  );
}

function MetricCard({
  label, value, sub, accent, highlight,
}: {
  label: string;
  value: string;
  sub?: string;
  accent?: boolean;
  highlight?: string;
}) {
  return (
    <div className="card p-4 relative overflow-hidden">
      {highlight && (
        <div
          className="absolute left-0 top-0 bottom-0 w-0.5"
          style={{ background: highlight }}
        />
      )}
      {accent && <div className="absolute left-0 top-0 bottom-0 w-0.5 bg-red" />}
      <div className="text-2xs text-muted uppercase tracking-widest mb-2">{label}</div>
      <div className="text-lg font-bold text-white leading-tight truncate">{value}</div>
      {sub && <div className="text-xs text-secondary mt-0.5 truncate">{sub}</div>}
    </div>
  );
}

function PredictedPodium() {
  const PODIUM = [
    { pos: 1, name: "Lando Norris",   abbr: "NOR", team: "McLaren",   color: "#FF8000", winProb: 34.2, podiumProb: 68.1 },
    { pos: 2, name: "Max Verstappen", abbr: "VER", team: "Red Bull",  color: "#1B3A6B", winProb: 24.8, podiumProb: 61.4 },
    { pos: 3, name: "Charles Leclerc",abbr: "LEC", team: "Ferrari",   color: "#DC0000", winProb: 16.1, podiumProb: 48.9 },
  ];

  return (
    <div className="card p-5">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <TrendingUp size={14} className="text-red" />
          <h3 className="text-sm font-semibold text-white">Predicted Podium</h3>
        </div>
        <span className="text-2xs text-muted">Belgian GP · Pre-Weekend</span>
      </div>

      <div className="space-y-2">
        {PODIUM.map((d) => (
          <div
            key={d.pos}
            className="flex items-center gap-3 p-3 rounded-md bg-bg-2 border border-border hover:border-border-2 transition-colors"
          >
            <div className={`pos-indicator p${d.pos}`}>P{d.pos}</div>

            <div
              className="team-bar self-stretch"
              style={{ background: d.color }}
            />

            <div className="flex-1 min-w-0">
              <div className="text-sm font-semibold text-white">{d.name}</div>
              <div className="text-xs text-muted">{d.team}</div>
            </div>

            <div className="text-right flex-shrink-0">
              <div className="text-sm font-mono font-semibold text-white">
                {d.winProb.toFixed(1)}%
              </div>
              <div className="text-2xs text-muted">Win prob</div>
            </div>

            <div className="w-24 hidden sm:block">
              <div className="text-2xs text-muted mb-1">
                Podium {d.podiumProb.toFixed(0)}%
              </div>
              <div className="prob-bar-track">
                <div
                  className="prob-bar-fill"
                  style={{
                    width: `${d.podiumProb}%`,
                    background: d.color,
                  }}
                />
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-3 pt-3 border-t border-border flex items-center gap-2">
        <Zap size={11} className="text-muted" />
        <span className="text-2xs text-muted">
          Model: RaceRank v1.00 · Pre-weekend estimate · 
          <span className="text-muted/60"> No practice data yet</span>
        </span>
      </div>
    </div>
  );
}

function ChampionshipSnapshot({
  leader,
  conLeader,
}: {
  leader: Awaited<ReturnType<typeof getDriverChampionship>>[0] | null;
  conLeader: Awaited<ReturnType<typeof getConstructorChampionship>>[0] | null;
}) {
  return (
    <div className="card p-5 h-full">
      <div className="flex items-center gap-2 mb-4">
        <TrendingUp size={14} className="text-red" />
        <h3 className="text-sm font-semibold text-white">Championship</h3>
      </div>

      <div className="space-y-4">
        <div>
          <div className="text-2xs text-muted uppercase tracking-widest mb-2">
            Drivers
          </div>
          {leader ? (
            <div className="space-y-1">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-sm font-semibold text-white">
                    {leader.driver.name}
                  </div>
                  <div className="text-xs text-muted">
                    {leader.constructor?.name}
                  </div>
                </div>
                <div className="text-right">
                  <div className="stat-number-sm text-white font-mono">
                    {formatPoints(leader.points)}
                  </div>
                  <div className="text-2xs text-muted">pts</div>
                </div>
              </div>
              <div className="text-xs text-muted">
                {leader.wins}W · {leader.podiums}P · {leader.races_entered} races
              </div>
            </div>
          ) : (
            <NoDataPlaceholder text="Start backend to load standings" />
          )}
        </div>

        <div className="divider" />

        <div>
          <div className="text-2xs text-muted uppercase tracking-widest mb-2">
            Constructors
          </div>
          {conLeader ? (
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div
                  className="w-2 h-6 rounded-sm flex-shrink-0"
                  style={{ background: conLeader.constructor.color ?? "#E8001D" }}
                />
                <div>
                  <div className="text-sm font-semibold text-white">
                    {conLeader.constructor.name}
                  </div>
                  <div className="text-xs text-muted">
                    {conLeader.wins}W · {conLeader.podiums}P
                  </div>
                </div>
              </div>
              <div className="text-right">
                <div className="stat-number-sm text-white font-mono">
                  {formatPoints(conLeader.points)}
                </div>
                <div className="text-2xs text-muted">pts</div>
              </div>
            </div>
          ) : (
            <NoDataPlaceholder text="No data" />
          )}
        </div>

        <div className="divider" />

        <div className="text-2xs text-muted flex items-center gap-1.5">
          <Clock size={10} />
          After Round 12 · 12 / 24 Races
        </div>
      </div>
    </div>
  );
}

function StandingsPreview({
  drivers,
}: {
  drivers: Awaited<ReturnType<typeof getDriverChampionship>>;
}) {
  return (
    <div className="card overflow-hidden">
      <div className="px-5 py-3 border-b border-border flex items-center justify-between">
        <h3 className="text-sm font-semibold text-white">Driver Standings</h3>
        <a href="/championship" className="text-xs text-red hover:text-red/80 transition-colors">
          Full table →
        </a>
      </div>
      <table className="f1-table">
        <thead>
          <tr>
            <th>Pos</th>
            <th>Driver</th>
            <th className="hidden sm:table-cell">Team</th>
            <th>Points</th>
            <th className="hidden md:table-cell">Wins</th>
          </tr>
        </thead>
        <tbody>
          {drivers.map((s) => (
            <tr key={s.id}>
              <td>
                <span className={`pos-indicator ${s.position === 1 ? "p1" : s.position === 2 ? "p2" : s.position === 3 ? "p3" : ""}`}>
                  {s.position}
                </span>
              </td>
              <td>
                <div className="flex items-center gap-2">
                  {s.constructor?.color && (
                    <div
                      className="team-bar h-5"
                      style={{ background: s.constructor.color }}
                    />
                  )}
                  <div>
                    <div className="font-medium text-white">{s.driver.name}</div>
                    <div className="text-2xs text-muted sm:hidden">
                      {s.constructor?.name}
                    </div>
                  </div>
                </div>
              </td>
              <td className="hidden sm:table-cell text-secondary">
                {s.constructor?.name}
              </td>
              <td>
                <span className="font-mono font-semibold text-white">
                  {formatPoints(s.points)}
                </span>
              </td>
              <td className="hidden md:table-cell text-secondary font-mono">
                {s.wins}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function ModelStatusBadge({
  status,
  updatedAt,
  version,
}: {
  status: "updated" | "new_data" | "unavailable";
  updatedAt: string;
  version: string;
}) {
  const config = {
    updated:     { dot: "bg-green",  label: "Model Updated",  cls: "text-green" },
    new_data:    { dot: "bg-gold",   label: "New Data",       cls: "text-gold" },
    unavailable: { dot: "bg-red",    label: "Unavailable",    cls: "text-red" },
  }[status];

  return (
    <div className="flex items-center gap-2 px-3 py-1.5 bg-bg-2 border border-border rounded-md">
      <div className={`w-1.5 h-1.5 rounded-full ${config.dot}`} />
      <span className={`text-xs font-medium ${config.cls}`}>{config.label}</span>
      <span className="text-2xs text-muted font-mono">{version}</span>
      <span className="text-2xs text-muted">· {updatedAt}</span>
    </div>
  );
}

function NoDataPlaceholder({ text }: { text: string }) {
  return (
    <div className="text-xs text-muted/60 italic">{text}</div>
  );
}
