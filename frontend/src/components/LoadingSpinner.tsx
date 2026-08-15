import { FC } from 'react';
import { Loader2 } from 'lucide-react';

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg' | 'xl';
  fullScreen?: boolean;
  text?: string;
  className?: string;
}

const LoadingSpinner: FC<LoadingSpinnerProps> = ({
  size = 'md',
  fullScreen = false,
  text = 'Loading...',
  className = '',
}) => {
  const sizeClasses = {
    sm: 'h-4 w-4',
    md: 'h-6 w-6',
    lg: 'h-8 w-8',
    xl: 'h-12 w-12',
  };

  const containerClasses = fullScreen
    ? 'min-h-screen flex flex-col items-center justify-center bg-slate-50'
    : 'flex flex-col items-center justify-center';

  return (
    <div className={`${containerClasses} ${className}`}>
      <Loader2 className={`${sizeClasses[size]} animate-spin text-brand-500`} />
      {text && (
        <p className="mt-3 text-slate-600 text-sm font-medium animate-pulse">
          {text}
        </p>
      )}
    </div>
  );
};

export default LoadingSpinner;
