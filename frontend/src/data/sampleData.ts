export interface CommitDataPoint {
  date: string;
  commits: number;
  lines_added: number;
  lines_deleted: number;
}

export interface RepositoryStats {
  name: string;
  stars: number;
  forks: number;
  commits: number;
  issues: number;
  prs: number;
  size_kb: number;
  languages: [string, number][];
}

export interface TimelineEvent {
  date: string;
  title: string;
  description: string;
  type: 'commit' | 'pr' | 'issue' | 'release';
  repo: string;
}

export const mockCommits: CommitDataPoint[] = [
  { date: '2024-01-15', commits: 8, lines_added: 245, lines_deleted: 45 },
  { date: '2024-01-22', commits: 12, lines_added: 512, lines_deleted: 89 },
  { date: '2024-01-29', commits: 5, lines_added: 128, lines_deleted: 12 },
  { date: '2024-02-05', commits: 15, lines_added: 842, lines_deleted: 156 },
  { date: '2024-02-12', commits: 9, lines_added: 342, lines_deleted: 67 },
  { date: '2024-02-19', commits: 11, lines_added: 498, lines_deleted: 92 },
  { date: '2024-02-26', commits: 6, lines_added: 167, lines_deleted: 34 },
  { date: '2024-03-04', commits: 14, lines_added: 745, lines_deleted: 128 },
];

export const mockRepositories: RepositoryStats[] = [
  {
    name: 'interviewsignal',
    stars: 42,
    forks: 12,
    commits: 245,
    issues: 6,
    prs: 18,
    size_kb: 4520,
    languages: [['TypeScript', 45], ['Python', 35], ['CSS', 20]],
  },
  {
    name: 'secure-ai-guardian',
    stars: 28,
    forks: 8,
    commits: 189,
    issues: 3,
    prs: 9,
    size_kb: 6120,
    languages: [['Python', 60], ['JavaScript', 30], ['Dockerfile', 10]],
  },
  {
    name: 'personal-portfolio',
    stars: 15,
    forks: 3,
    commits: 87,
    issues: 0,
    prs: 2,
    size_kb: 1850,
    languages: [['JavaScript', 70], ['HTML', 20], ['CSS', 10]],
  },
];

export const mockTimeline: TimelineEvent[] = [
  {
    date: '2024-01-10',
    title: 'Initial Project Setup',
    description: 'Created project structure',
    type: 'commit',
    repo: 'interviewsignal',
  },
  {
    date: '2024-01-15',
    title: 'Added Authentication',
    description: 'Implemented GitHub OAuth flow',
    type: 'pr',
    repo: 'interviewsignal',
  },
  {
    date: '2024-01-22',
    title: 'Fixed Security Bug',
    description: 'Patched XSS vulnerability',
    type: 'commit',
    repo: 'secure-ai-guardian',
  },
  {
    date: '2024-01-28',
    title: 'Added CI/CD Pipeline',
    description: 'GitHub Actions workflow',
    type: 'pr',
    repo: 'interviewsignal',
  },
  {
    date: '2024-02-05',
    title: 'Database Optimization',
    description: 'Improved query performance by 40%',
    type: 'commit',
    repo: 'interviewsignal',
  },
  {
    date: '2024-02-12',
    title: 'Major Release v1.0',
    description: 'Production-ready launch',
    type: 'release',
    repo: 'interviewsignal',
  },
  {
    date: '2024-02-20',
    title: 'Added Test Coverage',
    description: 'Increased to 85% coverage',
    type: 'pr',
    repo: 'secure-ai-guardian',
  },
  {
    date: '2024-02-28',
    title: 'Performance Monitoring',
    description: 'Added Sentry integration',
    type: 'commit',
    repo: 'interviewsignal',
  },
];

export const skillProgress = [
  { skill: 'React', level: 85, target: 90 },
  { skill: 'TypeScript', level: 80, target: 95 },
  { skill: 'Python', level: 75, target: 85 },
  { skill: 'Docker', level: 60, target: 80 },
  { skill: 'CI/CD', level: 70, target: 85 },
  { skill: 'Testing', level: 65, target: 80 },
];

export const languageDistribution = [
  { language: 'TypeScript', percentage: 45, color: '#3178c6' },
  { language: 'Python', percentage: 30, color: '#3572A5' },
  { language: 'JavaScript', percentage: 15, color: '#f1e05a' },
  { language: 'CSS', percentage: 5, color: '#563d7c' },
  { language: 'Other', percentage: 5, color: '#94a3b8' },
];
