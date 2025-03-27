import { useContext, useState } from 'react';
import { UserContext } from '../context/UserContext';

export default function SettingsModal({ onClose }) {
  const { user, setUser, apiKey, setApiKey } = useContext(UserContext);
  const [tempKey, setTempKey] = useState(apiKey || '');
  const [previewAvatar, setPreviewAvatar] = useState(user ? user.avatar : '');

  const handleAvatarChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Create a local preview URL for the selected image file
      const url = URL.createObjectURL(file);
      setPreviewAvatar(url);
    }
  };

  const handleSave = () => {
    // Save the API key and avatar changes to context
    setApiKey(tempKey);
    if (user) {
      setUser({ ...user, avatar: previewAvatar });
    }
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-30 flex items-center justify-center">
      {/* Modal content box */}
      <div className="bg-white dark:bg-gray-800 p-6 rounded shadow-xl w-80">
        <h2 className="text-lg font-bold mb-4 text-gray-800 dark:text-gray-100">Settings</h2>
        {/* API Key input */}
        <div className="mb-4">
          <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">
            OpenAI API Key:
          </label>
          <input 
            type="password"
            value={tempKey}
            onChange={e => setTempKey(e.target.value)}
            placeholder="sk-... (your API key)"
            className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded bg-gray-50 dark:bg-gray-700 
                       text-gray-800 dark:text-gray-100"
          />
        </div>
        {/* Avatar upload */}
        <div className="mb-4">
          <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">
            Avatar:
          </label>
          {previewAvatar && (
            <img 
              src={previewAvatar} 
              alt="Avatar preview" 
              className="w-12 h-12 rounded-full mb-2 object-cover" 
            />
          )}
          <input 
            type="file" 
            accept="image/*"
            onChange={handleAvatarChange}
            className="text-sm text-gray-700 dark:text-gray-300"
          />
        </div>
        {/* Action buttons */}
        <div className="text-right">
          <button 
            onClick={onClose} 
            className="mr-3 px-4 py-2 text-sm rounded bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600"
          >
            Cancel
          </button>
          <button 
            onClick={handleSave} 
            className="px-4 py-2 text-sm rounded bg-blue-600 text-white hover:bg-blue-700"
          >
            Save
          </button>
        </div>
      </div>
    </div>
  );
} 