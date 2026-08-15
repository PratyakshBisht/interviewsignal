import { FC, useState, useEffect, useCallback } from 'react';
import { useAuth } from '../context/AuthContext';
import DashboardSidebar from '../components/DashboardSidebar';
import ScoreCard from '../components/ScoreCard';
import RadarChart from '../components/RadarChart';
import ActionButton from '../components/ActionButton';
import CommitsTimeline from '../components/CommitsTimeline';
import RepositoryGraph from '../components/RepositoryGraph';
import PDFExporter from '../components/PDFExporter';
import SkillProgress from '../components/SkillProgress';
import LanguageDistribution from '../components/LanguageDistribution';
import { useGitHubData } from '../hooks/useGitHubData';
import { useAnalytics } from '../hooks/useAnalytics';
import { useExportPDF } from '../hooks/useExportPDF';
import { languageDistribution, skillProgress } from '../data/sampleData';
import {
  Code,
  GitBranch,
  TrendingUp,
  ShieldCheck,
  Download,
  RefreshCw,
  Star,
  Sparkles,
  Zap,
  CheckCircle2,
} from 'lucide-react';
import { analysisAPI, profileAPI } from '../lib/api';

const Dashboard: FC = () => {
  const { user, logout } = useAuth();
  const [analysis, setAnalysis] = useState<any>(null);
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [runningAnalysis, setRunningAnalysis] = useState(false);

  const { commits, repositories, refreshData: refreshGitHubData } = useGitHubData();
  const { analytics, refreshAnalytics, getStreakInfo } = useAnalytics();
  const { exportToPDF, exporting, progress: pdfProgress } = useExportPDF();

  const fetchDashboardData = useCallback(async () => {
    setLoading(true);
    try {
      const [latestRes, statsRes] = await Promise.all([
        analysisAPI.getLatestAnalysis().catch(() => ({ data: null })),
        profileAPI.getUserStats().catch(() => ({ data: null })),
      ]);
      setAnalysis(latestRes.data);
      setStats(statsRes.data);
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchDashboardData();
  }, [fetchDashboardData]);

  const runAnalysis = async () => {
    setRunningAnalysis(true);
    try {
      await analysisAPI.triggerAnalysis(true);
      await Promise.all([fetchDashboardData(), refreshGitHubData(), refreshAnalytics()]);
    } catch (error) {
      console.error('Analysis failed:', error);
    } finally {
      setRunningAnalysis(false);
    }
  };

  const radarData = analysis
    ? [
        { category: 'Code Quality', score: analysis.code_quality_score || 0, fullMark: 100 },
        { category: 'Consistency', score: analysis.consistency_score || 0, fullMark: 100 },
        { category: 'Depth', score: analysis.depth_score || 0, fullMark: 100 },
        { category: 'Production', score: analysis.production_readiness_score || 0, fullMark: 100 },
        { category: 'Collaboration', score: 75, fullMark: 100 },
      ]
    : [
        { category: 'Code Quality', score: 92, fullMark: 100 },
        { category: 'Consistency', score: 78, fullMark: 100 },
        { category: 'Depth', score: 89, fullMark: 100 },
        { category: 'Production', score: 85, fullMark: 100 },
        { category: 'Collaboration', score: 75, fullMark: 100 },
      ];

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-slate-50">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-brand-500 mb-4"></div>
        <p className="text-lg font-medium text-slate-700">Loading your developer insights...</p>
        <p className="text-sm text-slate-500 mt-1">Fetching GitHub metrics & AI summaries</p>
      </div>
    );
  }

  const overallScore = analysis?.overall_score ?? 84.5;
  const avgComparison = Math.round(overallScore - (analytics?.comparisons.avgFullStack ?? 72));

  return (
    <div className="min-h-screen bg-slate-50">
      <DashboardSidebar username={user?.username || 'Developer'} avatarUrl={user?.avatar_url} />

      <main className="lg:ml-64 pb-16">
        {/* Top Navigation */}
        <div className="bg-white border-b border-slate-200 px-6 lg:px-8 py-4 sticky top-0 z-10 backdrop-blur-md bg-white/90">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h1 className="text-2xl font-bold text-slate-800 flex items-center gap-2">
                Welcome back, {user?.username || 'Developer'}! <Sparkles className="text-brand-500" size={20} />
              </h1>
              <p className="text-slate-500 text-sm">
                Last analyzed: {analysis?.created_at ? new Date(analysis.created_at).toLocaleDateString() : 'Active Demo Session'}
              </p>
            </div>
            <div className="flex items-center gap-3">
              <ActionButton
                variant="secondary"
                size="md"
                icon={Download}
                loading={exporting}
                onClick={() => exportToPDF()}
              >
                {exporting ? `Exporting (${pdfProgress}%)` : 'Export PDF Report'}
              </ActionButton>
              <button
                onClick={logout}
                className="px-4 py-2 text-sm font-medium text-slate-600 hover:text-red-600 hover:bg-red-50 rounded-lg transition"
              >
                Sign Out
              </button>
            </div>
          </div>
        </div>

        <div className="p-6 lg:p-8 space-y-8">
          {/* Main Action Banner */}
          <div className="bg-gradient-to-r from-brand-600 via-blue-600 to-indigo-700 rounded-2xl p-6 lg:p-8 text-white shadow-xl shadow-brand-500/10">
            <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
              <div>
                <div className="inline-flex items-center gap-2 px-3 py-1 bg-white/10 rounded-full text-xs font-semibold tracking-wide uppercase mb-3 backdrop-blur-sm">
                  <Zap size={14} className="text-amber-300" /> Developer Reputation Graph
                </div>
                <h2 className="text-3xl font-extrabold mb-2">Overall Score: {overallScore.toFixed(1)} / 100</h2>
                <p className="text-brand-100 max-w-xl text-sm leading-relaxed">
                  Synthesized from commit patterns, code velocity, test frameworks, architecture consistency, and repository footprint.
                </p>
                <div className="flex items-center gap-4 mt-4 text-sm font-medium">
                  <span className="flex items-center gap-1 bg-white/15 px-3 py-1 rounded-lg">
                    <TrendingUp size={16} className="text-emerald-300" />
                    +{avgComparison > 0 ? avgComparison : 0}% vs Industry Average
                  </span>
                  <span className="text-brand-200">Top 15% of Candidates</span>
                </div>
              </div>

              <div className="flex flex-col items-start md:items-end w-full md:w-auto">
                <ActionButton
                  variant="primary"
                  size="lg"
                  icon={RefreshCw}
                  loading={runningAnalysis}
                  onClick={runAnalysis}
                  className="bg-white text-brand-700 hover:bg-brand-50 shadow-lg"
                >
                  {runningAnalysis ? 'Analyzing GitHub Signals...' : 'Refresh Live Analysis'}
                </ActionButton>
                <p className="text-brand-200 text-xs mt-2">Real-time LLM & pipeline computation</p>
              </div>
            </div>
          </div>

          {/* Score Cards Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            <ScoreCard
              category="Code Quality"
              score={analysis?.code_quality_score ?? 92.0}
              description="Modular design, type hints, and linting compliance"
              icon={Code}
              trend="up"
            />
            <ScoreCard
              category="Contribution Consistency"
              score={analysis?.consistency_score ?? 78.0}
              description="Active commit cadence and maintenance velocity"
              icon={GitBranch}
              trend="stable"
            />
            <ScoreCard
              category="Technical Depth"
              score={analysis?.depth_score ?? 89.0}
              description="Multi-language proficiency and stack complexity"
              icon={ShieldCheck}
              trend="up"
            />
            <ScoreCard
              category="Production Readiness"
              score={analysis?.production_readiness_score ?? 85.0}
              description="CI/CD workflows, Docker configs, and automated tests"
              icon={TrendingUp}
              trend="up"
            />
          </div>

          {/* Charts & AI Recruiter Insights */}
          <div className="grid lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2">
              <RadarChart data={radarData} />
            </div>

            <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-6 flex flex-col justify-between">
              <div>
                <h3 className="font-bold text-slate-800 text-lg mb-4 flex items-center gap-2">
                  <Star className="text-amber-500" size={20} /> AI Recruiter Summary
                </h3>
                <p className="text-slate-600 text-sm leading-relaxed border-l-4 border-brand-500 pl-4 py-2 bg-slate-50/70 rounded-r-lg">
                  "{analysis?.recruiter_summary ||
                    'Strong candidate with demonstrated competence across modern web backends and typed frontends. Shows healthy testing patterns and structured commit habits.'}"
                </p>

                <div className="pt-4 mt-4 border-t border-slate-100">
                  <h4 className="font-semibold text-slate-700 text-sm mb-3">Key Strengths</h4>
                  <ul className="space-y-2">
                    {(analysis?.strengths && analysis.strengths.length > 0
                      ? analysis.strengths
                      : [
                          'Strong TypeScript and Python typing standards',
                          'Consistent test harness integration',
                          'Automated GitHub Actions CI/CD workflows',
                        ]
                    )
                      .slice(0, 3)
                      .map((strength: string, idx: number) => (
                        <li key={idx} className="flex items-start gap-2 text-xs text-slate-600">
                          <CheckCircle2 size={14} className="text-emerald-500 mt-0.5 shrink-0" />
                          <span>{strength}</span>
                        </li>
                      ))}
                  </ul>
                </div>
              </div>

              {analysis?.recommendations && (
                <div className="pt-4 mt-4 border-t border-slate-100">
                  <h4 className="font-semibold text-slate-700 text-sm mb-2">Growth Target</h4>
                  <p className="text-xs text-amber-700 bg-amber-50 p-2.5 rounded-lg border border-amber-100">
                    💡 {analysis.recommendations[0] || 'Expand unit test coverage across auxiliary endpoints.'}
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Module 9: Commits Timeline & Repository Analytics */}
          <div className="grid lg:grid-cols-2 gap-8">
            <CommitsTimeline data={commits} />
            <RepositoryGraph repositories={repositories} />
          </div>

          {/* Module 9: Skills & Language Distribution */}
          <div className="grid lg:grid-cols-2 gap-8">
            <SkillProgress skills={skillProgress} />
            <LanguageDistribution languages={languageDistribution} />
          </div>

          {/* Module 9: Advanced Predictive Analytics */}
          {analytics && (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
                <p className="text-slate-500 text-xs font-medium uppercase tracking-wider mb-1">
                  Predicted Next Month
                </p>
                <h2 className="text-3xl font-extrabold text-slate-800">
                  {analytics.predictions.nextMonth}
                  <span className="text-sm font-normal text-slate-400"> / 100</span>
                </h2>
                <p className="text-xs text-emerald-600 mt-2 font-medium flex items-center gap-1">
                  <TrendingUp size={14} /> Confidence: {analytics.predictions.confidence}%
                </p>
              </div>

              <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
                <p className="text-slate-500 text-xs font-medium uppercase tracking-wider mb-1">
                  Improvement Streak
                </p>
                <h2 className="text-3xl font-extrabold text-slate-800">
                  {getStreakInfo(analytics.scoreTrend)}
                  <span className="text-sm font-normal text-slate-400"> weeks</span>
                </h2>
                <p className="text-xs text-brand-600 mt-2 font-medium">Consistently growing pace</p>
              </div>

              <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
                <p className="text-slate-500 text-xs font-medium uppercase tracking-wider mb-1">
                  Vs Industry Benchmark
                </p>
                <h2 className="text-3xl font-extrabold text-slate-800">
                  {avgComparison >= 0 ? `+${avgComparison}` : avgComparison}
                  <span className="text-sm font-normal text-slate-400"> pts</span>
                </h2>
                <p className="text-xs text-emerald-600 mt-2 font-medium">Above full-stack median</p>
              </div>

              <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
                <p className="text-slate-500 text-xs font-medium uppercase tracking-wider mb-1">
                  Focus Recommendations
                </p>
                <h2 className="text-3xl font-extrabold text-slate-800">
                  {analytics.recommendations.length}
                </h2>
                <p className="text-xs text-slate-500 mt-2 font-medium">Actionable growth targets</p>
              </div>
            </div>
          )}

          {/* Module 9: PDF Export Section */}
          <div>
            <PDFExporter />
          </div>

          {/* Historical Activity Summary */}
          {stats && (
            <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-6">
              <h3 className="font-bold text-slate-800 text-lg mb-4">Historical Activity Overview</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                <div>
                  <p className="text-slate-500 text-xs">Total Analyses Executed</p>
                  <p className="text-2xl font-bold text-slate-800">{stats.total_analyses || 1}</p>
                </div>
                <div>
                  <p className="text-slate-500 text-xs">Average Overall Score</p>
                  <p className="text-2xl font-bold text-slate-800">{stats.average_overall_score ?? '84.5'}</p>
                </div>
                <div>
                  <p className="text-slate-500 text-xs">Latest Evaluated Score</p>
                  <p className="text-2xl font-bold text-slate-800">{stats.latest_overall_score ?? '84.5'}</p>
                </div>
                <div>
                  <p className="text-slate-500 text-xs">Score Trajectory</p>
                  <p className="text-2xl font-bold text-emerald-600 capitalize">
                    {stats.score_trend || 'Upward Growth'}
                  </p>
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
