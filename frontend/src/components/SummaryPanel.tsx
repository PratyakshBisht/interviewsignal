import React from 'react';

interface SummaryPanelProps {
  summary: string;
  strengths?: string[];
  areasForGrowth?: string[];
}

export const SummaryPanel: React.FC<SummaryPanelProps> = ({
  summary,
  strengths = [],
  areasForGrowth = [],
}) => {
  return (
    <div className="p-6 rounded-2xl border border-slate-800 bg-slate-900/60 backdrop-blur-md">
      <div className="flex items-center gap-2 mb-4">
        <span className="text-xl">🤖</span>
        <h3 className="text-lg font-bold text-white">AI Recruiter Summary</h3>
      </div>

      <p className="text-slate-300 leading-relaxed text-sm mb-6 bg-slate-950/60 p-4 rounded-xl border border-slate-800/80">
        "{summary}"
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h4 className="text-xs font-semibold text-emerald-400 uppercase tracking-wider mb-3 flex items-center gap-2">
            <span>✓</span> Key Strengths
          </h4>
          <ul className="space-y-2">
            {strengths.map((item, idx) => (
              <li key={idx} className="text-sm text-slate-300 flex items-start gap-2">
                <span className="text-emerald-400 mt-0.5">•</span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </div>

        <div>
          <h4 className="text-xs font-semibold text-amber-400 uppercase tracking-wider mb-3 flex items-center gap-2">
            <span>↗</span> Areas for Growth
          </h4>
          <ul className="space-y-2">
            {areasForGrowth.map((item, idx) => (
              <li key={idx} className="text-sm text-slate-300 flex items-start gap-2">
                <span className="text-amber-400 mt-0.5">•</span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};
