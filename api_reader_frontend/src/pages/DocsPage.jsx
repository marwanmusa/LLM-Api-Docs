import { useState } from 'react';
import { apiDocs } from '../data/apiDocs';
import { Link } from 'react-router-dom';
import EndpointItem from '../components/EndpointItem';

export default function DocsPage() {
  const [selectedApi, setSelectedApi] = useState(null);
  
  // Function to display API details when clicked
  const handleApiSelect = (apiId) => {
    setSelectedApi(apiId);
  };
  
  // Get the selected API object
  const currentApi = selectedApi ? apiDocs.find(api => api.id === selectedApi) : null;
  
  return (
    <div className="flex flex-col h-full bg-white dark:bg-gray-800">
      {/* Navigation bar with API selection */}
      <div className="border-b border-gray-200 dark:border-gray-700 p-4 bg-white dark:bg-gray-800">
        <div className="flex flex-wrap gap-2">
          {apiDocs.map(api => (
            <button
              key={api.id}
              onClick={() => handleApiSelect(api.id)}
              className={`px-4 py-2 rounded-md text-sm font-medium ${
                selectedApi === api.id 
                  ? 'bg-blue-600 text-white' 
                  : 'bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 hover:bg-gray-300 dark:hover:bg-gray-600'
              }`}
            >
              {api.name}
            </button>
          ))}
        </div>
      </div>
      
      {/* Content area */}
      <div className="flex-1 overflow-auto p-6">
        {currentApi ? (
          <div>
            {/* API Header */}
            <div className="flex justify-between items-start mb-6">
              <div>
                <h1 className="text-2xl font-bold text-gray-800 dark:text-gray-100">{currentApi.name}</h1>
                <p className="text-sm text-gray-600 dark:text-gray-400 font-mono">{currentApi.baseUrl}</p>
                {currentApi.description && (
                  <p className="mt-2 text-gray-700 dark:text-gray-300">{currentApi.description}</p>
                )}
              </div>
              <Link 
                to={`/chat/${currentApi.id}`} 
                className="bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded text-sm"
              >
                Chat with this API
              </Link>
            </div>
            
            {/* Endpoints List */}
            <div className="space-y-4">
              <h2 className="text-xl font-semibold text-gray-800 dark:text-gray-100 mb-3">Endpoints</h2>
              {currentApi.endpoints.map((endpoint, idx) => (
                <EndpointItem key={idx} endpoint={endpoint} />
              ))}
            </div>
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              Select an API from above to view its documentation
            </p>
            <Link to="/" className="text-blue-600 dark:text-blue-400 hover:underline">
              Return to home page
            </Link>
          </div>
        )}
      </div>
    </div>
  );
} 