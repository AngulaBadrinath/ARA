import { Button } from "@/components/ui/button";

export default function HomePage() {
  return (
    <main className="min-h-screen">
      <div className="mx-auto flex max-w-3xl flex-col gap-8 px-6 py-16">
        <header className="space-y-2">
          <p className="text-sm font-medium text-muted-foreground">AI Resume Analyzer</p>
          <h1 className="text-4xl font-semibold tracking-tight">Analyze resumes with confidence</h1>
          <p className="text-muted-foreground">
            Upload a resume, run async AI analysis, and review structured feedback. Business logic
            is not wired yet — this is the application scaffold.
          </p>
        </header>

        <section className="rounded-xl border bg-card p-6 text-card-foreground shadow-sm">
          <h2 className="mb-2 text-lg font-medium">Getting started</h2>
          <ol className="list-decimal space-y-1 pl-5 text-sm text-muted-foreground">
            <li>Start infrastructure: <code className="rounded bg-muted px-1">make up</code></li>
            <li>Run migrations: <code className="rounded bg-muted px-1">make migrate</code></li>
            <li>API docs: <code className="rounded bg-muted px-1">http://localhost:8000/docs</code></li>
          </ol>
          <div className="mt-4 flex gap-3">
            <Button disabled>Upload resume</Button>
            <Button variant="outline" disabled>
              View analyses
            </Button>
          </div>
        </section>
      </div>
    </main>
  );
}
