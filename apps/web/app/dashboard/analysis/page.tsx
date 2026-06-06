"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";

export default function AnalysisPage() {
  const [jobs, setJobs] = useState<any[]>([]);

  useEffect(() => {
    const token = localStorage.getItem("token");

    api
      .get("/analysis/jobs", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((res) => {
        setJobs(res.data);
      })
      .catch(console.error);
  }, []);

  return (
    <div className="mx-auto max-w-7xl">
      <div className="mb-10">
        <p className="mb-2 text-sm text-emerald-400">&gt; ANALYSIS HISTORY</p>

        <h1 className="text-5xl font-bold">Analysis Center</h1>

        <p className="mt-2 text-gray-400">Review completed AI evaluations</p>
      </div>

      <div className="space-y-4">
        {jobs.map((job) => (
          <div
            key={job.job_id}
            className="rounded-xl border border-emerald-500/20 bg-zinc-950 p-6"
          >
            <p className="font-mono text-sm text-emerald-400">{job.job_id}</p>

            <p className="mt-2">Resume ID: {job.resume_id}</p>

            <p className="text-gray-400">Status: {job.status}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
