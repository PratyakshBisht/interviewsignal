import React, { createContext, useContext, useState, useEffect } from 'react';

export interface User {
  id?: number;
  username: string;
  name?: string;
  avatar_url?: string;
  email?: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (token: string, user: User) => void;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem('interviewsignal_token'));

  useEffect(() => {
    const savedUser = localStorage.getItem('interviewsignal_user');
    if (savedUser && token) {
      try {
        setUser(JSON.parse(savedUser));
      } catch (e) {
        console.error('Failed to parse user session', e);
      }
    }
  }, [token]);

  const login = (newToken: string, newUser: User) => {
    localStorage.setItem('interviewsignal_token', newToken);
    localStorage.setItem('interviewsignal_user', JSON.stringify(newUser));
    setToken(newToken);
    setUser(newUser);
  };

  const logout = () => {
    localStorage.removeItem('interviewsignal_token');
    localStorage.removeItem('interviewsignal_user');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout, isAuthenticated: !!token }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
