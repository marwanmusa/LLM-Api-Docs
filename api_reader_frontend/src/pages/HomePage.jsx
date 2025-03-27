import { Link } from 'react-router-dom';
import { apiDocs } from '../data/apiDocs';

export default function HomePage() {
  return (
    <div className="flex flex-col items-center justify-center p-8 bg-white dark:bg-gray-800 h-full">
      <h1 className="text-3xl font-bold mb-6 text-gray-800 dark:text-gray-100">Welcome to SwaggerChat</h1>
      <p className="text-gray-600 dark:text-gray-400 text-center max-w-xl mb-8">
        Explore API documentation or chat with our AI assistant about any of our available APIs.
      </p>
      
      <div className="grid md:grid-cols-2 gap-8 w-full max-w-4xl">
        {/* Documentation Card */}
        <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-6 shadow-md">
          <h2 className="text-xl font-semibold mb-3 text-gray-800 dark:text-gray-100">API Documentation</h2>
          <p className="text-gray-600 dark:text-gray-400 mb-4">
            Browse our API documentation in a Swagger-like interface.
          </p>
          <Link 
            to="/docs" 
            className="block w-full bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded text-center"
          >
            View Documentation
          </Link>
        </div>
        
        {/* Chat Card */}
        <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-6 shadow-md">
          <h2 className="text-xl font-semibold mb-3 text-gray-800 dark:text-gray-100">Chat with API</h2>
          <p className="text-gray-600 dark:text-gray-400 mb-4">
            Select an API to chat with our AI assistant about its usage.
          </p>
          <div className="space-y-2">
            {apiDocs.map(api => (
              <Link 
                key={api.id}
                to={`/chat/${api.id}`}
                className="block w-full bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded text-center mb-2"
              >
                Chat with {api.name}
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
} 