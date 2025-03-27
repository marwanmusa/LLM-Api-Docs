import { useContext, useState } from 'react';
import { UserContext } from '../context/UserContext';
import { ThemeContext } from '../context/ThemeContext';

export default function Navbar({ onOpenSettings }) {
  const { user, setUser } = useContext(UserContext);
  const { dark, toggleDark } = useContext(ThemeContext);
  const [menuOpen, setMenuOpen] = useState(false);

  const handleLogout = () => {
    setUser(null);
    setMenuOpen(false);
  };

  const handleLogin = () => {
    // For demo purposes, set a dummy user on login
    setUser({ name: 'Demo User', avatar: 'https://i.pravatar.cc/40?u=demo' });
    setMenuOpen(false);
  };

  return (
    <nav className="flex items-center justify-between px-4 py-2 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
      <h1 className="text-lg font-bold text-gray-800 dark:text-gray-100">SwaggerChat</h1>
      <div className="flex items-center space-x-4">
        {/* Dark mode toggle */}
        <button onClick={toggleDark} className="text-xl">
          {dark ? '🌞' : '🌙'}
        </button>
        {/* Avatar and dropdown */}
        <div className="relative">
          <img
            src={user ? user.avatar : "https://i.pravatar.cc/40?u=guest"}
            alt="User Avatar"
            className="w-8 h-8 rounded-full cursor-pointer"
            onClick={() => setMenuOpen(!menuOpen)}
          />
          {menuOpen && (
            <ul className="absolute right-0 mt-2 w-40 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded shadow-lg">
              <li>
                <button 
                  onClick={() => { setMenuOpen(false); onOpenSettings(); }}
                  className="block w-full text-left px-4 py-2 text-sm hover:bg-gray-100 dark:hover:bg-gray-700"
                >
                  Settings
                </button>
              </li>
              {user ? (
                <li>
                  <button 
                    onClick={handleLogout}
                    className="block w-full text-left px-4 py-2 text-sm hover:bg-gray-100 dark:hover:bg-gray-700"
                  >
                    Logout
                  </button>
                </li>
              ) : (
                <li>
                  <button 
                    onClick={handleLogin}
                    className="block w-full text-left px-4 py-2 text-sm hover:bg-gray-100 dark:hover:bg-gray-700"
                  >
                    Login
                  </button>
                </li>
              )}
            </ul>
          )}
        </div>
      </div>
    </nav>
  );
} 