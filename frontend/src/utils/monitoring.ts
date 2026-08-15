import api from '../lib/api';

export interface PerformanceMetrics {
  pageLoadTime: number;
  apiResponseTime: number;
  memoryUsage: number;
  networkLatency: number;
  errorsCount: number;
}

export interface SystemHealth {
  status: 'healthy' | 'degraded' | 'unhealthy';
  timestamp: string;
  metrics: PerformanceMetrics;
  dependencies: {
    api: boolean;
    database: boolean;
    cache: boolean;
    externalServices: boolean;
  };
}

export class MonitoringService {
  private static instance: MonitoringService;
  private metrics: PerformanceMetrics[] = [];
  private maxMetrics = 100;

  private constructor() {
    this.initializePerformanceObserver();
  }

  static getInstance(): MonitoringService {
    if (!MonitoringService.instance) {
      MonitoringService.instance = new MonitoringService();
    }
    return MonitoringService.instance;
  }

  private initializePerformanceObserver() {
    if (typeof PerformanceObserver === 'undefined') {
      return;
    }

    try {
      // Observe Largest Contentful Paint
      const lcpObserver = new PerformanceObserver((entryList) => {
        const entries = entryList.getEntries();
        const lastEntry = entries[entries.length - 1];
        if (import.meta.env.DEV) {
          console.log('LCP:', lastEntry?.startTime || 0);
        }
      });

      lcpObserver.observe({ type: 'largest-contentful-paint', buffered: true });

      // Observe Layout Shift
      const clsObserver = new PerformanceObserver((entryList) => {
        const entries = entryList.getEntries();
        const cls = entries.reduce((sum: number, entry: any) => sum + (entry.value || 0), 0);
        if (import.meta.env.DEV) {
          console.log('CLS:', cls);
        }
      });

      clsObserver.observe({ type: 'layout-shift', buffered: true });
    } catch (error) {
      console.warn('Performance observer initialization failed:', error);
    }
  }

  trackPageLoad() {
    if (typeof window !== 'undefined' && window.performance) {
      const navigationTiming = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;

      if (navigationTiming) {
        const metrics: PerformanceMetrics = {
          pageLoadTime: navigationTiming.loadEventEnd - navigationTiming.loadEventStart,
          apiResponseTime: 0,
          memoryUsage: (performance as any).memory?.usedJSHeapSize || 0,
          networkLatency: navigationTiming.responseEnd - navigationTiming.requestStart,
          errorsCount: 0,
        };

        this.addMetric(metrics);
        this.sendMetrics(metrics);
      }
    }
  }

  trackApiCall(method: string, url: string, duration: number, status: number) {
    const metric: PerformanceMetrics = {
      pageLoadTime: 0,
      apiResponseTime: duration,
      memoryUsage: (performance as any).memory?.usedJSHeapSize || 0,
      networkLatency: 0,
      errorsCount: status >= 400 ? 1 : 0,
    };

    this.addMetric(metric);

    if (duration > 1500) {
      console.warn(`Slow API call detected: ${method} ${url} took ${duration}ms`);
    }
  }

  trackError(error: Error, context: any = {}) {
    const metric: PerformanceMetrics = {
      pageLoadTime: 0,
      apiResponseTime: 0,
      memoryUsage: 0,
      networkLatency: 0,
      errorsCount: 1,
    };

    this.addMetric(metric);
    this.sendErrorToServer(error, context);
  }

  private addMetric(metric: PerformanceMetrics) {
    this.metrics.push(metric);
    if (this.metrics.length > this.maxMetrics) {
      this.metrics = this.metrics.slice(-this.maxMetrics);
    }
  }

  private async sendMetrics(metrics: PerformanceMetrics) {
    if (!import.meta.env.PROD) {
      return;
    }

    try {
      await api.post('/monitoring/metrics', {
        metrics,
        timestamp: new Date().toISOString(),
        userAgent: navigator.userAgent,
        pathname: window.location.pathname,
        viewport: `${window.innerWidth}x${window.innerHeight}`,
      });
    } catch {
      // Silently ignore telemetry failure in dev/prod
    }
  }

  private async sendErrorToServer(error: Error, context: any) {
    if (!import.meta.env.PROD) {
      return;
    }

    try {
      await api.post('/monitoring/errors', {
        error: {
          message: error.message,
          stack: error.stack,
          name: error.name,
        },
        context: {
          ...context,
          url: window.location.href,
          userAgent: navigator.userAgent,
          timestamp: new Date().toISOString(),
        },
      });
    } catch {
      // Silently ignore telemetry failure
    }
  }

  getHealthStatus(): Promise<SystemHealth> {
    return api.get('/health').then((response) => response.data);
  }

  getAverageMetrics(): Partial<PerformanceMetrics> {
    if (this.metrics.length === 0) {
      return {};
    }

    const sum = this.metrics.reduce(
      (acc, metric) => ({
        pageLoadTime: acc.pageLoadTime + metric.pageLoadTime,
        apiResponseTime: acc.apiResponseTime + metric.apiResponseTime,
        memoryUsage: acc.memoryUsage + metric.memoryUsage,
        networkLatency: acc.networkLatency + metric.networkLatency,
        errorsCount: acc.errorsCount + metric.errorsCount,
      }),
      {
        pageLoadTime: 0,
        apiResponseTime: 0,
        memoryUsage: 0,
        networkLatency: 0,
        errorsCount: 0,
      }
    );

    const count = this.metrics.length;
    return {
      pageLoadTime: sum.pageLoadTime / count,
      apiResponseTime: sum.apiResponseTime / count,
      memoryUsage: sum.memoryUsage / count,
      networkLatency: sum.networkLatency / count,
      errorsCount: sum.errorsCount,
    };
  }

  clearMetrics() {
    this.metrics = [];
  }
}

export const monitoringService = MonitoringService.getInstance();
