import { useNavigate } from 'react-router-dom';
import { apiDocs } from '../data/apiDocs';
import EndpointItem from './EndpointItem';

export default function DocsSidebar({ selectedApiId }) {
  const navigate = useNavigate();
  // Determine which APIs to display (all, or only the selected one)
  const apisToDisplay = selectedApiId
    ? apiDocs.filter(api => api.id === selectedApiId)
    : apiDocs;

  return (
    <aside className="h-full bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 p-4 overflow-y-auto md:w-80 w-full">
      {apisToDisplay.map(api => (
        <div key={api.id} className="mb-6">
          {/* API Title and Description */}
          <h2 className="text-xl font-bold text-gray-800 dark:text-gray-100 mb-1">{api.name}</h2>
          {api.description && (
            <p className="text-gray-600 dark:text-gray-400 text-sm mb-2">
              {api.description}
            </p>
          )}
          {/* List of Endpoints */}
          {api.endpoints.map((endpoint, idx) => (
            <EndpointItem key={idx} endpoint={endpoint} />
          ))}
          {/* Link to start a chat for this API (shown on docs page) */}
          {!selectedApiId && (
            <button 
              onClick={() => navigate(`/chat/${api.id}`)}
              className="mt-2 text-blue-600 dark:text-blue-400 text-sm underline"
            >
              Chat with {api.name}
            </button>
          )}
        </div>
      ))}
    </aside>
  );
} 