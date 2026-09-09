"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard, Calendar, TrendingUp, Trophy, Database,
} from "lucide-react";
import { cn } from "@/lib/utils";

const MOBILE_NAV = [
  { href: "/",           label: "Overview", icon: LayoutDashboard },
  { href: "/season-hub", label: "Season",   icon: Calendar },
  { href: "/race-predictor", label: "Predict",  icon: TrendingUp },
  { href: "/championship",   label: "Champ",    icon: Trophy },
  { href: "/data-center",    label: "Data",     icon: Database },
];

export function BottomNav() {
  const pathname = usePathname();

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-50 lg:hidden bg-bg border-t border-border">
      <div className="flex items-center justify-around h-16 px-2">
        {MOBILE_NAV.map((item) => {
          const isActive =
            item.href === "/" ? pathname === "/" : pathname.startsWith(item.href);
          const Icon = item.icon;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex flex-col items-center gap-1 flex-1 py-2 transition-colors",
                isActive ? "text-white" : "text-muted"
              )}
            >
              <Icon
                size={20}
                className={cn(isActive ? "text-red" : "text-muted")}
              />
              <span className="text-2xs font-medium tracking-wide">
                {item.label}
              </span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
