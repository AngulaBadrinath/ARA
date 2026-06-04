export default function HomePage() {
  return (
    <main className="min-h-screen bg-black text-white">
      <div className="mx-auto max-w-7xl px-8 py-16">
        <div className="mb-6 text-green-400">&gt; ARA_SYSTEM v1.0</div>

        <h1 className="max-w-5xl text-7xl font-bold leading-tight">
          AI Resume Analysis
          <br />
          Built For Modern Hiring.
        </h1>

        <p className="mt-8 max-w-2xl text-lg text-zinc-400">
          Upload resumes, detect ATS weaknesses, discover skill gaps, and
          generate recruiter-grade insights using AI.
        </p>

        <div className="mt-10 flex gap-4">
          <button className="rounded-xl border border-green-500 px-6 py-3 text-green-400 transition hover:bg-green-500 hover:text-black">
            Upload Resume
          </button>

          <button className="rounded-xl border border-zinc-700 px-6 py-3 hover:border-zinc-500">
            Analysis History
          </button>
        </div>

        <div className="mt-24 grid gap-6 md:grid-cols-3">
          <div className="rounded-2xl border border-zinc-800 bg-zinc-950 p-6">
            <div className="mb-2 text-green-400">ATS Score</div>

            <div className="text-5xl font-bold">85%</div>
          </div>

          <div className="rounded-2xl border border-zinc-800 bg-zinc-950 p-6">
            <div className="mb-2 text-green-400">Skills Found</div>

            <div className="text-5xl font-bold">18</div>
          </div>

          <div className="rounded-2xl border border-zinc-800 bg-zinc-950 p-6">
            <div className="mb-2 text-green-400">Missing Skills</div>

            <div className="text-5xl font-bold">3</div>
          </div>
        </div>
      </div>
    </main>
  );
}
