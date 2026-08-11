import React from 'react';
import { useAuth } from '../context/AuthContext';

export const Profile: React.FC = () => {
  const { user } = useAuth();
  const username = user?.username || 'PratyakshBisht';

  return (
    <div className="max-w-4xl mx-auto px-4 py-10 space-y-8">
      <div className="p-8 rounded-3xl border border-slate-800 bg-slate-900/60 backdrop-blur-xl">
        <div className="flex flex-col sm:flex-row items-center sm:items-start gap-6">
          <div className="h-24 w-24 rounded-2xl bg-gradient-to-tr from-teal-500 to-indigo-600 flex items-center justify-center text-4xl font-extrabold text-white shadow-xl shadow-teal-500/20">
            {username.charAt(0).toUpperCase()}
          </div>

          <div className="flex-1 text-center sm:text-left space-y-2">
            <div className="flex flex-col sm:flex-row sm:items-center gap-3">
              <h1 className="text-2xl font-bold text-white">
                {user?.name || username}
              </h1>
              <span className="self-center sm:self-auto px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                Active Candidate
              </span>
            </div>
            <p className="text-sm font-mono text-teal-400">@{username}</p>
            <p className="text-sm text-slate-400 max-w-xl">
              Software Engineer specializing in FastAPI, React/TypeScript, PostgreSQL, and autonomous AI systems.
            </p>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-slate-800/80 grid grid-cols-1 sm:grid-cols-3 gap-4 text-center">
          <div className="p-4 rounded-xl bg-slate-950/50 border border-slate-800">
            <span className="block text-2xl font-black text-white">87.5</span>
            <span className="text-xs text-slate-400">Signal Rating</span>
          </div>
          <div className="p-4 rounded-xl bg-slate-950/50 border border-slate-800">
            <span className="block text-2xl font-black text-teal-400">Top 8%</span>
            <span className="text-xs text-slate-400">Global Percentile</span>
          </div>
          <div className="p-4 rounded-xl bg-slate-950/50 border border-slate-800">
            <span className="block text-2xl font-black text-emerald-400">Verified</span>
            <span className="text-xs text-slate-400">GitHub Identity</span>
          </div>
        </div>
      </div>
    </div>
  );
};
