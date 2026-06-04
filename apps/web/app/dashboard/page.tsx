"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";

export default function DashboardPage() {
  const [resumeCount, setResumeCount] = useState(0);
  const [analysisCount, setAnalysisCount] = useState(0);

  useEffect(() => {
    const token = localStorage.getItem("token");

    Promise.all([
      api.get("/resumes", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }),
      api.get("/analysis/jobs", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }),
    ])
      .then(([resumes, analyses]) => {
        setResumeCount(resumes.data.length);
        setAnalysisCount(analyses.data.length);
      })
      .catch(console.error);
  }, []);

  return (
    <div className="mx-auto max-w-7xl">
      <div className="mb-10">
        <p className="mb-2 text-sm text-emerald-400">
          &gt; ARA SYSTEM v1.0
        </p>

        <h1 className="text-5xl font-bold tracking-tight">
          Recruiter Dashboard
        </h1>

        <p className="mt-3 text-gray-400">
          AI-powered resume screening terminal
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        <div className="rounded-xl border border-emerald-500/30 bg-zinc-950 p-6 backdrop-blur-sm">
          <p className="text-sm text-emerald-400">
            Total Resumes
          </p>

          <h2 className="mt-3 text-5xl font-bold">
            {resumeCount}
          </h2>
        </div>

        <div className="rounded-xl border border-emerald-500/30 bg-zinc-950 p-6 backdrop-blur-sm">
          <p className="text-sm text-emerald-400">
            Analyses Run
          </p>

          <h2 className="mt-3 text-5xl font-bold">
            {analysisCount}
          </h2>
        </div>

        <div className="rounded-xl border border-emerald-500/30 bg-zinc-950 p-6 backdrop-blur-sm">
          <p className="text-sm text-emerald-400">
            System Status
          </p>

          <h2 className="mt-3 text-3xl font-bold text-emerald-400">
            ONLINE
          </h2>
        </div>
      </div>

      <div className="mt-10 rounded-xl border border-emerald-500/20 bg-zinc-950 p-6 backdrop-blur-sm">
        <h2 className="mb-4 text-xl font-bold text-emerald-400">
          Terminal
        </h2>

        <div className="space-y-2 font-mono text-sm">
          <p>&gt; Connected to ARA backend</p>
          <p>&gt; Resumes indexed: {resumeCount}</p>
          <p>&gt; Analysis jobs processed: {analysisCount}</p>

          <p className="text-emerald-400">
            &gt; System operational
          </p>
        </div>
      </div>
    </div>
  );
}