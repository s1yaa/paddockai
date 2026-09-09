import Link from "next/link";

export default function NotFound() {
  return (
    <div className="min-h-screen bg-bg flex items-center justify-center p-6">
      <div className="text-center">
        <div className="text-8xl font-black font-mono text-border-2 mb-4">404</div>
        <h1 className="text-2xl font-bold text-white mb-2">Page not found</h1>
        <p className="text-sm text-secondary mb-6">
          The page you are looking for does not exist.
        </p>
        <Link
          href="/"
          className="inline-flex items-center gap-2 px-4 py-2 bg-bg-2 border border-border rounded-md text-sm text-secondary hover:text-white hover:border-border-2 transition-colors"
        >
          ← Back to Overview
        </Link>
      </div>
    </div>
  );
}
