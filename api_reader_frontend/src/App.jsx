import React, {useState} from 'react';
import dummyResponses from './assets/dummy_ai_responses.json'; // Import the JSON data
import './App.css';


function App() {
  const [conversation, setConversation] = useState([
    { question: `Hi, tell me about "Lorem Ipsum"?`, answer: "Lorem Ipsum is simply dummy text of the printing and typesetting industry." }
  ]);
  const [userInput, setUserInput] = useState('');

  // Function to handle user input submission
  const handleKeyDown = (event) => {
    if (event.key === 'Enter' && userInput.trim() !== '') {
      const randomAnswer = dummyResponses[Math.floor(Math.random() * dummyResponses.length)];
      setConversation([...conversation, { question: userInput, answer: randomAnswer.answer }]);
      setUserInput(''); // Clear the input field
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        {/* Left side: Logo */}
        <div className="header-left">
          {/* You could also use an <img> tag for an actual image logo: */}
          {/* <img src="path/to/logo.png" alt="Logo" className="logo" /> */}
          <h2>API Explorer</h2>
        </div>

        {/* Right side: Username & User Icon */}
        <div className="header-right">
          <span className="username">Marwan Musa</span>
          {/* Replace path/to/user_icon.png with your actual icon path */}
          <img
            src="/src/assets/boy.png"
            alt="User Icon"
            className="user-icon"
          />
        </div>
      </header>

      {/* MAIN LAYOUT */}
      <div className="main-layout">
        {/* LEFT COLUMN: Chat History */}
        <div className="left-sidebar">
          {/* TOP INPUTS */}
          <div className="api-url-input">
            <p>Api url...</p>
          </div>
          <div className="api-explanation-input">
            <p>Api explanation...</p>
          </div>
          <div className="sidebar-header">
            <div className='left-sidebar-header'>
              <h3>Chat History</h3>
            </div>
            <div className='right-sidebar-header'>
              <img
                src="/src/assets/telegram.png"
                alt="Chat Icon"
                className="chat-icon"
              />
            </div>
          </div>
          <div></div>
          {/* ... you can list past conversations here ... */}
          <div className='list-conversation'>
            <div className='conversation-section'>
              <div className='time-tracker'>
                <p>Today</p>
              </div>
              <div className='conversations'>
                <p>Lorem Ipsum</p>
                <p>Astronaut and moon</p>
                <p>Mars is red</p>
                <p>Moon is gray</p>
              </div>
            </div>
            <div className='conversation-section'>
              <div className='time-tracker'>
                <p>Previous 7 days</p>
              </div>
              <div className='conversations'>
                <p>Amazing PC</p>
                <p>Smart grid</p>
                <p>Minihydro plant</p>
                <p>Biak and the river</p>
              </div>
            </div>
          </div>
        </div>

        {/* RIGHT COLUMN: Main Content */}
        <div className="main-content">
          {/* CHAT CONTAINER */}
          <div className="chat-container">
            {conversation.map((entry, index) => (
              <div key={index}>
                <div className="user-question-header">
                  <p className='user-questions'>{entry.question}</p>
                </div>
                <div className="assistant-answer">
                  <img src="/src/assets/ai.png" alt="AI Icon" className="ai-icon" />
                  <p className='ai-answers'>{entry.answer}</p>
                </div>
              </div>
            ))}
          </div>

          {/* BOTTOM CHAT INPUT */}
          <div className="chat-input">
            <input
              placeholder="Enter to submit"
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              onKeyDown={handleKeyDown} // Listen for Enter key press
            />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;

