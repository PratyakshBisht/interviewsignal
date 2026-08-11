import React from 'react';

interface RepoProps {
  name: string;
  description?: string;
  stars: number;
  forks: number;
  language?: string;
  qualityScore: number;
  url?: string;
}

export const RepoCard: React.FC<RepoProps> = ({
  name,
  description,
  stars,
  forks,
  language,
  qualityScore,
  url,
}) => {
  return (
    <div className="p-5 rounded-xl border border-slate-800/80 bg-slate-900/40 hover:bg-slate-900/80 transition-all duration-200">
      <div className="flex items-start justify-between gap-4 mb-2">
        <a
          href={url || '#'}
          target="_blank"
          rel="noopener noreferrer"
          className="text-base font-semibold text-teal-300 hover:text-teal-200 hover:underline font-mono"
        >
          {name}
        </a>
        <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-teal-500/10 border border-teal-500/20 text-teal-400 text-xs font-semibold">
          <span>Quality:</span>
          <span>{qualityScore}/100</span>
        </div>
      </div>

      <p className="text-sm text-slate-400 mb-4 line-clamp-2">
        {description || 'No description provided.'}
      </p>

      <div className="flex items-center gap-4 text-xs text-slate-500 font-mono">
        {language && (
          <span className="flex items-center gap-1.5 text-slate-300">
            <span className="h-2 w-2 rounded-full bg-teal-400" />
            {language}
          </span>
        )}
        <span>⭐ {stars}</span>
        <span>🍴 {forks}</span>
      </div>
    </div>
  );
};
