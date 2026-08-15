import { FC } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import { Code, Palette, Layers } from 'lucide-react';

interface LanguageData {
  language: string;
  percentage: number;
  color: string;
}

interface LanguageDistributionProps {
  languages: LanguageData[];
}

const LanguageDistribution: FC<LanguageDistributionProps> = ({ languages }) => {
  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 rounded-lg shadow-lg border border-slate-200 text-xs">
          <p className="font-bold text-slate-800">{payload[0].name}</p>
          <p className="text-slate-600 mt-0.5">{payload[0].value}% of codebase</p>
        </div>
      );
    }
    return null;
  };

  const COLORS = [
    '#3b82f6', // Blue
    '#10b981', // Green
    '#8b5cf6', // Purple
    '#f59e0b', // Amber
    '#ef4444', // Red
    '#ec4899', // Pink
    '#14b8a6', // Teal
    '#f97316', // Orange
  ];

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <div>
          <h3 className="font-bold text-slate-800 text-lg flex items-center gap-2">
            <Code className="text-brand-500" size={20} /> Language Distribution
          </h3>
          <p className="text-slate-500 text-sm">
            Primary programming languages in your repositories
          </p>
        </div>
        <div className="flex items-center gap-2 text-slate-400">
          <Palette size={16} />
          <Layers size={16} />
        </div>
      </div>

      <div className="grid lg:grid-cols-2 gap-8 items-center">
        {/* Pie Chart */}
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={languages}
                cx="50%"
                cy="50%"
                labelLine={false}
                outerRadius={80}
                fill="#8884d8"
                dataKey="percentage"
                nameKey="language"
              >
                {languages.map((entry, index) => (
                  <Cell
                    key={`cell-lang-${index}`}
                    fill={entry.color || COLORS[index % COLORS.length]}
                  />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Language Details */}
        <div className="space-y-3">
          <h4 className="font-semibold text-slate-700 text-sm mb-2">Language Details</h4>
          {languages.map((lang, index) => (
            <div key={lang.language} className="flex items-center justify-between text-xs">
              <div className="flex items-center gap-2">
                <div
                  className="w-2.5 h-2.5 rounded-sm"
                  style={{
                    backgroundColor: lang.color || COLORS[index % COLORS.length],
                  }}
                />
                <span className="text-slate-700 font-medium">{lang.language}</span>
              </div>
              <div className="flex items-center gap-3">
                <span className="font-bold text-slate-800">{lang.percentage}%</span>
                <div className="w-20 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                  <div
                    className="h-full rounded-full"
                    style={{
                      width: `${lang.percentage}%`,
                      backgroundColor: lang.color || COLORS[index % COLORS.length],
                    }}
                  />
                </div>
              </div>
            </div>
          ))}

          {/* Stats Summary */}
          <div className="mt-6 pt-4 border-t border-slate-100 grid grid-cols-3 gap-2">
            <div className="text-center">
              <p className="text-slate-500 text-[11px]">Primary</p>
              <p className="font-bold text-slate-800 text-xs truncate">
                {languages[0]?.language || 'N/A'}
              </p>
            </div>
            <div className="text-center">
              <p className="text-slate-500 text-[11px]">Diversity</p>
              <p className="font-bold text-slate-800 text-xs">
                {languages.length > 3 ? 'High' : languages.length > 1 ? 'Medium' : 'Low'}
              </p>
            </div>
            <div className="text-center">
              <p className="text-slate-500 text-[11px]">Top 3 Total</p>
              <p className="font-bold text-slate-800 text-xs">
                {languages.slice(0, 3).reduce((sum, lang) => sum + lang.percentage, 0)}%
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LanguageDistribution;
