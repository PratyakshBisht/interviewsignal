import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { ScoreCard } from '../components/ScoreCard';
import { RepoCard } from '../components/RepoCard';
import { SummaryPanel } from '../components/SummaryPanel';
import apiClient from '../api/client';

export const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState({
    overall_score: 87.5,
    quality_score: 92.0,
    depth_score: 84.0,
    consistency_score: 86.5,
    summary: 'Candidate exhibits robust software engineering discipline, high commit frequency, well-scoped microservices architectures, and clean modular code standards.',
    strengths: [
      'Comprehensive RESTful API modeling with FastAPI & PostgreSQL',
      'Solid component-driven UI architecture in React & TypeScript',
      'High attention to continuous integration, unit tests, and containerization'
    ],
    areas_for_growth: [
      'Increase automated integration test coverage',
      'Publish and maintain open-source package releases'
    ],
    repos: [
      {
        name: 'interviewsignal',
        description: 'Developer reputation graph and talent scoring platform for students and engineers.',
        stars: 12,
        forks: 3,
        language: 'TypeScript',
        qualityScore: 94,
      },
      {
        name: 'health-tracker-system',
        description: 'Full-stack health analytics and telemetry metrics platform.',
        stars: 8,
        forks: 2,
        language: 'Python',
        qualityScore: 89,
      },
      {
        name: 'Find-your-Stay',
        description: 'Modern accommodation discovery and reservation portal.',
        stars: 5,
        forks: 1,
        language: 'JavaScript',
        qualityScore: 82,
      },
    ]
  });

  const username = user?.username || 'PratyakshBisht';

  useEffect(() => {
    const fetchAnalysis = async () => {
      try {
        setLoading(true);
        const res = await apiClient.get(`/analysis/${username}`);
        if (res.data && res.data.scores) {
          setData((prev) => ({
            ...prev,
            ...res.data.scores,
            summary: res.data.summary || prev.summary,
          }));
        }
      } catch (err) {
        console.log('Using default presentation telemetry');
      } finally {
        setLoading(false);
      }
    };
    fetchAnalysis();
  }, [username]);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-8 rounded-3xl bg-gradient-to-r from-slate-900 via-slate-900/90 to-teal-950/40 border border-slate-800">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white">
              Reputation Graph
            </h1>
            <span className="px-3 py-1 rounded-full text-xs font-bold bg-teal-500/20 text-teal-400 border border-teal-500/30">
              Verified Candidate
            </span>
          </div>
          <p className="text-slate-400 text-sm">
            Analysis generated for <span className="text-teal-300 font-mono">@{username}</span>
          </p>
        </div>

        <button
          onClick={() => alert('Refreshing analysis graph...')}
          className="self-start md:self-auto px-5 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-sm font-semibold transition-all border border-slate-700"
        >
          ↻ Re-calculate Graph
        </button>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <ScoreCard
          title="Overall Signal"
          score={data.overall_score}
          subtitle="Top 8% among peers"
          color="teal"
        />
        <ScoreCard
          title="Code Quality"
          score={data.quality_score}
          subtitle="Clean architecture & tests"
          color="emerald"
        />
        <ScoreCard
          title="Project Depth"
          score={data.depth_score}
          subtitle="Complexity & system scope"
          color="indigo"
        />
        <ScoreCard
          title="Consistency"
          score={data.consistency_score}
          subtitle="Commit habits & cadence"
          color="amber"
        />
      </div>

      {/* Recruiter Summary */}
      <SummaryPanel
        summary={data.summary}
        strengths={data.strengths}
        areasForGrowth={data.areas_for_growth}
      />

      {/* Repositories Breakdown */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold text-white">Repository Evaluation</h2>
          <span className="text-xs text-slate-400 font-mono">3 Active Projects Evaluated</span>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {data.repos.map((repo, idx) => (
            <RepoCard key={idx} {...repo} />
          ))}
        </div>
      </div>
    </div>
  );
};
