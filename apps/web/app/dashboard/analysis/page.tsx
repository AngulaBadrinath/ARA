"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";

interface AnalysisJob {
  job_id: string;
  resume_id: string;
  resume_title: string | null;
  status: string;
  score: number | null;
  created_at: string;
}

export default function AnalysisPage() {
  const [jobs, setJobs] = useState<AnalysisJob[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      setError("Not authenticated. Please log in.");
      setLoading(false);
      return;
    }

    api
      .get("/analysis/jobs", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((res) => {
        setJobs(res.data);
      })
      .catch((err) => {
        console.error(err);
        setError("Failed to load analysis jobs.");
      })
      .finally(() => setLoading(false));
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case "completed": return "text-emerald-400";
      case "processing": return "text-yellow-400";
      case "failed": return "text-red-400";
      default: return "text-gray-400";
    }
  };

  return (
    <div className="mx-auto max-w-7xl">
      <div className="mb-10">
        <p className="mb-2 text-sm text-emerald-400">{">"} ANALYSIS HISTORY</p>
        <h1 className="text-5xl font-bold">Analysis Center</h1>
        <p className="mt-2 text-gray-400">Review completed AI evaluations</p>
      </div>

      {loading && (
        <div className="rounded-xl border border-emerald-500/20 bg-zinc-950 p-8">
          <p className="text-gray-400 animate-pulse">Loading analyses...</p>
        </div>
      )}

      {error && (
        <div className="rounded-xl border border-red-500/20 bg-zinc-950 p-8">
          <p className="text-red-400">{error}</p>
        </div>
      )}

      {!loading && !error && jobs.length === 0 && (
        <div className="rounded-xl border border-emerald-500/20 bg-zinc-950 p-8">
          <p className="text-gray-400">No analyses run yet. Upload a resume and analyze it.</p>
        </div>
      )}

      {!loading && !error && jobs.length > 0 && (
        <div className="grid gap-4">
          {jobs.map((job) => (
            <div
              key={job.job_id}
              className="rounded-xl border border-emerald-500/20 bg-zinc-950 p-6 transition hover:border-emerald-500/50"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h2 className="text-lg font-bold">
                    {job.resume_title || "Untitled Resume"}
                  </h2>
                  <p className="mt-1 text-xs font-mono text-gray-500">
                    Job: {job.job_id.slice(0, 8)}...
                  </p>
                  <p className="mt-1 text-xs text-gray-500">
                    {new Date(job.created_at).toLocaleString()}
                  </p>
                </div>
                <div className="text-right">
                  <p className={`text-sm font-medium ${getStatusColor(job.status)}`}>
                    {job.status.toUpperCase()}
                  </p>
                  {job.score !== null && (
                    <p className="mt-1 text-2xl font-bold text-emerald-400">
                      {job.score}/100
                    </p>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
