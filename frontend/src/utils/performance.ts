export const measurePerformance = <T extends (...args: any[]) => any>(
  fn: T,
  name: string
): ((...args: Parameters<T>) => ReturnType<T>) => {
  return (...args: Parameters<T>): ReturnType<T> => {
    const start = performance.now();
    const result = fn(...args);
    const end = performance.now();
    if (import.meta.env.DEV) {
      console.log(`[Performance] ${name} executed in ${(end - start).toFixed(2)}ms`);
    }
    return result;
  };
};

export const getNavigationTimings = () => {
  if (typeof window === 'undefined' || !window.performance) {
    return null;
  }
  const [nav] = performance.getEntriesByType('navigation') as PerformanceNavigationTiming[];
  if (!nav) return null;

  return {
    dns: nav.domainLookupEnd - nav.domainLookupStart,
    tls: nav.connectEnd - nav.secureConnectionStart,
    ttfb: nav.responseStart - nav.requestStart,
    domReady: nav.domContentLoadedEventEnd - nav.startTime,
    loadComplete: nav.loadEventEnd - nav.startTime,
  };
};
