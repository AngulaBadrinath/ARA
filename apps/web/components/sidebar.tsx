"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Sidebar() {
  const pathname = usePathname();

  const linkClass = (href: string) =>
    `block rounded-lg border p-3 transition ${
      pathname === href
        ? "border-emerald-400 bg-emerald-500/10 text-emerald-400"
        : "border-emerald-500/20 text-white hover:border-emerald-400 hover:bg-emerald-500/5"
    }`;

  return (
    <aside className="w-64 border-r border-emerald-500/20 bg-black p-6">
      <div className="mb-10">
        <p className="text-xs text-emerald-400">&gt; ARA SYSTEM</p>

        <h2 className="mt-2 text-2xl font-bold text-white">ARA</h2>

        <p className="mt-1 text-xs text-gray-500">Recruiter Terminal</p>
      </div>

      <nav className="space-y-3">
        <Link href="/dashboard" className={linkClass("/dashboard")}>
          Dashboard
        </Link>

        <Link
          href="/dashboard/resumes"
          className={linkClass("/dashboard/resumes")}
        >
          Resumes
        </Link>

        <Link
          href="/dashboard/analysis"
          className={linkClass("/dashboard/analysis")}
        >
          Analysis
        </Link>

        <button
          className="mt-6 w-full rounded-lg border border-red-500/30 p-3 text-left text-red-400 transition hover:bg-red-500/10"
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
