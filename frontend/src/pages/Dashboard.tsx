import { FC, useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import DashboardSidebar from '../components/DashboardSidebar';
import ScoreCard from '../components/ScoreCard';
import RadarChart from '../components/RadarChart';
import ActionButton from '../components/ActionButton';
import { 
  Code, 
  GitBranch, 
  TrendingUp, 
  ShieldCheck, 
  Download, 
  RefreshCw,
  Star
} from 'lucide-react';
import { analysisAPI, profileAPI } from '../lib/api';

const Dashboard: FC = () => {
  const { user, logout } = useAuth();
  const [analysis, setAnalysis] = useState<any>(null);
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [runningAnalysis, setRunningAnalysis] = useState(false);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    setLoading(true);
    try {
      const [latestRes, statsRes] = await Promise.all([
        analysisAPI.getLatestAnalysis().catch(() => ({ data: null })),
        profileAPI.getUserStats().catch(() => ({ data: null }))
      ]);
      setAnalysis(latestRes.data);
      setStats(statsRes.data);
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const runAnalysis = async () => {
    setRunningAnalysis(true);
    try {
      await analysisAPI.triggerAnalysis(true);
      await fetchDashboardData();
    } catch (error) {
      console.error('Analysis failed:', error);
    } finally {
      setRunningAnalysis(false);
    }
  };

  const radarData = analysis ? [
    { category: 'Code Quality', score: analysis.code_quality_score, fullMark: 100 },
    { category: 'Consistency', score: analysis.consistency_score, fullMark: 100 },
    { category: 'Depth', score: analysis.depth_score, fullMark: 100 },
    { category: 'Production', score: analysis.production_readiness_score, fullMark: 100 },
    { category: 'Collaboration', score: 75, fullMark: 100 }
  ] : [];

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-brand-500"></div>
        <p className="ml-4 text-lg text-slate-600">Loading your dashboard...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <DashboardSidebar username={user?.username || ''} avatarUrl={user?.avatar_url} />
      
      <main className="lg:ml-64">
        {/* Top Navigation */}
        <div className="bg-white border-b border-slate-200 px-8 py-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold text-slate-800">Welcome back, {user?.username}!</h1>
              <p className="text-slate-500">Your last analysis was {analysis ? new Date(analysis.created_at).toLocaleDateString() : 'never'}</p>
            </div>
            <div className="flex items-center gap-4">
              <ActionButton 
                variant="secondary" 
                size="md"
                icon={Download}
              >
                Export Report
              </ActionButton>
              <button
                onClick={logout}
                className="px-4 py-2 text-slate-600 hover:text-red-600 transition"
              >
                Sign Out
              </button>
            </div>
          </div>
        </div>

        {/* Action Card */}
        <div className="p-8">
          <div className="bg-gradient-to-r from-brand-600 to-blue-600 rounded-2xl p-8 text-white mb-8">
            <div className="flex flex-col md:flex-row items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold mb-2">Your Current Reputation Score</h2>
                <p className="text-brand-100 mb-4">
                  Based on your GitHub activity, commit history, and code quality metrics.
                </p>
                <div className="flex items-center gap-4">
                  <div className="flex items-baseline">
                    <span className="text-6xl font-black mr-2">{analysis?.overall_score ?? '--'}</span>
                    <span className="text-brand-200">/ 100</span>
                  </div>
                  <div className="text-sm">
                    <p className="flex items-center gap-1">
                      <TrendingUp size={16} /> Trending upward
                    </p>
                    <p className="text-brand-200">+12.5% from last month</p>
                  </div>
                </div>
              </div>
              <div className="mt-4 md:mt-0">
                <ActionButton
                  variant="primary"
                  size="lg"
                  icon={RefreshCw}
                  loading={runningAnalysis}
                  onClick={runAnalysis}
                  className="bg-white text-brand-600 hover:bg-brand-50"
                >
                  {runningAnalysis ? 'Analyzing...' : 'Refresh Analysis'}
                </ActionButton>
                <p className="text-brand-200 text-sm text-center mt-2">Updates in real-time</p>
              </div>
            </div>
          </div>

          {/* Score Cards Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <ScoreCard
              category="Code Quality"
              score={analysis?.code_quality_score || 0}
              description="Code structure, testing, documentation"
              icon={Code}
              trend="up"
            />
            <ScoreCard
              category="Consistency"
              score={analysis?.consistency_score || 0}
              description="Regular contributions and maintenance"
              icon={GitBranch}
              trend="stable"
            />
            <ScoreCard
              category="Technical Depth"
              score={analysis?.depth_score || 0}
              description="Complexity and architecture patterns"
              icon={ShieldCheck}
              trend="up"
            />
            <ScoreCard
              category="Production Ready"
              score={analysis?.production_readiness_score || 0}
              description="Deployment, monitoring, CI/CD"
              icon={TrendingUp}
              trend="up"
            />
          </div>

          {/* Charts & Insights */}
          <div className="grid lg:grid-cols-3 gap-8 mb-8">
            {/* Radar Chart */}
            <div className="lg:col-span-2">
              <RadarChart data={radarData} />
            </div>
            
            {/* AI Summary */}
            <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-6">
              <h3 className="font-bold text-slate-800 text-lg mb-4 flex items-center gap-2">
                <Star className="text-amber-500" size={20} /> AI Recruiter Summary
              </h3>
              <div className="space-y-4">
                {analysis?.recruiter_summary ? (
                  <p className="text-slate-600 text-sm leading-relaxed border-l-4 border-brand-500 pl-4 py-2">
                    "{analysis.recruiter_summary}"
                  </p>
                ) : (
                  <p className="text-slate-500 italic">No analysis summary available yet.</p>
                )}
                
                <div className="pt-4 border-t border-slate-100">
                  <h4 className="font-semibold text-slate-700 mb-2">Key Strengths</h4>
                  <ul className="space-y-2">
                    {analysis?.strengths?.slice(0, 3).map((strength: string, idx: number) => (
                      <li key={idx} className="flex items-center gap-2 text-sm text-slate-600">
                        <div className="w-1.5 h-1.5 rounded-full bg-green-500"></div>
                        {strength}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </div>

          {/* Stats Overview */}
          {stats && (
            <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-6">
              <h3 className="font-bold text-slate-800 text-lg mb-6">Activity Overview</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                <div>
                  <p className="text-slate-500 text-sm">Total Analyses</p>
                  <p className="text-2xl font-bold text-slate-800">{stats.total_analyses || 0}</p>
                </div>
                <div>
                  <p className="text-slate-500 text-sm">Avg. Score</p>
                  <p className="text-2xl font-bold text-slate-800">{stats.average_overall_score ?? '--'}</p>
                </div>
                <div>
                  <p className="text-slate-500 text-sm">Latest Score</p>
                  <p className="text-2xl font-bold text-slate-800">{stats.latest_overall_score ?? '--'}</p>
                </div>
                <div>
                  <p className="text-slate-500 text-sm">Trend</p>
                  <p className="text-2xl font-bold text-slate-800 capitalize">{stats.score_trend || 'stable'}</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
