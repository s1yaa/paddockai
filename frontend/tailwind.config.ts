import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Core palette
        bg:        "#0A0A0B",
        "bg-2":    "#111113",
        "bg-3":    "#18181B",
        "bg-4":    "#1E1E22",
        border:    "#1E1E22",
        "border-2":"#27272A",

        // Text
        primary:   "#FFFFFF",
        secondary: "#A1A1AA",
        muted:     "#52525B",

        // Accents
        red:    "#E8001D",
        "red-dim": "rgba(232,0,29,0.15)",
        orange: "#FF8000",
        gold:   "#F59E0B",
        green:  "#22C55E",
        blue:   "#3B82F6",
        teal:   "#00D2BE",

        // Team colors
        "team-redbull":    "#1B3A6B",
        "team-mclaren":    "#FF8000",
        "team-ferrari":    "#DC0000",
        "team-mercedes":   "#00D2BE",
        "team-aston":      "#006F62",
        "team-alpine":     "#0090FF",
        "team-williams":   "#005AFF",
        "team-haas":       "#B6BABD",
        "team-rb":         "#1E3D8F",
        "team-audi":       "#BB0000",
      },
      fontFamily: {
        sans:  ["var(--font-inter)", "system-ui", "sans-serif"],
        mono:  ["var(--font-mono)", "JetBrains Mono", "monospace"],
      },
      fontSize: {
        "2xs": ["0.625rem", { lineHeight: "0.875rem" }],
      },
      borderRadius: {
        sm: "4px",
        DEFAULT: "6px",
        md: "8px",
        lg: "12px",
        xl: "16px",
      },
      boxShadow: {
        "glow-red":  "0 0 20px rgba(232, 0, 29, 0.15)",
        "glow-blue": "0 0 20px rgba(59, 130, 246, 0.15)",
        card:        "0 1px 3px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.04)",
      },
      backgroundImage: {
        "grid-pattern": "linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px)",
      },
      backgroundSize: {
        "grid": "32px 32px",
      },
      animation: {
        "pulse-slow": "pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "fade-in":    "fadeIn 0.2s ease-out",
        "slide-up":   "slideUp 0.3s ease-out",
      },
      keyframes: {
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        slideUp: {
          "0%":   { opacity: "0", transform: "translateY(8px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
      },
    },
  },
  plugins: [],
};

export default config;
