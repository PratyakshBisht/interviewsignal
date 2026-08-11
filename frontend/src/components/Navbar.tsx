import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export const Navbar: React.FC = () => {
  const { user, logout, isAuthenticated } = useAuth();

  return (
    <nav className="border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2.5">
          <div className="h-9 w-9 rounded-xl bg-gradient-to-tr from-teal-500 to-emerald-400 flex items-center justify-center font-black text-slate-950 text-xl shadow-lg shadow-teal-500/20">
            ⚡
          </div>
          <span className="text-xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white via-slate-200 to-teal-200">
            InterviewSignal
          </span>
        </Link>

        <div className="flex items-center gap-4">
          {isAuthenticated ? (
            <>
              <Link
                to="/dashboard"
                className="text-sm font-medium text-slate-300 hover:text-white transition-colors"
              >
                Dashboard
              </Link>
              <Link
                to="/profile"
                className="text-sm font-medium text-slate-300 hover:text-white transition-colors"
              >
                Profile
              </Link>
              <div className="flex items-center gap-3 pl-2 border-l border-slate-800">
                <span className="text-sm text-slate-400 font-mono">@{user?.username}</span>
                <button
                  onClick={logout}
                  className="text-xs px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors"
                >
                  Sign Out
                </button>
              </div>
            </>
          ) : (
            <Link
              to="/login"
              className="text-sm font-medium px-4 py-2 rounded-xl bg-teal-500 hover:bg-teal-400 text-slate-950 font-semibold transition-all shadow-md shadow-teal-500/10"
            >
              Sign In with GitHub
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
};
