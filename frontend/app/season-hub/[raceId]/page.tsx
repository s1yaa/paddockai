import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { getRace } from "@/lib/api";
import { formatDate, getCountryFlagByCountry, getSessionLabel } from "@/lib/utils";
import { ChevronLeft, CheckCircle, Circle, Clock, AlertCircle } from "lucide-react";
import type { SessionType, SessionStatus } from "@/types";

interface PageProps {
  params: Promise<{ raceId: string }>;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { raceId } = await params;
  const race = await getRace(raceId);
  return { title: race ? `${race.gp_name} — PaddockAI` : "Race — PaddockAI" };
}

export default async function RaceWorkspacePage({ params }: PageProps) {
  const { raceId } = await params;
  const race = await getRace(raceId);

  if (!race) {
    notFound();
  }

  const flag = getCountryFlagByCountry(race.country);
  const isActive    = race.status === "active";
  const isCompleted = race.status === "completed";

  // Sort sessions in logical order
  const SESSION_ORDER: SessionType[] = [
    "fp1", "fp2", "fp3",
    "sprint_qualifying", "sprint",
    "qualifying", "race",
  ];

  const sessions = [...(race.sessions ?? [])].sort(
    (a, b) =>
      SESSION_ORDER.indexOf(a.session_type as SessionType) -
      SESSION_ORDER.indexOf(b.session_type as SessionType)
  );

  // Determine data and prediction status per session (stub for Phase 1)
  const dataAdded = isCompleted
    ? sessions.map((s) => s.session_type)
    : [];

  return (
    <div className="min-h-screen bg-bg">
      {/* Header */}
      <div className="border-b border-border px-6 py-4">
        <div className="flex items-center gap-3 mb-3">
          <Link
            href="/season-hub"
            className="flex items-center gap-1 text-xs text-muted hover:text-secondary transition-colors"
          >
            <ChevronLeft size={14} />
            Season Hub
          </Link>
        </div>
        <div className="flex items-start justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-2xs font-mono text-muted">
                Round {String(race.round_number).padStart(2, "0")}
              </span>
              <span className="text-muted">/</span>
              <span className="text-2xs text-muted">2026 Season</span>
            </div>
            <h1 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
              <span>{flag}</span>
              {race.gp_name}
            </h1>
            {race.circuit && (
              <div className="text-sm text-secondary mt-0.5">
                {race.circuit.name}
                {race.circuit.city ? ` · ${race.circuit.city}` : ""}
                {race.circuit.country ? ` · ${race.circuit.country}` : ""}
              </div>
            )}
          </div>
          <div className="flex flex-col items-end gap-2">
            <span
              className={`badge ${
                isActive    ? "badge-active"    :
                isCompleted ? "badge-completed" :
                              "badge-upcoming"
              }`}
            >
              {isActive    && <span className="w-1.5 h-1.5 rounded-full bg-current animate-pulse-slow" />}
              {isActive ? "Race Weekend Active" : isCompleted ? "Completed" : "Upcoming"}
            </span>
            <div className="text-xs text-muted font-mono">
              {formatDate(race.date)}
            </div>
          </div>
        </div>
      </div>

      <div className="p-6 space-y-6">
        {/* Circuit info */}
        {race.circuit && (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {race.circuit.length_km && (
              <InfoCard label="Track Length" value={`${race.circuit.length_km} km`} mono />
            )}
            {race.circuit.corners && (
              <InfoCard label="Corners" value={race.circuit.corners.toString()} mono />
            )}
            {race.circuit.circuit_type && (
              <InfoCard label="Circuit Type" value={race.circuit.circuit_type} capitalize />
            )}
            {race.circuit.overtaking_difficulty && (
              <InfoCard
                label="Overtaking"
                value={`${race.circuit.overtaking_difficulty}/10`}
                mono
              />
            )}
          </div>
        )}

        {/* Weekend timeline */}
        <div className="card overflow-hidden">
          <div className="px-5 py-3.5 border-b border-border">
            <h2 className="text-sm font-semibold text-white">Weekend Timeline</h2>
          </div>

          <div className="divide-y divide-border">
            {sessions.map((session) => {
              const hasData = dataAdded.includes(session.session_type);
              const isSessionActive = session.status === "active";
              const isSessionCompleted = session.status === "completed";

              return (
                <div
                  key={session.id}
                  className="flex items-center gap-4 px-5 py-4 hover:bg-bg-2 transition-colors"
                >
                  {/* Status icon */}
                  <div className="flex-shrink-0 w-5 flex justify-center">
                    {isSessionCompleted || hasData ? (
                      <CheckCircle size={16} className="text-green" />
                    ) : isSessionActive ? (
                      <div className="w-4 h-4 rounded-full border-2 border-[#A78BFA] flex items-center justify-center">
                        <div className="w-1.5 h-1.5 rounded-full bg-[#A78BFA] animate-pulse-slow" />
                      </div>
                    ) : (
                      <Circle size={16} className="text-border-2" />
                    )}
                  </div>

                  {/* Session label */}
                  <div className="w-28 flex-shrink-0">
                    <div className="text-sm font-semibold text-white">
                      {getSessionLabel(session.session_type)}
                    </div>
                    {session.scheduled_at && (
                      <div className="text-2xs text-muted font-mono">
                        {new Date(session.scheduled_at).toLocaleDateString("en-GB", {
                          day: "numeric", month: "short",
                        })}
                      </div>
                    )}
                  </div>

                  {/* Data status */}
                  <div className="flex-1">
                    <span className={`badge ${
                      hasData || isSessionCompleted ? "badge-completed" :
                      isSessionActive ? "badge-active" :
                      "badge-waiting"
                    }`}>
                      {hasData || isSessionCompleted
                        ? "Data Available"
                        : isSessionActive
                        ? "In Progress"
                        : "Waiting"}
                    </span>
                  </div>

                  {/* Prediction status */}
                  <div className="hidden sm:flex items-center">
                    <span className={`badge ${
                      isCompleted && session.session_type !== "fp1" && session.session_type !== "fp2"
                        ? "badge-completed"
                        : "badge-waiting"
                    }`}>
                      {isCompleted && session.session_type !== "fp1" && session.session_type !== "fp2"
                        ? "Prediction Saved"
                        : "No Prediction"}
                    </span>
                  </div>

                  {/* CTA */}
                  <div className="flex-shrink-0">
                    {!isSessionCompleted && !hasData && (
                      <Link
                        href={`/data-center?race=${race.id}&session=${session.session_type}`}
                        className="text-xs text-red hover:text-red/80 transition-colors flex items-center gap-1"
                      >
                        Add Data
                      </Link>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Action panel */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <ActionCard
            title="Add Session Data"
            description="Enter practice, qualifying, or race results for this weekend."
            href={`/data-center?race=${race.id}`}
            label="Open Data Center"
            accent
          />
          <ActionCard
            title="View Predictions"
            description="See the current race prediction and all historical snapshots."
            href={`/race-predictor?race=${race.id}`}
            label="Race Predictor"
          />
        </div>

        {/* Sprint weekend note */}
        {race.has_sprint && (
          <div className="flex items-start gap-2.5 p-3.5 rounded-md border border-[#9333ea]/20 bg-[#9333ea]/5">
            <AlertCircle size={14} className="text-[#A78BFA] mt-0.5 flex-shrink-0" />
            <div className="text-xs text-[#C4B5FD]">
              <strong>Sprint Weekend</strong> — This round includes Sprint Qualifying and Sprint
              Race sessions in addition to the standard format.
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ── Sub-components ────────────────────────────────────────────────────────────

function InfoCard({
  label, value, mono, capitalize,
}: {
  label: string;
  value: string;
  mono?: boolean;
  capitalize?: boolean;
}) {
  return (
    <div className="card p-3.5">
      <div className="text-2xs text-muted uppercase tracking-widest mb-1.5">{label}</div>
      <div className={`text-base font-semibold text-white ${mono ? "font-mono" : ""} ${capitalize ? "capitalize" : ""}`}>
        {value}
      </div>
    </div>
  );
}

function ActionCard({
  title, description, href, label, accent,
}: {
  title: string;
  description: string;
  href: string;
  label: string;
  accent?: boolean;
}) {
  return (
    <Link href={href} className="block">
      <div className={`card card-hover p-4 border ${accent ? "border-red/20 hover:border-red/40" : ""} transition-colors`}>
        <div className="text-sm font-semibold text-white mb-1">{title}</div>
        <div className="text-xs text-secondary mb-3">{description}</div>
        <div className={`text-xs font-semibold ${accent ? "text-red" : "text-secondary"}`}>
          {label} →
        </div>
      </div>
    </Link>
  );
}
