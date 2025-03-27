export default function ChatMessage({ message }) {
  const isUser = message.role === 'user';
  return (
    <div className={`my-1 flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`px-4 py-2 rounded-lg text-sm break-words max-w-xl 
        ${isUser 
          ? 'bg-blue-600 text-white rounded-br-none' 
          : 'bg-gray-300 dark:bg-gray-700 text-gray-900 dark:text-gray-100 rounded-bl-none'
        }`}>
        {message.content}
      </div>
    </div>
  );
} 