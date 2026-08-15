import { FC } from 'react';
import { TrendingUp, Target, CheckCircle, Award } from 'lucide-react';

interface Skill {
  skill: string;
  level: number;
  target: number;
}

interface SkillProgressProps {
  skills: Skill[];
  title?: string;
}

const SkillProgress: FC<SkillProgressProps> = ({
  skills,
  title = 'Skill Development Progress',
}) => {
  const getProgressColor = (progress: number) => {
    if (progress >= 90) return 'text-green-600 bg-green-50';
    if (progress >= 70) return 'text-blue-600 bg-blue-50';
    if (progress >= 50) return 'text-amber-600 bg-amber-50';
    return 'text-red-600 bg-red-50';
  };

  const getStatusIcon = (current: number, target: number) => {
    const progress = (current / target) * 100;
    if (progress >= 100) return <CheckCircle size={16} className="text-green-500" />;
    if (progress >= 80) return <TrendingUp size={16} className="text-blue-500" />;
    return <Target size={16} className="text-amber-500" />;
  };

  const avgCompletion = skills.length
    ? (
        skills.reduce((sum, s) => sum + (s.level / s.target) * 100, 0) / skills.length
      ).toFixed(0)
    : '0';

  const skillsMastered = skills.filter((s) => s.level >= s.target).length;
  const mostAdvanced = skills.length
    ? skills.reduce((max, s) => (s.level / s.target > max.level / max.target ? s : max), skills[0]).skill
    : 'N/A';

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <div>
          <h3 className="font-bold text-slate-800 text-lg flex items-center gap-2">
            <Award className="text-brand-500" size={20} /> {title}
          </h3>
          <p className="text-slate-500 text-sm">Track your technical skills development</p>
        </div>
        <div className="text-sm text-slate-600">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <div className="w-2.5 h-2.5 rounded-full bg-green-500"></div>
              <span>Mastered</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2.5 h-2.5 rounded-full bg-blue-500"></div>
              <span>In Progress</span>
            </div>
          </div>
        </div>
      </div>

      <div className="space-y-5">
        {skills.map((skill) => {
          const progressPercent = (skill.level / skill.target) * 100;
          const isComplete = skill.level >= skill.target;

          return (
            <div key={skill.skill} className="relative">
              <div className="flex items-center justify-between mb-1">
                <div className="flex items-center gap-2">
                  {getStatusIcon(skill.level, skill.target)}
                  <span className="font-medium text-slate-800 text-sm">{skill.skill}</span>
                </div>
                <div className="flex items-center gap-2">
                  <span
                    className={`font-bold text-xs ${getProgressColor(progressPercent)} px-2 py-0.5 rounded`}
                  >
                    {skill.level}/{skill.target}
                  </span>
                  <span className="text-slate-500 text-xs">
                    ({progressPercent.toFixed(0)}%)
                  </span>
                </div>
              </div>
              <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-500 ${
                    progressPercent >= 90
                      ? 'bg-green-500'
                      : progressPercent >= 70
                      ? 'bg-blue-500'
                      : progressPercent >= 50
                      ? 'bg-amber-500'
                      : 'bg-red-500'
                  }`}
                  style={{ width: `${Math.min(100, progressPercent)}%` }}
                />
              </div>
              {!isComplete && (
                <div className="text-[11px] text-slate-400 mt-1">
                  Need {skill.target - skill.level} more points to reach target
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-3 gap-4 mt-8 pt-6 border-t border-slate-100">
        <div className="text-center">
          <p className="text-slate-500 text-xs">Avg. Completion</p>
          <p className="text-2xl font-bold text-slate-800">{avgCompletion}%</p>
        </div>
        <div className="text-center">
          <p className="text-slate-500 text-xs">Skills Mastered</p>
          <p className="text-2xl font-bold text-slate-800">{skillsMastered}</p>
        </div>
        <div className="text-center">
          <p className="text-slate-500 text-xs">Most Advanced</p>
          <p className="text-lg font-bold text-slate-800 truncate" title={mostAdvanced}>
            {mostAdvanced}
          </p>
        </div>
      </div>
    </div>
  );
};

export default SkillProgress;
