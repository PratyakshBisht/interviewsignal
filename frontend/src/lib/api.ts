import axios from 'axios';
import type { User, Analysis, AuthResponse } from '../types';

const API_BASE = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add JWT token to requests automatically
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  getGitHubAuthURL: () => api.get<{ authorization_url: string }>('/auth/login/github'),
  handleCallback: (code: string) => api.get<AuthResponse>(`/auth/callback?code=${code}`),
  getUserInfo: () => api.get<User>('/auth/me'),
};

export const analysisAPI = {
  triggerAnalysis: (forceRefresh: boolean = false) => 
    api.post<Analysis>('/analysis/trigger', { force_refresh: forceRefresh }),
  getLatestAnalysis: () => api.get<Analysis>('/analysis/latest'),
  getAnalysisHistory: (limit: number = 10) => 
    api.get<{ total: number; history: Analysis[] }>(`/analysis/history?limit=${limit}`),
  getStats: () => api.get('/analysis/stats/overall'),
};

export const profileAPI = {
  getUserStats: () => api.get('/profile/stats'),
  getUserRepos: () => api.get('/profile/repos/summary'),
};

export default api;
