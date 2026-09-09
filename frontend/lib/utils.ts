import { type ClassValue, clsx } from "clsx";

export function cn(...inputs: ClassValue[]) {
  return clsx(inputs);
}

export function formatDate(dateStr: string | null): string {
  if (!dateStr) return "TBD";
  const d = new Date(dateStr + "T00:00:00");
  return d.toLocaleDateString("en-GB", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}

export function formatDateShort(dateStr: string | null): string {
  if (!dateStr) return "TBD";
  const d = new Date(dateStr + "T00:00:00");
  return d.toLocaleDateString("en-GB", { day: "numeric", month: "short" });
}

export function getCountryFlag(countryCode: string | null): string {
  if (!countryCode) return "🏁";
  const COUNTRY_FLAGS: Record<string, string> = {
    AUS: "🇦🇺", CHN: "🇨🇳", JPN: "🇯🇵", BHR: "🇧🇭", SAU: "🇸🇦",
    USA: "🇺🇸", ITA: "🇮🇹", MON: "🇲🇨", ESP: "🇪🇸", CAN: "🇨🇦",
    AUT: "🇦🇹", GBR: "🇬🇧", BEL: "🇧🇪", HUN: "🇭🇺", NLD: "🇳🇱",
    SGP: "🇸🇬", AZE: "🇦🇿", MEX: "🇲🇽", BRA: "🇧🇷", QAT: "🇶🇦",
    UAE: "🇦🇪",
  };
  return COUNTRY_FLAGS[countryCode.toUpperCase()] ?? "🏁";
}

export function getCountryFlagByCountry(country: string | null): string {
  if (!country) return "🏁";
  const map: Record<string, string> = {
    "Australia": "🇦🇺", "China": "🇨🇳", "Japan": "🇯🇵", "Bahrain": "🇧🇭",
    "Saudi Arabia": "🇸🇦", "United States": "🇺🇸", "Italy": "🇮🇹",
    "Monaco": "🇲🇨", "Spain": "🇪🇸", "Canada": "🇨🇦", "Austria": "🇦🇹",
    "United Kingdom": "🇬🇧", "Belgium": "🇧🇪", "Hungary": "🇭🇺",
    "Netherlands": "🇳🇱", "Singapore": "🇸🇬", "Azerbaijan": "🇦🇿",
    "Mexico": "🇲🇽", "Brazil": "🇧🇷", "Qatar": "🇶🇦",
    "United Arab Emirates": "🇦🇪",
  };
  return map[country] ?? "🏁";
}

export function getRaceStatusBadge(status: string) {
  switch (status) {
    case "completed": return { label: "Completed", cls: "badge-completed" };
    case "active":    return { label: "Active",    cls: "badge-active" };
    case "upcoming":  return { label: "Upcoming",  cls: "badge-upcoming" };
    default:          return { label: status,      cls: "badge-waiting" };
  }
}

export function getSessionLabel(type: string): string {
  const labels: Record<string, string> = {
    fp1: "FP1", fp2: "FP2", fp3: "FP3",
    qualifying: "Qualifying", race: "Race",
    sprint_qualifying: "Sprint Quali", sprint: "Sprint",
  };
  return labels[type] ?? type.toUpperCase();
}

export function formatPoints(pts: number): string {
  return pts % 1 === 0 ? pts.toString() : pts.toFixed(1);
}

export function formatProbability(prob: number): string {
  return `${(prob * 100).toFixed(1)}%`;
}

export function getRoundLabel(n: number): string {
  return String(n).padStart(2, "0");
}

export function daysUntil(dateStr: string | null): number {
  if (!dateStr) return 999;
  const now = new Date();
  const race = new Date(dateStr + "T00:00:00");
  return Math.ceil((race.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));
}
