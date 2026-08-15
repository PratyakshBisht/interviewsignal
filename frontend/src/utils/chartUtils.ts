export const getScoreColor = (score: number): string => {
  if (score >= 80) return '#10b981'; // Emerald 500
  if (score >= 60) return '#3b82f6'; // Blue 500
  if (score >= 40) return '#f59e0b'; // Amber 500
  return '#ef4444'; // Red 500
};

export const formatScorePercentage = (score: number, maxScore: number = 100): string => {
  return `${((score / maxScore) * 100).toFixed(1)}%`;
};
