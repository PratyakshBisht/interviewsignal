export const formatPDFFileName = (username?: string): string => {
  const sanitized = (username || 'developer').replace(/[^a-zA-Z0-9_-]/g, '_');
  const dateStr = new Date().toISOString().split('T')[0];
  return `InterviewSignal_${sanitized}_${dateStr}.pdf`;
};

export const sanitizeReportText = (text?: string): string => {
  if (!text) return '';
  return text.replace(/[\u0000-\u001F\u007F-\u009F]/g, '').trim();
};
