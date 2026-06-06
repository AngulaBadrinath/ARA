"use client";

import { useState } from "react";
import { api } from "@/lib/api";

export default function UploadPage() {
  const [title, setTitle] = useState("");
  const [file, setFile] = useState<File | null>(null);

  const uploadResume = async () => {
    if (!file) return;

    const token = localStorage.getItem("token");

    const formData = new FormData();

    formData.append("title", title);
    formData.append("file", file);

    try {
      await api.post("/resumes/upload", formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "multipart/form-data",
        },
      });

      window.location.href = "/dashboard/resumes";
    } catch (err) {
      console.error(err);
      alert("Upload failed");
    }
  };

  return (
    <div className="mx-auto max-w-4xl">
      <p className="mb-2 text-sm text-emerald-400">&gt; RESUME UPLOADER</p>

      <h1 className="text-5xl font-bold">Upload Resume</h1>

      <p className="mt-3 text-gray-400">Add a new candidate profile</p>

      <div className="mt-10 rounded-xl border border-emerald-500/20 bg-zinc-950 p-8">
        <div className="space-y-6">
          <input
            type="text"
            placeholder="Resume Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full rounded-lg border border-emerald-500/20 bg-black p-4 outline-none"
          />

          <input
            type="file"
            accept=".pdf"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className="w-full rounded-lg border border-emerald-500/20 bg-black p-4"
          />

          <button
            onClick={uploadResume}
            className="rounded-lg border border-emerald-500 px-6 py-3 text-emerald-400 transition hover:bg-emerald-500 hover:text-black"
          >
            Upload Resume
          </button>
        </div>
      </div>
    </div>
  );
}
