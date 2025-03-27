import DocsSidebar from '../components/DocsSidebar';

export default function ApiDocsPage() {
  return (
    <div className="flex flex-col md:flex-row h-full bg-gray-50 dark:bg-gray-900">
      <DocsSidebar />
      {/* Right side: prompt or placeholder */}
      <div className="flex-1 flex items-center justify-center p-4 bg-white dark:bg-gray-800">
        <p className="text-gray-600 dark:text-gray-400 text-center">
          Select an API from the left to view documentation or start a chat.
        </p>
      </div>
    </div>
  );
} 