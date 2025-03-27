import { useState } from 'react';

export default function EndpointItem({ endpoint }) {
  const [open, setOpen] = useState(false);
  // Color coding for HTTP methods
  const methodColors = {
    GET: 'bg-green-100 text-green-800 dark:bg-green-200 dark:text-green-900',
    POST: 'bg-blue-100 text-blue-800 dark:bg-blue-200 dark:text-blue-900',
    PUT: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-200 dark:text-yellow-900',
    DELETE: 'bg-red-100 text-red-800 dark:bg-red-200 dark:text-red-900'
  };

  return (
    <div className="mb-2">
      {/* Endpoint header row */}
      <div 
        className="flex justify-between items-center cursor-pointer px-2 py-1 bg-gray-100 dark:bg-gray-800 rounded"
        onClick={() => setOpen(!open)}
      >
        <div>
          <span className={`text-xs font-bold px-2 py-1 rounded ${methodColors[endpoint.method]}`}>
            {endpoint.method}
          </span>
          <span className="ml-2 font-mono text-sm text-gray-800 dark:text-gray-100">
            {endpoint.path}
          </span>
        </div>
        <span className="text-xl text-gray-600 dark:text-gray-400">{open ? '−' : '+'}</span>
      </div>
      {/* Expanded details section */}
      {open && (
        <div className="mt-1 ml-4 p-2 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded text-sm">
          {endpoint.description && <p className="mb-2">{endpoint.description}</p>}
          {endpoint.parameters && endpoint.parameters.length > 0 && (
            <div className="mb-2">
              <strong>Parameters:</strong>
              <ul className="list-disc list-inside">
                {endpoint.parameters.map((param, i) => (
                  <li key={i}>
                    <span className="font-mono font-semibold">{param.name}</span>{" "}
                    <em>({param.type})</em> – {param.description}
                  </li>
                ))}
              </ul>
            </div>
          )}
          {endpoint.exampleResponse && (
            <div>
              <strong>Example Response:</strong>
              <pre className="mt-1 p-2 bg-gray-100 dark:bg-gray-900 rounded overflow-x-auto text-xs">
                {JSON.stringify(endpoint.exampleResponse, null, 2)}
              </pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
} 