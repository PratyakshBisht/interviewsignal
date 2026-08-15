import { FC } from 'react';
import {
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Area,
  AreaChart,
  Legend,
} from 'recharts';
import { GitCommit, TrendingUp, Calendar } from 'lucide-react';
import { CommitDataPoint } from '../data/sampleData';

interface CommitsTimelineProps {
  data: CommitDataPoint[];
  title?: string;
}

const CommitsTimeline: FC<CommitsTimelineProps> = ({
  data,
  title = 'Commit Activity Timeline',
}) => {
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 rounded-lg shadow-lg border border-slate-200">
          <p className="font-bold text-slate-800">{label}</p>
          <div className="space-y-1 mt-1">
            <p className="flex items-center gap-2 text-xs">
              <GitCommit size={14} className="text-blue-500" />
              <span className="text-slate-600">Commits:</span>
              <span className="font-bold">{payload[0]?.value}</span>
            </p>
            <p className="flex items-center gap-2 text-xs">
              <TrendingUp size={14} className="text-green-500" />
              <span className="text-slate-600">Lines Added:</span>
              <span className="font-bold text-green-600">
                {payload[0]?.payload?.lines_added}
              </span>
            </p>
            <p className="flex items-center gap-2 text-xs">
              <TrendingUp size={14} className="text-red-500 transform rotate-180" />
              <span className="text-slate-600">Lines Deleted:</span>
              <span className="font-bold text-red-600">
                {payload[0]?.payload?.lines_deleted}
              </span>
            </p>
          </div>
        </div>
      );
    }
    return null;
  };

  const totalCommits = data.reduce((sum, day) => sum + day.commits, 0);
  const avgPerWeek = data.length ? (totalCommits / data.length).toFixed(1) : '0';
  const totalLines = data.reduce((sum, day) => sum + day.lines_added, 0);
  const mostActive = data.length ? Math.max(...data.map((d) => d.commits)) : 0;

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <div>
          <h3 className="font-bold text-slate-800 text-lg flex items-center gap-2">
            <Calendar className="text-brand-500" size={20} /> {title}
          </h3>
          <p className="text-slate-500 text-sm">Weekly commit activity overview</p>
        </div>
        <div className="text-sm text-slate-600">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-blue-500"></div>
              <span>Commits</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-green-500"></div>
              <span>Lines Added</span>
            </div>
          </div>
        </div>
      </div>

      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
            <XAxis
              dataKey="date"
              tick={{ fill: '#64748b', fontSize: 11 }}
              axisLine={{ stroke: '#e2e8f0' }}
            />
            <YAxis
              tick={{ fill: '#64748b', fontSize: 11 }}
              axisLine={{ stroke: '#e2e8f0' }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend />
            <Area
              type="monotone"
              dataKey="commits"
              name="Commits"
              stroke="#3b82f6"
              fill="#3b82f6"
              fillOpacity={0.2}
              strokeWidth={2}
            />
            <Area
              type="monotone"
              dataKey="lines_added"
              name="Lines Added"
              stroke="#10b981"
              fill="#10b981"
              fillOpacity={0.2}
              strokeWidth={2}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {/* Stats summary */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6 pt-6 border-t border-slate-100">
        <div className="text-center">
          <p className="text-slate-500 text-sm">Total Commits</p>
          <p className="text-2xl font-bold text-slate-800">{totalCommits}</p>
        </div>
        <div className="text-center">
          <p className="text-slate-500 text-sm">Avg per Week</p>
          <p className="text-2xl font-bold text-slate-800">{avgPerWeek}</p>
        </div>
        <div className="text-center">
          <p className="text-slate-500 text-sm">Lines Added</p>
          <p className="text-2xl font-bold text-slate-800">{totalLines.toLocaleString()}</p>
        </div>
        <div className="text-center">
          <p className="text-slate-500 text-sm">Most Active Day</p>
          <p className="text-2xl font-bold text-slate-800">{mostActive}</p>
        </div>
      </div>
    </div>
  );
};

export default CommitsTimeline;
