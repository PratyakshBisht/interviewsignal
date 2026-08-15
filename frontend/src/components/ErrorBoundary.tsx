import React, { Component, ErrorInfo, ReactNode } from 'react';
import { AlertTriangle, RefreshCw, Home } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

const ErrorFallbackUI: React.FC<{
  error: Error | null;
  errorInfo: ErrorInfo | null;
  onReset: () => void;
}> = ({ error, errorInfo, onReset }) => {
  const navigate = useNavigate();

  const handleRetry = () => {
    onReset();
    window.location.reload();
  };

  const handleGoHome = () => {
    onReset();
    navigate('/');
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-slate-50 p-4">
      <div className="max-w-lg w-full bg-white rounded-xl shadow-lg p-8 border border-red-100">
        <div className="flex items-center justify-center mb-6">
          <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center">
            <AlertTriangle className="text-red-600" size={32} />
          </div>
        </div>

        <h1 className="text-2xl font-bold text-center text-red-700 mb-4">
          Something went wrong
        </h1>

        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
          <p className="text-red-800 font-medium mb-2">Error Details:</p>
          <code className="text-sm text-red-600 bg-red-100 p-2 rounded block overflow-x-auto">
            {error?.message || 'Unknown error occurred'}
          </code>
          {errorInfo && (
            <details className="mt-3">
              <summary className="text-sm text-red-700 cursor-pointer">
                Click for component stack
              </summary>
              <pre className="text-xs text-red-600 bg-red-50 p-2 mt-2 rounded overflow-auto max-h-40">
                {errorInfo.componentStack}
              </pre>
            </details>
          )}
        </div>

        <div className="text-center text-slate-600 mb-8">
          <p className="mb-2">
            We're sorry for the inconvenience. This error has been logged.
          </p>
          <p className="text-sm">
            If this persists, please contact support or try again later.
          </p>
        </div>

        <div className="flex flex-col sm:flex-row gap-4">
          <button
            onClick={handleRetry}
            className="flex-1 flex items-center justify-center gap-2 bg-brand-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-brand-700 transition"
          >
            <RefreshCw size={18} />
            Reload Application
          </button>
          <button
            onClick={handleGoHome}
            className="flex-1 flex items-center justify-center gap-2 bg-slate-100 text-slate-700 px-6 py-3 rounded-lg font-semibold hover:bg-slate-200 transition"
          >
            <Home size={18} />
            Go to Homepage
          </button>
        </div>
      </div>
    </div>
  );
};

export class ErrorBoundaryClass extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
    };
  }

  static getDerivedStateFromError(error: Error): State {
    return {
      hasError: true,
      error,
      errorInfo: null,
    };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('React ErrorBoundary caught an error:', error, errorInfo);
    this.setState({
      error,
      errorInfo,
    });

    if ((window as any).Sentry) {
      (window as any).Sentry.captureException(error, {
        extra: { componentStack: errorInfo.componentStack },
      });
    }
  }

  handleReset = () => {
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null,
    });
  };

  render() {
    const { hasError, error, errorInfo } = this.state;
    const { children } = this.props;

    if (hasError) {
      return (
        <ErrorFallbackUI
          error={error}
          errorInfo={errorInfo}
          onReset={this.handleReset}
        />
      );
    }

    return children;
  }
}

const ErrorBoundary: React.FC<Props> = ({ children }) => {
  return <ErrorBoundaryClass>{children}</ErrorBoundaryClass>;
};

export default ErrorBoundary;
