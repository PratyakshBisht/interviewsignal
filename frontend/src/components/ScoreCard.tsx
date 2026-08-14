import { FC } from 'react';
import { 
  ShieldCheck, 
  TrendingUp, 
  CheckCircle, 
  AlertCircle 
} from 'lucide-react';

interface ScoreCardProps {
  category: string;
  score: number;
  maxScore?: number;
  description: string;
  icon?: React.ElementType;
  trend?: 'up' | 'down' | 'stable';
}

const ScoreCard: FC<ScoreCardProps> = ({ 
  category, 
  score, 
  maxScore = 100,
  description,
  icon: Icon = ShieldCheck,
  trend 
}) => {
  const getColorClass = (score: number) => {
    if (score >= 80) return 'text-green-600 bg-green-50 border-green-200';
    if (score >= 60) return 'text-blue-600 bg-blue-50 border-blue-200';
    return 'text-amber-600 bg-amber-50 border-amber-200';
  };

  const getTrendIcon = () => {
    switch (trend) {
      case 'up': return <TrendingUp className="text-green-500" size={16} />;
      case 'down': return <TrendingUp className="text-red-500 transform rotate-180" size={16} />;
      default: return null;
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-6 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className={`p-2 rounded-lg ${getColorClass(score)}`}>
            <Icon size={20} />
          </div>
          <div>
            <h3 className="font-bold text-slate-800 text-lg">{category}</h3>
            <div className="flex items-center gap-2 mt-1">
              <span className="text-2xl font-black text-slate-900">{score.toFixed(1)}</span>
              <span className="text-slate-500 text-sm">/ {maxScore}</span>
              {trend && getTrendIcon()}
            </div>
          </div>
        </div>
        {score >= 70 ? (
          <CheckCircle className="text-green-500" size={20} />
        ) : (
          <AlertCircle className="text-amber-500" size={20} />
        )}
      </div>
      
      <p className="text-slate-600 text-sm">{description}</p>
      
      {/* Progress bar */}
      <div className="mt-4">
        <div className="flex justify-between text-xs text-slate-500 mb-1">
          <span>0</span>
          <span>{maxScore}</span>
        </div>
        <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
          <div 
            className={`h-full rounded-full ${score >= 80 ? 'bg-green-500' : score >= 60 ? 'bg-blue-500' : 'bg-amber-500'}`}
            style={{ width: `${(score / maxScore) * 100}%` }}
          />
        </div>
      </div>
    </div>
  );
};

export default ScoreCard;
