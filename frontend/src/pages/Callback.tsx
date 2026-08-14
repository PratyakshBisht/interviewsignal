import { FC, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { authAPI } from '../lib/api';
import { CheckCircle, AlertCircle } from 'lucide-react';

const Callback: FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const code = searchParams.get('code');
  const error = searchParams.get('error');

  useEffect(() => {
    const handleCallback = async () => {
      if (error) {
        console.error('GitHub OAuth error:', error);
        navigate('/');
        return;
      }

      if (code) {
        try {
          const response = await authAPI.handleCallback(code);
          localStorage.setItem('token', response.data.access_token);
          setTimeout(() => navigate('/dashboard'), 1500);
        } catch (err) {
          console.error('Authentication failed:', err);
          navigate('/');
        }
      } else {
        navigate('/');
      }
    };

    handleCallback();
  }, [code, error, navigate]);

  if (error) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-slate-50">
        <div className="bg-red-50 border border-red-200 rounded-xl p-8 max-w-lg text-center">
          <AlertCircle className="text-red-500 mx-auto mb-4" size={48} />
          <h2 className="text-2xl font-bold text-red-700 mb-2">Authentication Failed</h2>
          <p className="text-red-600 mb-6">
            We couldn't authenticate you with GitHub. Please try again or contact support if the issue persists.
          </p>
          <button
            onClick={() => navigate('/')}
            className="bg-red-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-red-700 transition"
          >
            Return to Home
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-slate-50">
      <div className="text-center">
        <CheckCircle className="text-brand-500 mx-auto mb-6" size={64} />
        <h1 className="text-3xl font-bold text-slate-800 mb-4">Authentication Successful!</h1>
        <p className="text-slate-600 mb-8">Redirecting you to your dashboard...</p>
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-brand-500 mx-auto"></div>
        <p className="text-slate-500 text-sm mt-6">Securely connecting your GitHub account</p>
      </div>
    </div>
  );
};

export default Callback;
