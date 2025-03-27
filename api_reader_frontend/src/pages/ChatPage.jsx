import { useState } from 'react';
import { useParams } from 'react-router-dom';
import { apiDocs } from '../data/apiDocs';
import DocsSidebar from '../components/DocsSidebar';
import ChatMessage from '../components/ChatMessage';
import ChatInput from '../components/ChatInput';

export default function ChatPage() {
  const { apiId } = useParams();
  // Find the selected API details from the data
  const api = apiDocs.find(api => api.id === apiId);

  // Chat messages state (array of { role: 'user'|'assistant', content: string })
  const [messages, setMessages] = useState([
    { role: 'assistant', content: `You are now chatting with the ${api.name}. How can I assist you?` }
  ]);

  // Simulate streaming a response from the assistant
  const streamAssistantResponse = (userPrompt) => {
    const fakeResponse = `You asked about "${userPrompt}". This is a dummy response about the API.`;
    // Add an empty assistant message to start filling in
    setMessages(prev => [...prev, { role: 'assistant', content: '' }]);
    let index = 0;
    const interval = setInterval(() => {
      setMessages(prev => {
        // Append one character to the last message's content
        const updated = [...prev];
        updated[updated.length - 1] = {
          ...updated[updated.length - 1],
          content: updated[updated.length - 1].content + fakeResponse[index]
        };
        return updated;
      });
      index++;
      if (index >= fakeResponse.length) {
        clearInterval(interval);
      }
    }, 50);
  };

  // Handle sending a new user message
  const handleSendMessage = (text) => {
    // Append user message to chat
    setMessages(prev => [...prev, { role: 'user', content: text }]);
    // Call the assistant response streamer
    streamAssistantResponse(text);
  };

  return (
    <div className="flex flex-col md:flex-row h-full bg-gray-50 dark:bg-gray-900">
      <DocsSidebar selectedApiId={apiId} />
      {/* Right side: Chat interface */}
      <div className="flex flex-col flex-1">
        {/* Top section: API info */}
        <div className="px-4 py-2 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
          <h2 className="text-gray-800 dark:text-gray-100 font-semibold">{api.name}</h2>
          <p className="text-sm text-gray-600 dark:text-gray-400">{api.baseUrl}</p>
        </div>
        {/* Chat history (messages) */}
        <div className="flex-1 p-4 overflow-y-auto bg-white dark:bg-gray-800">
          {messages.map((msg, idx) => (
            <ChatMessage key={idx} message={msg} />
          ))}
        </div>
        {/* Input box */}
        <div className="px-4 py-3 border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-700">
          <ChatInput onSend={handleSendMessage} />
        </div>
      </div>
    </div>
  );
} 