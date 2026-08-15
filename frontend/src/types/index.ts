export interface User {
  id: number;
  username: string;
  email: string;
  avatar_url: string;
  github_id: number;
  bio?: string;
  company?: string;
  location?: string;
  created_at: string;
  last_analysis_at?: string;
}

export interface Analysis {
  id: number;
  user_id: number;
  overall_score: number;
  code_quality_score: number;
  consistency_score: number;
  depth_score: number;
  production_readiness_score: number;
  recruiter_summary: string;
  strengths: string[];
  weaknesses: string[];
  recommendations: string[];
  created_at: string;
  updated_at: string;
  github_data?: any;
  analysis_version?: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}
