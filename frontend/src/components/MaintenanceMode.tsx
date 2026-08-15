import { FC } from 'react';
import { Wrench, Clock, Mail, RefreshCw } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

interface MaintenanceModeProps {
  scheduledStart?: string;
  scheduledEnd?: string;
  reason?: string;
  contactEmail?: string;
}

const MaintenanceMode: FC<MaintenanceModeProps> = ({
  scheduledStart = 'Soon',
  scheduledEnd = 'Within 2 hours',
  reason = 'System upgrade and maintenance',
  contactEmail = 'support@interviewsignal.app',
}) => {
  const navigate = useNavigate();

  const handleRetry = () => {
    window.location.reload();
  };

  const handleGoHome = () => {
    navigate('/');
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-slate-900 to-slate-800 p-4">
      <div className="max-w-xl w-full bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 text-white">
        <div className="flex flex-col items-center text-center mb-8">
          <div className="w-20 h-20 bg-white/10 rounded-full flex items-center justify-center mb-6">
            <Wrench size={40} className="text-brand-300" />
          </div>
          <h1 className="text-3xl font-bold mb-4">Under Maintenance</h1>
          <p className="text-lg text-white/80 mb-2">
            InterviewSignal is currently undergoing scheduled maintenance
          </p>
        </div>

        <div className="bg-white/5 rounded-xl p-6 mb-8 space-y-4">
          <div className="flex items-center gap-4">
            <Clock className="text-brand-300" size={24} />
            <div>
              <h3 className="font-bold text-lg">Maintenance Schedule</h3>
              <p className="text-white/70">
                {scheduledStart} → {scheduledEnd}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <Wrench className="text-brand-300" size={24} />
            <div>
              <h3 className="font-bold text-lg">Reason</h3>
              <p className="text-white/70">{reason}</p>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <Mail className="text-brand-300" size={24} />
            <div>
              <h3 className="font-bold text-lg">Contact Support</h3>
              <a
                href={`mailto:${contactEmail}`}
                className="text-brand-300 hover:text-brand-200 transition"
              >
                {contactEmail}
              </a>
            </div>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-4">
          <button
            onClick={handleRetry}
            className="flex items-center justify-center gap-3 bg-brand-500 text-white px-6 py-4 rounded-xl font-bold hover:bg-brand-600 transition-all"
          >
            <RefreshCw size={20} />
            Check Status
          </button>
          <button
            onClick={handleGoHome}
            className="flex items-center justify-center gap-3 bg-white/10 border border-white/30 text-white px-6 py-4 rounded-xl font-bold hover:bg-white/20 transition"
          >
            Return to Homepage
          </button>
        </div>

        {/* Progress indicator */}
        <div className="mt-8">
          <div className="flex justify-between text-sm text-white/60 mb-2">
            <span>Maintenance Progress</span>
            <span>~60%</span>
          </div>
          <div className="w-full bg-white/10 rounded-full h-3">
            <div
              className="bg-gradient-to-r from-brand-400 to-blue-500 rounded-full h-3 animate-pulse"
              style={{ width: '60%' }}
            ></div>
          </div>
        </div>

        {/* Live status updates */}
        <div className="mt-8 pt-6 border-t border-white/20">
          <h4 className="font-bold mb-4">Recent Updates</h4>
          <div className="space-y-3">
            <div className="flex items-center gap-3">
              <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
              <span className="text-sm text-white/80">
                Database migration complete
              </span>
              <span className="text-xs text-white/60 ml-auto">2 min ago</span>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-2 h-2 rounded-full bg-amber-500 animate-pulse"></div>
              <span className="text-sm text-white/80">
                Frontend deployment in progress
              </span>
              <span className="text-xs text-white/60 ml-auto">5 min ago</span>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-2 h-2 rounded-full bg-blue-500 animate-pulse"></div>
              <span className="text-sm text-white/80">
                API services restarting
              </span>
              <span className="text-xs text-white/60 ml-auto">10 min ago</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MaintenanceMode;
