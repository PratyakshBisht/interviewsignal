import { FC } from 'react';
import { 
  Layout, 
  Github, 
  BarChart3, 
  ShieldCheck, 
  Users,
  Settings,
  Star,
  TrendingUp
} from 'lucide-react';
import clsx from 'clsx';

interface SidebarItem {
  icon: React.ElementType;
  label: string;
  active?: boolean;
  href?: string;
}

interface DashboardSidebarProps {
  username: string;
  avatarUrl?: string;
}

const DashboardSidebar: FC<DashboardSidebarProps> = ({ username, avatarUrl }) => {
  const navItems: SidebarItem[] = [
    { icon: Layout, label: 'Dashboard', active: true },
    { icon: Github, label: 'Repositories' },
    { icon: BarChart3, label: 'Analytics' },
    { icon: Star, label: 'Strengths' },
    { icon: TrendingUp, label: 'Progress' },
    { icon: Users, label: 'Community' },
    { icon: Settings, label: 'Settings' },
  ];

  return (
    <div className="w-64 bg-slate-900 text-white hidden lg:flex flex-col h-screen fixed">
      {/* Logo */}
      <div className="p-6 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <ShieldCheck className="text-brand-500" size={28} />
          <span className="text-2xl font-black italic tracking-tighter">InterviewSignal</span>
        </div>
      </div>

      {/* User Profile */}
      <div className="p-6 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-full bg-brand-500 flex items-center justify-center overflow-hidden">
            {avatarUrl ? (
              <img src={avatarUrl} alt={username} className="w-full h-full object-cover" />
            ) : (
              <span className="text-white font-bold text-lg">{username.charAt(0).toUpperCase()}</span>
            )}
          </div>
          <div>
            <h3 className="font-semibold text-lg">{username}</h3>
            <p className="text-slate-400 text-sm">Developer Profile</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4">
        <ul className="space-y-2">
          {navItems.map((item) => (
            <li key={item.label}>
              <a
                href={item.href || '#'}
                className={clsx(
                  'flex items-center gap-3 px-4 py-3 rounded-lg transition-all',
                  item.active
                    ? 'bg-slate-800 text-brand-300'
                    : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                )}
              >
                <item.icon size={20} />
                <span>{item.label}</span>
              </a>
            </li>
          ))}
        </ul>
      </nav>

      {/* Footer */}
      <div className="p-6 border-t border-slate-800">
        <p className="text-slate-400 text-sm">
          <span className="text-brand-500">✦</span> Powered by AI Insights
        </p>
        <p className="text-slate-500 text-xs mt-2">v1.0.0</p>
      </div>
    </div>
  );
};

export default DashboardSidebar;
