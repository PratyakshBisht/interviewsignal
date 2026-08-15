export const initSentry = () => {
  const dsn = import.meta.env.VITE_SENTRY_DSN;
  if (!dsn || typeof window === 'undefined' || !(window as any).Sentry) {
    return;
  }

  (window as any).Sentry.init({
    dsn,
    environment: import.meta.env.VITE_ENVIRONMENT || 'production',
    release: `interviewsignal@${import.meta.env.VITE_APP_VERSION || '1.0.0'}`,
    tracesSampleRate: 0.1,
  });
};

export const captureException = (error: Error, extra: Record<string, any> = {}) => {
  if (typeof window !== 'undefined' && (window as any).Sentry) {
    (window as any).Sentry.captureException(error, { extra });
  } else {
    console.error('Unhandled exception:', error, extra);
  }
};
