import React from 'react';

interface ScoreCardProps {
  title: string;
  score: number;
  maxScore?: number;
  subtitle?: string;
  color?: 'teal' | 'indigo' | 'emerald' | 'amber';
}

export const ScoreCard: React.FC<ScoreCardProps> = ({
  title,
  score,
  maxScore = 100,
  subtitle,
  color = 'teal',
}) => {
  const percentage = Math.round((score / maxScore) * 100);

  const colorStyles = {
    teal: 'from-teal-500/20 to-teal-500/5 border-teal-500/30 text-teal-400',
    indigo: 'from-indigo-500/20 to-indigo-500/5 border-indigo-500/30 text-indigo-400',
    emerald: 'from-emerald-500/20 to-emerald-500/5 border-emerald-500/30 text-emerald-400',
    amber: 'from-amber-500/20 to-amber-500/5 border-amber-500/30 text-amber-400',
  }[color];

  const progressBg = {
    teal: 'bg-teal-500',
    indigo: 'bg-indigo-500',
    emerald: 'bg-emerald-500',
    amber: 'bg-amber-500',
  }[color];

  return (
    <div className={`p-6 rounded-2xl border bg-gradient-to-b ${colorStyles} backdrop-blur-sm relative overflow-hidden group transition-all duration-300 hover:border-slate-700`}>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-medium text-slate-400 uppercase tracking-wider">{title}</h3>
        <span className="text-2xl font-extrabold text-white">{score}</span>
      </div>

      {/* Progress Bar */}
      <div className="w-full bg-slate-800/80 rounded-full h-2.5 overflow-hidden mb-3">
        <div
          className={`h-full ${progressBg} transition-all duration-1000 ease-out`}
          style={{ width: `${percentage}%` }}
        />
      </div>

      {subtitle && <p className="text-xs text-slate-400">{subtitle}</p>}
    </div>
  );
};
