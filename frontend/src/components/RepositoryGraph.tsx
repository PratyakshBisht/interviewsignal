import { FC } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
  LabelList,
} from 'recharts';
import { GitFork, Star, GitPullRequest, GitCommit, FolderGit2 } from 'lucide-react';
import { RepositoryStats } from '../data/sampleData';

interface RepositoryGraphProps {
  repositories: RepositoryStats[];
}

const RepositoryGraph: FC<RepositoryGraphProps> = ({ repositories }) => {
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const repo = repositories.find((r) => r.name === label);
      return (
        <div className="bg-white p-3 rounded-lg shadow-lg border border-slate-200 min-w-48">
          <p className="font-bold text-slate-800 mb-2">{label}</p>
          <div className="space-y-1 text-xs">
            <div className="flex items-center justify-between">
              <span className="flex items-center gap-1 text-slate-600">
                <Star size={14} className="text-amber-500" /> Stars
              </span>
              <span className="font-bold">{repo?.stars || 0}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="flex items-center gap-1 text-slate-600">
                <GitFork size={14} className="text-emerald-500" /> Forks
              </span>
              <span className="font-bold">{repo?.forks || 0}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="flex items-center gap-1 text-slate-600">
                <GitCommit size={14} className="text-blue-500" /> Commits
              </span>
              <span className="font-bold">{repo?.commits || 0}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="flex items-center gap-1 text-slate-600">
                <GitPullRequest size={14} className="text-purple-500" /> PRs
              </span>
              <span className="font-bold">{repo?.prs || 0}</span>
            </div>
          </div>
        </div>
      );
    }
    return null;
  };

  const chartData = repositories.map((repo) => ({
    name: repo.name,
    Stars: repo.stars,
    Forks: repo.forks,
    Commits: repo.commits,
    PRs: repo.prs,
  }));

  const colors = ['#3b82f6', '#10b981', '#8b5cf6', '#f59e0b', '#ef4444'];
  const totalStars = repositories.reduce((sum, repo) => sum + repo.stars, 0);
  const totalCommits = repositories.reduce((sum, repo) => sum + repo.commits, 0);
  const mostPopular = repositories.length
    ? repositories.reduce((max, repo) => (repo.stars > max.stars ? repo : max), repositories[0])?.name
    : 'N/A';

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <div>
          <h3 className="font-bold text-slate-800 text-lg flex items-center gap-2">
            <FolderGit2 className="text-brand-500" size={20} /> Repository Analytics
          </h3>
          <p className="text-slate-500 text-sm">Compare performance across your repositories</p>
        </div>
        <div className="flex items-center gap-4">
          <div className="text-xs text-slate-600 flex items-center gap-3">
            {['Stars', 'Forks', 'Commits'].map((label, idx) => (
              <span key={label} className="flex items-center gap-1">
                <div
                  className="w-3 h-3 rounded-sm"
                  style={{ backgroundColor: colors[idx] }}
                ></div>
                {label}
              </span>
            ))}
          </div>
        </div>
      </div>

      <div className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
            <XAxis
              dataKey="name"
              tick={{ fill: '#64748b', fontSize: 11 }}
              axisLine={{ stroke: '#e2e8f0' }}
            />
            <YAxis
              tick={{ fill: '#64748b', fontSize: 11 }}
              axisLine={{ stroke: '#e2e8f0' }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Bar name="Stars" dataKey="Stars" radius={[4, 4, 0, 0]}>
              {chartData.map((_entry, index) => (
                <Cell key={`cell-star-${index}`} fill={colors[0]} opacity={0.85} />
              ))}
              <LabelList dataKey="Stars" position="top" fill="#3b82f6" fontSize={11} />
            </Bar>
            <Bar name="Forks" dataKey="Forks" radius={[4, 4, 0, 0]}>
              {chartData.map((_entry, index) => (
                <Cell key={`cell-fork-${index}`} fill={colors[1]} opacity={0.85} />
              ))}
            </Bar>
            <Bar name="Commits" dataKey="Commits" radius={[4, 4, 0, 0]}>
              {chartData.map((_entry, index) => (
                <Cell key={`cell-commit-${index}`} fill={colors[2]} opacity={0.85} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Repository Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6 pt-6 border-t border-slate-100">
        <div className="text-center">
          <p className="text-slate-500 text-sm">Total Repositories</p>
          <p className="text-2xl font-bold text-slate-800">{repositories.length}</p>
        </div>
        <div className="text-center">
          <p className="text-slate-500 text-sm">Total Stars</p>
          <p className="text-2xl font-bold text-slate-800">{totalStars}</p>
        </div>
        <div className="text-center">
          <p className="text-slate-500 text-sm">Most Popular</p>
          <p className="text-lg font-bold text-slate-800 truncate" title={mostPopular}>
            {mostPopular}
          </p>
        </div>
        <div className="text-center">
          <p className="text-slate-500 text-sm">Total Commits</p>
          <p className="text-2xl font-bold text-slate-800">{totalCommits.toLocaleString()}</p>
        </div>
      </div>
    </div>
  );
};

export default RepositoryGraph;
