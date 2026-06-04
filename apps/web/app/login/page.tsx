"use client";

import { useState } from "react";
import { api } from "@/lib/api";
import { saveToken } from "@/lib/auth";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    try {
      const response = await api.post("/auth/login", {
        email,
        password,
      });

      saveToken(response.data.access_token);

      router.push("/dashboard");
    } catch (error) {
      console.error(error);
      alert("Login failed");
    }
  };

  return (
    <main className="flex min-h-screen items-center justify-center bg-black text-white">
      <div className="w-full max-w-md rounded-2xl border border-zinc-800 bg-zinc-950 p-8">
        <div className="mb-6 text-green-400">&gt; LOGIN</div>

        <h1 className="mb-6 text-3xl font-bold">Welcome Back</h1>

        <div className="space-y-4">
          <input
            className="w-full rounded-lg border border-zinc-700 bg-black p-3"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <input
            type="password"
            className="w-full rounded-lg border border-zinc-700 bg-black p-3"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <button
            onClick={handleLogin}
            className="w-full rounded-lg border border-green-500 p-3 text-green-400 hover:bg-green-500 hover:text-black"
          >
            Login
          </button>
        </div>
      </div>
    </main>
  );
}
