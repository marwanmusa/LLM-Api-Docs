import { createContext, useState } from 'react';

export const UserContext = createContext(null);

export function UserProvider({ children }) {
  // Manage user login state and OpenAI API key here
  const [user, setUser] = useState({
    name: 'John Doe',
    avatar: 'https://i.pravatar.cc/40?u=johndoe'  // placeholder avatar image
  });
  const [apiKey, setApiKey] = useState('');

  return (
    <UserContext.Provider value={{ user, setUser, apiKey, setApiKey }}>
      {children}
    </UserContext.Provider>
  );
} 