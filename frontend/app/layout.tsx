import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Sidebar } from "@/components/layout/Sidebar";
import { BottomNav } from "@/components/layout/BottomNav";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

export const metadata: Metadata = {
  title: {
    default: "PaddockAI — F1 Prediction Intelligence",
    template: "%s | PaddockAI",
  },
  description:
    "Predict the weekend. Simulate the season. Understand the outcome. Professional-grade Formula 1 machine learning prediction platform.",
  keywords: ["F1", "Formula 1", "prediction", "machine learning", "motorsport", "racing"],
  authors: [{ name: "PaddockAI" }],
  openGraph: {
    title: "PaddockAI — F1 Prediction Intelligence",
    description: "Professional F1 machine learning prediction platform",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={inter.variable}>
      <body>
        <div className="page-layout">
          <Sidebar />
          <main className="main-content">
            {children}
          </main>
        </div>
        <BottomNav />
        {process.env.NEXT_PUBLIC_DEMO_MODE === "true" && (
          <div className="demo-banner">
            ● Demo Mode — Seeded 2026 Season Data
          </div>
        )}
      </body>
    </html>
  );
}
