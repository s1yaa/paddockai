"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard, Calendar, TrendingUp, Timer,
  Trophy, Building2, Users, Factory, MapPin,
  FlaskConical, History, BarChart3, Rewind, Database,
  ChevronRight,
} from "lucide-react";
import { cn } from "@/lib/utils";

const NAV_GROUPS = [
  {
    label: null,
    items: [
      { href: "/",            label: "Overview",          icon: LayoutDashboard },
      { href: "/season-hub",  label: "Season Hub",        icon: Calendar },
    ],
  },
  {
    label: "PREDICTIONS",
    items: [
      { href: "/race-predictor",       label: "Race Predictor",      icon: TrendingUp },
      { href: "/qualifying-predictor", label: "Qualifying Predictor",icon: Timer },
      { href: "/championship",         label: "Championship",         icon: Trophy },
      { href: "/prediction-history",   label: "Prediction History",   icon: History },
    ],
  },
  {
    label: "INTELLIGENCE",
    items: [
      { href: "/drivers",      label: "Drivers",      icon: Users },
      { href: "/constructors", label: "Constructors", icon: Building2 },
      { href: "/teams",        label: "Teams",        icon: Factory },
      { href: "/circuits",     label: "Circuits",     icon: MapPin },
    ],
  },
  {
    label: "TOOLS",
    items: [
      { href: "/what-if-lab",       label: "What-If Lab",      icon: FlaskConical },
      { href: "/model-lab",         label: "Model Lab",        icon: BarChart3 },
      { href: "/historical-replay", label: "Historical Replay",icon: Rewind },
      { href: "/data-center",       label: "Data Center",      icon: Database },
    ],
  },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <nav className="sidebar flex flex-col">
      {/* Logo */}
      <div className="px-4 py-5 border-b border-border flex-shrink-0">
        <Link href="/" className="flex items-center gap-2.5 group">
          <div className="relative w-7 h-7 flex items-center justify-center">
            {/* F1-style logo mark */}
            <div className="w-5 h-5 border-2 border-red rotate-45 group-hover:border-red transition-colors" />
            <div className="absolute w-2 h-2 bg-red rotate-45" />
          </div>
          <div>
            <div className="text-sm font-bold tracking-wider text-white leading-none">
              PADDOCK<span className="text-red">AI</span>
            </div>
            <div className="text-2xs text-muted tracking-widest uppercase leading-none mt-0.5">
              F1 Intelligence
            </div>
          </div>
        </Link>
      </div>

      {/* Navigation */}
      <div className="flex-1 overflow-y-auto py-3 px-2">
        {NAV_GROUPS.map((group, gi) => (
          <div key={gi} className={cn("mb-3", gi > 0 && "mt-1")}>
            {group.label && (
              <div className="px-2 mb-1 mt-3">
                <span className="text-2xs font-semibold tracking-widest text-muted uppercase">
                  {group.label}
                </span>
              </div>
            )}
            {group.items.map((item) => {
              const isActive =
                item.href === "/" ? pathname === "/" : pathname.startsWith(item.href);
              const Icon = item.icon;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={cn("nav-item", isActive && "active")}
                >
                  <Icon
                    size={15}
                    className={cn(
                      "nav-icon flex-shrink-0 transition-colors",
                      isActive ? "text-red" : "text-muted"
                    )}
                  />
                  <span className="truncate">{item.label}</span>
                </Link>
              );
            })}
          </div>
        ))}
      </div>

      {/* Footer */}
      <div className="px-4 py-3 border-t border-border flex-shrink-0">
        <div className="flex items-center justify-between">
          <div>
            <div className="text-2xs text-muted uppercase tracking-widest">Season</div>
            <div className="text-xs font-semibold text-secondary font-mono">2026 F1</div>
          </div>
          <div className="flex items-center gap-1.5">
            <div className="w-1.5 h-1.5 rounded-full bg-green animate-pulse-slow" />
            <span className="text-2xs text-green">Live</span>
          </div>
        </div>
      </div>
    </nav>
  );
}
