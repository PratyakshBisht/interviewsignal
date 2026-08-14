import { FC } from 'react';
import {
  Radar,
  RadarChart as RechartsRadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Legend
} from 'recharts';

interface RadarChartProps {
  data: {
    category: string;
    score: number;
    fullMark: number;
  }[];
}

const RadarChart: FC<RadarChartProps> = ({ data }) => {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-6">
      <h3 className="font-bold text-slate-800 text-lg mb-6">Skill Distribution</h3>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <RechartsRadarChart cx="50%" cy="50%" outerRadius="80%" data={data}>
            <PolarGrid stroke="#e2e8f0" />
            <PolarAngleAxis 
              dataKey="category" 
              tick={{ fill: '#64748b', fontSize: 12 }}
              axisLine={{ stroke: '#e2e8f0' }}
            />
            <PolarRadiusAxis 
              angle={30} 
              domain={[0, 100]} 
              tick={{ fill: '#64748b', fontSize: 10 }}
            />
            <Radar
              name="Your Score"
              dataKey="score"
              stroke="#0ea5e9"
              fill="#0ea5e9"
              fillOpacity={0.3}
              strokeWidth={2}
            />
            <Legend />
          </RechartsRadarChart>
        </ResponsiveContainer>
      </div>
      <div className="mt-4 grid grid-cols-2 gap-2">
        {data.slice(0, 4).map((item) => (
          <div key={item.category} className="flex items-center justify-between text-sm">
            <span className="text-slate-600">{item.category}</span>
            <span className="font-bold text-slate-800">{item.score}%</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RadarChart;
