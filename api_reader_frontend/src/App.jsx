import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { UserProvider } from './context/UserContext';
import { ThemeProvider } from './context/ThemeContext';
import Navbar from './components/Navbar';
import SettingsModal from './components/SettingsModal';
import HomePage from './pages/HomePage';
import DocsPage from './pages/DocsPage';
import ChatPage from './pages/ChatPage';
import { useState } from 'react';

function App() {
  const [settingsOpen, setSettingsOpen] = useState(false);

  return (
    <UserProvider>
      <ThemeProvider>
        <BrowserRouter>
          {/* Main layout container */}
          <div className="flex flex-col h-screen w-full bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100">
            {/* Top navigation bar */}
            <Navbar onOpenSettings={() => setSettingsOpen(true)} />
            {/* Content area for pages */}
            <div className="flex-1 overflow-hidden">
              <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/docs" element={<DocsPage />} />
                <Route path="/chat/:apiId" element={<ChatPage />} />
              </Routes>
            </div>
            {/* Settings modal */}
            {settingsOpen && <SettingsModal onClose={() => setSettingsOpen(false)} />}
          </div>
        </BrowserRouter>
      </ThemeProvider>
    </UserProvider>
  );
}

export default App;

