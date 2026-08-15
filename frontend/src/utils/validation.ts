export const isValidGitHubUsername = (username: string): boolean => {
  return /^[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38}$/i.test(username);
};

export const isValidEmail = (email: string): boolean => {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
};
