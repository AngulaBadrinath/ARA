"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";

interface Resume {
  id: string;
  title: string;
  filename: string;
  created_at: string;
}

export default function ResumesPage() {
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchResumes = async () => {
    try {
      const token = localStorage.getItem("token");

      const res = await api.get("/resumes", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setResumes(res.data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchResumes();
  }, []);

  const deleteResume = async (id: string) => {
    try {
      const token = localStorage.getItem("token");

      await api.delete(`/resumes/${id}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setResumes((prev) => prev.filter((resume) => resume.id !== id));
    } catch (error) {
      console.error(error);
      alert("Failed to delete resume");
    }
  };

  const analyzeResume = async (resumeId: string) => {
    try {
      const token = localStorage.getItem("token");

      await api.post(
        "/analysis/jobs",
        {
          resume_id: resumeId,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      );

      window.location.href = "/dashboard/analysis";
    } catch (error) {
      console.error(error);
      alert("Failed to start analysis");
    }
  };

  return (
    <div className="mx-auto max-w-7xl">
      <div className="mb-10 flex items-start justify-between">
        <div>
          <p className="mb-2 text-sm text-emerald-400">&gt; RESUME DATABASE</p>

          <h1 className="text-5xl font-bold">Resume Vault</h1>

          <p className="mt-3 text-gray-400">
            Indexed resumes available for analysis
          </p>
        </div>

        <button
          onClick={() => {
            window.location.href = "/dashboard/upload";
          }}
          className="rounded-lg border border-emerald-500 px-6 py-3 text-emerald-400 transition hover:bg-emerald-500 hover:text-black"
        >
          Upload Resume
        </button>
      </div>

      {loading ? (
        <div className="rounded-xl border border-emerald-500/20 bg-zinc-950 p-8">
          Loading resumes...
        </div>
      ) : resumes.length === 0 ? (
        <div className="rounded-xl border border-emerald-500/20 bg-zinc-950 p-8">
          <p className="text-gray-400">No resumes uploaded yet.</p>
        </div>
      ) : (
        <div className="grid gap-6">
          {resumes.map((resume) => (
            <div
              key={resume.id}
              className="rounded-xl border border-emerald-500/20 bg-zinc-950 p-6 transition hover:border-emerald-500/50"
            >
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-xl font-bold">{resume.title}</h2>

                  <p className="mt-1 text-sm text-gray-400">
                    {resume.filename}
                  </p>

                  <p className="mt-2 text-xs text-gray-500">
                    Uploaded {new Date(resume.created_at).toLocaleString()}
                  </p>
                </div>

                <div className="flex gap-3">
                  <button
                    onClick={() => analyzeResume(resume.id)}
                    className="rounded-lg border border-emerald-500 px-4 py-2 text-emerald-400 transition hover:bg-emerald-500 hover:text-black"
                  >
                    Analyze
                  </button>

                  <button
                    onClick={() => deleteResume(resume.id)}
                    className="rounded-lg border border-red-500 px-4 py-2 text-red-400 transition hover:bg-red-500 hover:text-white"
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
