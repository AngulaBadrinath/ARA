"use client";

import { useState } from "react";
import { api } from "@/lib/api";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const uploadResume = async () => {
    if (!file) {
      setError("Please select a PDF file.");
      return;
    }

    setUploading(true);
    setError(null);
    setSuccess(null);

    const token = localStorage.getItem("token");

    if (!token) {
      setError("Not authenticated. Please log in.");
      setUploading(false);
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await api.post("/resumes/upload", formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "multipart/form-data",
        },
      });

      setSuccess(`Uploaded "${res.data.filename}" (${res.data.characters} characters extracted)`);

      setTimeout(() => {
        window.location.href = "/dashboard/resumes";
      }, 1500);
    } catch (err: any) {
      console.error(err);
      setError(err?.response?.data?.detail || "Upload failed. Please try again.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="mx-auto max-w-4xl">
      <p className="mb-2 text-sm text-emerald-400">{">"} RESUME UPLOADER</p>
      <h1 className="text-5xl font-bold">Upload Resume</h1>
      <p className="mt-3 text-gray-400">Add a new candidate profile</p>

      <div className="mt-10 rounded-xl border border-emerald-500/20 bg-zinc-950 p-8">
        <div className="space-y-6">
          <div>
            <label className="mb-2 block text-sm text-gray-400">PDF File</label>
            <input
              type="file"
              accept=".pdf"
              onChange={(e) => {
                setFile(e.target.files?.[0] || null);
                setError(null);
                setSuccess(null);
              }}
              className="w-full rounded-lg border border-emerald-500/20 bg-black p-4 text-sm file:mr-4 file:rounded file:border-0 file:bg-emerald-500/10 file:px-4 file:py-2 file:text-sm file:text-emerald-400 hover:file:bg-emerald-500/20"
            />
          </div>

          {error && (
            <div className="rounded-lg border border-red-500/20 bg-red-500/5 p-4">
              <p className="text-sm text-red-400">{error}</p>
            </div>
          )}

          {success && (
            <div className="rounded-lg border border-emerald-500/20 bg-emerald-500/5 p-4">
              <p className="text-sm text-emerald-400">{success}</p>
            </div>
          )}

          <button
            onClick={uploadResume}
            disabled={!file || uploading}
            className="rounded-lg border border-emerald-500 px-6 py-3 text-emerald-400 transition hover:bg-emerald-500 hover:text-black disabled:cursor-not-allowed disabled:opacity-50"
          >
            {uploading ? "Uploading..." : "Upload Resume"}
          </button>
        </div>
      </div>
    </div>
  );
}
