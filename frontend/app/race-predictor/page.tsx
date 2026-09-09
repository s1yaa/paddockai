import type { Metadata } from "next";
import { TrendingUp } from "lucide-react";

export const metadata: Metadata = { title: "Race Predictor — PaddockAI" };

export default function RacePredictorPage() {
  return <ComingSoonPage title="Race Predictor" icon={<TrendingUp size={20} className="text-red" />} phase={4} description="Full predicted finishing order with win/podium/DNF probabilities, SHAP explanations, and per-driver position distribution charts." />;
}

function ComingSoonPage({ title, icon, phase, description }: { title: string; icon: React.ReactNode; phase: number; description: string }) {
  return (
    <div className="min-h-screen bg-bg">
      <div className="border-b border-border px-6 py-4">
        <div className="flex items-center gap-3">
          {icon}
          <h1 className="text-xl font-bold text-white">{title}</h1>
        </div>
      </div>
      <div className="flex items-center justify-center p-12">
        <div className="text-center max-w-md">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full border border-border-2 bg-bg-2 mb-6">
            <div className="w-1.5 h-1.5 rounded-full bg-gold animate-pulse-slow" />
            <span className="text-xs font-semibold text-gold tracking-widest uppercase">Phase {phase}</span>
          </div>
          <h2 className="text-2xl font-bold text-white mb-3">{title}</h2>
          <p className="text-sm text-secondary leading-relaxed mb-6">{description}</p>
          <div className="text-2xs text-muted uppercase tracking-widest">Coming after Phase 1 is verified</div>
        </div>
      </div>
    </div>
  );
}
