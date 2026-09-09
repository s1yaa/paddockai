import { History } from "lucide-react";
export const metadata = { title: "Prediction History — PaddockAI" };
export default function PredictionHistoryPage() {
  return <StubPage title="Prediction History" icon={<History size={20} className="text-red" />} phase={4} desc="Complete archive of prediction snapshots. See how win probabilities evolved from pre-weekend through each practice session, qualifying, and the race itself." />;
}
function StubPage({ title, icon, phase, desc }: any) {
  return (<div className="min-h-screen bg-bg"><div className="border-b border-border px-6 py-4 flex items-center gap-3">{icon}<h1 className="text-xl font-bold text-white">{title}</h1></div><div className="flex items-center justify-center p-12"><div className="text-center max-w-md"><div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full border border-border-2 bg-bg-2 mb-5"><div className="w-1.5 h-1.5 rounded-full bg-gold animate-pulse-slow" /><span className="text-xs font-semibold text-gold tracking-widest uppercase">Phase {phase}</span></div><h2 className="text-2xl font-bold text-white mb-3">{title}</h2><p className="text-sm text-secondary leading-relaxed">{desc}</p></div></div></div>);
}
