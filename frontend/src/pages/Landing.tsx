import { FC } from 'react';
import { useAuth } from '../context/AuthContext';
import { Github, ShieldCheck, TrendingUp, Users, BarChart3 } from 'lucide-react';

const Landing: FC = () => {
  const { loginWithGithub } = useAuth();

  const features = [
    {
      icon: TrendingUp,
      title: 'Track Progress',
      description: 'Monitor your GitHub contributions over time',
      color: 'text-blue-500',
      bgColor: 'bg-blue-50'
    },
    {
      icon: ShieldCheck,
      title: 'Verified Scores',
      description: 'AI-powered analysis of your code quality',
      color: 'text-emerald-500',
      bgColor: 'bg-emerald-50'
    },
    {
      icon: Users,
      title: 'Recruiter Ready',
      description: 'Export professional reports for interviews',
      color: 'text-purple-500',
      bgColor: 'bg-purple-50'
    },
    {
      icon: BarChart3,
      title: 'Deep Insights',
      description: 'Understand your development strengths',
      color: 'text-amber-500',
      bgColor: 'bg-amber-50'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 text-white">
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-16 md:py-24">
        <div className="max-w-6xl mx-auto">
          {/* Logo/Nav */}
          <div className="flex items-center justify-between mb-16">
            <div className="flex items-center gap-3">
              <ShieldCheck className="text-brand-500" size={32} />
              <span className="text-3xl font-black italic tracking-tighter">InterviewSignal</span>
            </div>
            <div className="hidden md:flex items-center gap-6 text-slate-300">
              <a href="#" className="hover:text-white transition">How it works</a>
              <a href="#" className="hover:text-white transition">Pricing</a>
              <a href="#" className="hover:text-white transition">FAQ</a>
            </div>
          </div>

          {/* Main Hero */}
          <div className="grid md:grid-cols-2 gap-12 items-center mb-24">
            <div>
              <h1 className="text-5xl md:text-6xl font-black leading-tight mb-6">
                Turn your <span className="text-brand-500">GitHub activity</span> into recruiter-ready insights
              </h1>
              <p className="text-xl text-slate-300 mb-8 leading-relaxed">
                Get AI-powered analysis of your code quality, contribution consistency, and technical depth. Impress recruiters with data-backed developer reputation.
              </p>
              <div className="flex flex-col sm:flex-row gap-4">
                <button
                  onClick={loginWithGithub}
                  className="inline-flex items-center justify-center gap-3 bg-brand-600 text-white px-8 py-4 rounded-xl font-bold text-lg hover:bg-brand-700 transition-all shadow-lg shadow-brand-500/30"
                >
                  <Github size={24} />
                  Analyze My GitHub Profile
                </button>
                <button className="inline-flex items-center justify-center gap-3 border border-slate-600 text-slate-300 px-8 py-4 rounded-xl font-semibold hover:bg-slate-800 transition">
                  See Live Demo
                </button>
              </div>
            </div>
            <div className="relative">
              <div className="bg-slate-800/50 backdrop-blur-sm rounded-2xl p-8 border border-slate-700">
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-12 h-12 rounded-full bg-brand-500 flex items-center justify-center">
                    <ShieldCheck size={24} />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold">Sample Developer Profile</h3>
                    <p className="text-slate-400">Overall Score: 84.5</p>
                  </div>
                </div>
                <div className="space-y-4">
                  {[
                    { label: 'Code Quality', score: 92 },
                    { label: 'Consistency', score: 78 },
                    { label: 'Production Readiness', score: 85 },
                    { label: 'Technical Depth', score: 89 }
                  ].map((item) => (
                    <div key={item.label} className="flex items-center justify-between">
                      <span className="text-slate-300">{item.label}</span>
                      <div className="flex items-center gap-2">
                        <div className="w-24 h-2 bg-slate-700 rounded-full overflow-hidden">
                          <div 
                            className="h-full bg-brand-500 rounded-full"
                            style={{ width: `${item.score}%` }}
                          />
                        </div>
                        <span className="font-bold">{item.score}%</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Features */}
          <div className="mb-24">
            <h2 className="text-3xl font-bold text-center mb-12">Why Choose InterviewSignal?</h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              {features.map((feature) => (
                <div key={feature.title} className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700 hover:border-brand-500 transition">
                  <div className={`${feature.bgColor} ${feature.color} w-12 h-12 rounded-lg flex items-center justify-center mb-4`}>
                    <feature.icon size={24} />
                  </div>
                  <h3 className="text-xl font-bold mb-2">{feature.title}</h3>
                  <p className="text-slate-400">{feature.description}</p>
                </div>
              ))}
            </div>
          </div>

          {/* CTA */}
          <div className="text-center">
            <h2 className="text-3xl font-bold mb-8">Ready to showcase your skills?</h2>
            <button
              onClick={loginWithGithub}
              className="inline-flex items-center justify-center gap-3 bg-brand-600 text-white px-12 py-5 rounded-xl font-bold text-xl hover:bg-brand-700 transition-all shadow-2xl shadow-brand-500/40 animate-pulse"
            >
              <Github size={28} />
              Start Free Analysis
            </button>
            <p className="text-slate-400 mt-4">No credit card required • 100% free for students</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Landing;
