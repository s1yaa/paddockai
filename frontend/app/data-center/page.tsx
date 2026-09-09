import type { Metadata } from "next";
import { Database, Upload, RefreshCw, Plus, CheckCircle } from "lucide-react";

export const metadata: Metadata = { title: "Data Center — PaddockAI" };

const SESSION_TYPES = [
  { value: "fp1",               label: "Free Practice 1 (FP1)" },
  { value: "fp2",               label: "Free Practice 2 (FP2)" },
  { value: "fp3",               label: "Free Practice 3 (FP3)" },
  { value: "sprint_qualifying", label: "Sprint Qualifying" },
  { value: "sprint",            label: "Sprint Race" },
  { value: "qualifying",        label: "Qualifying" },
  { value: "race",              label: "Race" },
];

export default function DataCenterPage() {
  return (
    <div className="min-h-screen bg-bg">
      {/* Header */}
      <div className="border-b border-border px-6 py-4">
        <div className="flex items-center gap-3">
          <Database size={18} className="text-red" />
          <div>
            <div className="text-2xs text-muted uppercase tracking-widest mb-0.5">
              Input & Manage
            </div>
            <h1 className="text-xl font-bold text-white tracking-tight">Data Center</h1>
          </div>
        </div>
      </div>

      <div className="p-6 space-y-6">

        {/* Status cards */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <DataStatusCard
            label="Last Data Update"
            value="2 hours ago"
            sub="British GP — Race Results"
            icon={<CheckCircle size={16} className="text-green" />}
          />
          <DataStatusCard
            label="Data Freshness"
            value="12 / 12 races"
            sub="2026 season complete through R12"
            icon={<Database size={16} className="text-blue" />}
          />
          <DataStatusCard
            label="Next Session"
            value="FP1 · Spa"
            sub="Belgian GP · July 25"
            icon={<RefreshCw size={16} className="text-gold" />}
          />
        </div>

        {/* Main data entry area */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">

          {/* Quick add form */}
          <div className="lg:col-span-2 space-y-4">
            <div className="card overflow-hidden">
              <div className="px-5 py-3.5 border-b border-border">
                <h2 className="text-sm font-semibold text-white flex items-center gap-2">
                  <Plus size={14} className="text-red" />
                  Add Session Results
                </h2>
              </div>
              <div className="p-5 space-y-4">
                {/* Race + Session selectors */}
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-2xs text-muted uppercase tracking-widest mb-1.5">
                      Grand Prix
                    </label>
                    <select className="w-full bg-bg-3 border border-border rounded-md px-3 py-2 text-sm text-white focus:border-red/50 focus:outline-none transition-colors">
                      <option value="">Select race...</option>
                      <option value="belgian-gp">Round 13 — Belgian GP</option>
                      <option value="hungarian-gp">Round 14 — Hungarian GP</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-2xs text-muted uppercase tracking-widest mb-1.5">
                      Session
                    </label>
                    <select className="w-full bg-bg-3 border border-border rounded-md px-3 py-2 text-sm text-white focus:border-red/50 focus:outline-none transition-colors">
                      {SESSION_TYPES.map((s) => (
                        <option key={s.value} value={s.value}>{s.label}</option>
                      ))}
                    </select>
                  </div>
                </div>

                {/* Phase 2 notice */}
                <div className="rounded-md border border-border-2 bg-bg-2 p-4">
                  <div className="flex items-start gap-3">
                    <div className="w-1.5 h-1.5 rounded-full bg-gold mt-1.5 flex-shrink-0" />
                    <div>
                      <div className="text-sm font-medium text-white mb-1">
                        Phase 2 Feature
                      </div>
                      <p className="text-xs text-secondary leading-relaxed">
                        Full manual data entry forms (driver rows, lap times, positions) and 
                        CSV bulk upload are coming in Phase 2. The session selector is connected 
                        to the live database — race and session choices will populate dynamically.
                      </p>
                    </div>
                  </div>
                </div>

                {/* Entry method tabs */}
                <div>
                  <div className="text-2xs text-muted uppercase tracking-widest mb-2">
                    Entry Method
                  </div>
                  <div className="flex gap-2">
                    <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-bg-3 border border-red/30 text-xs font-medium text-red">
                      <Plus size={12} />
                      Manual Entry
                    </button>
                    <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-bg-3 border border-border text-xs font-medium text-muted hover:text-secondary hover:border-border-2 transition-colors">
                      <Upload size={12} />
                      CSV Upload
                    </button>
                    <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-bg-3 border border-border text-xs font-medium text-muted hover:text-secondary hover:border-border-2 transition-colors">
                      <RefreshCw size={12} />
                      OpenF1 API
                    </button>
                  </div>
                </div>

                {/* CSV upload zone */}
                <div className="border-2 border-dashed border-border-2 rounded-lg p-8 text-center hover:border-border transition-colors cursor-pointer">
                  <Upload size={24} className="text-muted mx-auto mb-2" />
                  <div className="text-sm text-secondary mb-1">
                    Drop a CSV file here
                  </div>
                  <div className="text-xs text-muted">
                    or click to browse
                  </div>
                  <div className="mt-3 text-2xs text-muted/60">
                    Supported: practice, qualifying, race result CSVs
                  </div>
                </div>

                <button
                  disabled
                  className="w-full py-2.5 rounded-md bg-red/10 border border-red/20 text-sm font-semibold text-red/50 cursor-not-allowed"
                >
                  Save Results — Coming Phase 2
                </button>
              </div>
            </div>
          </div>

          {/* Sidebar info */}
          <div className="space-y-4">
            <div className="card p-4">
              <h3 className="text-sm font-semibold text-white mb-3">Data Pipeline</h3>
              <div className="space-y-2.5">
                {[
                  { step: "1", label: "Select race & session", done: true },
                  { step: "2", label: "Enter or upload results", done: false },
                  { step: "3", label: "Validate data", done: false },
                  { step: "4", label: "Update features", done: false },
                  { step: "5", label: "Refresh model", done: false },
                  { step: "6", label: "New prediction ready", done: false },
                ].map((item) => (
                  <div key={item.step} className="flex items-center gap-2.5">
                    <div className={`w-5 h-5 rounded-full flex items-center justify-center flex-shrink-0 text-2xs font-bold ${
                      item.done
                        ? "bg-green/15 text-green"
                        : "bg-bg-3 text-muted"
                    }`}>
                      {item.step}
                    </div>
                    <div className={`text-xs ${item.done ? "text-secondary" : "text-muted"}`}>
                      {item.label}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="card p-4">
              <h3 className="text-sm font-semibold text-white mb-3">Data Sources</h3>
              <div className="space-y-2">
                {[
                  { src: "OpenF1 API", status: "Ready",     cls: "text-green" },
                  { src: "Manual CSV", status: "Phase 2",   cls: "text-gold" },
                  { src: "FastF1",     status: "Phase 11",  cls: "text-muted" },
                ].map((s) => (
                  <div key={s.src} className="flex items-center justify-between">
                    <span className="text-xs text-secondary">{s.src}</span>
                    <span className={`text-2xs font-medium ${s.cls}`}>{s.status}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="card p-4">
              <h3 className="text-sm font-semibold text-white mb-3">Validation Rules</h3>
              <ul className="space-y-1.5 text-xs text-muted">
                <li>• Driver must exist in database</li>
                <li>• Constructor must be assigned</li>
                <li>• No duplicate positions</li>
                <li>• Position range 1–20</li>
                <li>• Points match position</li>
                <li>• No future race data</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function DataStatusCard({
  label, value, sub, icon,
}: {
  label: string;
  value: string;
  sub: string;
  icon: React.ReactNode;
}) {
  return (
    <div className="card p-4">
      <div className="flex items-start justify-between mb-2">
        <div className="text-2xs text-muted uppercase tracking-widest">{label}</div>
        {icon}
      </div>
      <div className="text-base font-bold text-white">{value}</div>
      <div className="text-xs text-muted mt-0.5">{sub}</div>
    </div>
  );
}
