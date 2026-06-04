"use client";

import Link from "next/link";

export default function Sidebar() {
  return (
    <aside className="w-64 border-r border-emerald-500/20 bg-black p-6">
      <div className="mb-10">
        <p className="text-xs text-emerald-400">
          &gt; ARA SYSTEM
        </p>

        <h2 className="mt-2 text-2xl font-bold text-white">
          ARA
        </h2>
      </div>

      <nav className="space-y-3">
        <Link
          href="/dashboard"
          className="block rounded border border-emerald-500/20 p-3 hover:border-emerald-400"
        >
          Dashboard
        </Link>

        <Link
          href="/resumes"
          className="block rounded border border-emerald-500/20 p-3 hover:border-emerald-400"
        >
          Resumes
        </Link>

        <Link
          href="/analysis"
          className="block rounded border border-emerald-500/20 p-3 hover:border-emerald-400"
        >
          Analysis
        </Link>

        <button
          className="w-full rounded border border-red-500/30 p-3 text-left text-red-400"
          onClick={() => {
            localStorage.removeItem("token");
            window.location.href = "/login";
          }}
        >
          Logout
        </button>
      </nav>
    </aside>
  );
}