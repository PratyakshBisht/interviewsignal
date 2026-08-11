import React from 'react';
import { useAuth } from '../context/AuthContext';
import apiClient from '../api/client';

export const Login: React.FC = () => {
  const { login } = useAuth();

  const handleGitHubAuth = async () => {
    try {
      const response = await apiClient.get('/auth/login');
      if (response.data.auth_url) {
        window.location.href = response.data.auth_url;
      }
    } catch (e) {
      console.warn('Simulating local dev authentication');
      // For local development simulation
      login('demo-token-12345', {
        username: 'PratyakshBisht',
        name: 'Pratyaksh Bisht',
        email: 'pratyakshbisht05@gmail.com',
      });
      window.location.href = '/dashboard';
    }
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center p-4">
      <div className="max-w-md w-full p-8 rounded-3xl border border-slate-800 bg-slate-900/60 backdrop-blur-xl text-center relative overflow-hidden">
        {/* Glow effect */}
        <div className="absolute -top-24 left-1/2 -translate-x-1/2 w-48 h-48 bg-teal-500/20 blur-3xl rounded-full pointer-events-none" />

        <div className="inline-flex items-center justify-center h-16 w-16 rounded-2xl bg-gradient-to-tr from-teal-500 to-emerald-400 text-3xl font-black text-slate-950 mb-6 shadow-xl shadow-teal-500/20">
          ⚡
        </div>

        <h1 className="text-3xl font-extrabold text-white tracking-tight mb-2">
          InterviewSignal
        </h1>
        <p className="text-sm text-slate-400 mb-8">
          The developer reputation graph and automated AI talent evaluation for engineers.
        </p>

        <button
          onClick={handleGitHubAuth}
          className="w-full flex items-center justify-center gap-3 py-3.5 px-4 rounded-xl bg-teal-500 hover:bg-teal-400 text-slate-950 font-bold transition-all transform active:scale-[0.98] shadow-lg shadow-teal-500/25"
        >
          <svg className="w-5 h-5 fill-current" viewBox="0 0 24 24">
            <path fillRule="evenodd" clipRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" />
          </svg>
          Continue with GitHub
        </button>

        <p className="text-xs text-slate-500 mt-6">
          By signing in, you grant read-only access to your public profile and repositories.
        </p>
      </div>
    </div>
  );
};
