import { useEffect } from 'react';

declare global {
  interface Window {
    Sentry?: any;
    gtag?: (...args: any[]) => void;
  }
}

interface ErrorContext {
  component: string;
  userId?: string;
  pathname: string;
  userAgent: string;
}

export const useErrorTracking = (enabled: boolean = true) => {
  useEffect(() => {
    if (!enabled || !import.meta.env.PROD) {
      return;
    }

    // Initialize Sentry if available
    if (window.Sentry) {
      window.Sentry.init({
        dsn: import.meta.env.VITE_SENTRY_DSN,
        environment: import.meta.env.VITE_ENVIRONMENT || 'development',
        release: `interviewsignal@${import.meta.env.VITE_APP_VERSION || '1.0.0'}`,
        tracesSampleRate: 0.1,
        replaysSessionSampleRate: 0.1,
        replaysOnErrorSampleRate: 1.0,

        beforeSend(event: any) {
          if (event.exception?.values?.[0]?.value?.includes('chrome-extension://')) {
            return null;
          }

          event.tags = {
            ...event.tags,
            frontend: 'react',
            environment: import.meta.env.VITE_ENVIRONMENT,
          };

          return event;
        },
      });
    }

    const handleGlobalError = (event: ErrorEvent) => {
      console.error('Global error caught:', event.error);

      if (window.Sentry) {
        window.Sentry.captureException(event.error, {
          extra: {
            component: 'global',
            pathname: window.location.pathname,
            userAgent: navigator.userAgent,
          },
        });
      }

      if (window.gtag && import.meta.env.VITE_GA_TRACKING_ID) {
        window.gtag('event', 'exception', {
          description: event.error?.message || 'Unknown error',
          fatal: false,
        });
      }
    };

    const handleUnhandledRejection = (event: PromiseRejectionEvent) => {
      console.error('Unhandled promise rejection:', event.reason);

      if (window.Sentry) {
        window.Sentry.captureException(event.reason, {
          extra: {
            component: 'promise',
            type: 'unhandled_rejection',
          },
        });
      }
    };

    window.addEventListener('error', handleGlobalError);
    window.addEventListener('unhandledrejection', handleUnhandledRejection);

    return () => {
      window.removeEventListener('error', handleGlobalError);
      window.removeEventListener('unhandledrejection', handleUnhandledRejection);
    };
  }, [enabled]);

  const trackError = (error: Error, context: Partial<ErrorContext> = {}) => {
    console.error('Tracked error:', error, context);

    if (window.Sentry) {
      window.Sentry.withScope((scope: any) => {
        scope.setExtras({
          component: context.component || 'unknown',
          userId: context.userId,
          pathname: context.pathname || window.location.pathname,
          userAgent: navigator.userAgent,
          timestamp: new Date().toISOString(),
        });

        window.Sentry.captureException(error);
      });
    }

    if (window.gtag && import.meta.env.VITE_GA_TRACKING_ID) {
      window.gtag('event', 'exception', {
        description: error.message,
        fatal: false,
      });
    }
  };

  const trackEvent = (eventName: string, eventData: any = {}) => {
    if (window.gtag && import.meta.env.VITE_GA_TRACKING_ID) {
      window.gtag('event', eventName, eventData);
    }

    if (import.meta.env.DEV) {
      console.log(`Event tracked: ${eventName}`, eventData);
    }
  };

  const setUser = (userId: string, userData: any = {}) => {
    if (window.Sentry) {
      window.Sentry.setUser({
        id: userId,
        ...userData,
      });
    }
  };

  const clearUser = () => {
    if (window.Sentry) {
      window.Sentry.setUser(null);
    }
  };

  return {
    trackError,
    trackEvent,
    setUser,
    clearUser,
  };
};
