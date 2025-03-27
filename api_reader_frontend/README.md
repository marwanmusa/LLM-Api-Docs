# SwaggerChat

A modern web application that combines Swagger-style API documentation with a ChatGPT-like chat interface, built with React and Tailwind CSS.

## Features

- **Swagger-Inspired API Documentation**: Browse API endpoints with expandable details including parameters and example responses.
- **Interactive Chat Interface**: Interact with APIs through a ChatGPT-style interface with token-by-token streaming responses.
- **Responsive Design**: Fully responsive layout that works well on all device sizes.
- **Dark Mode Support**: Toggle between light and dark themes with a click.
- **User Management**: Simple account management with settings for API keys and avatar customization.

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd api_reader_frontend
```

2. Install dependencies
```bash
npm install
# or with yarn
yarn install
```

3. Start the development server
```bash
npm run dev
# or with yarn
yarn dev
```

4. Open your browser and navigate to the URL displayed in your terminal (typically http://localhost:5173/)

## Project Structure

- `src/components/`: Reusable UI components
- `src/context/`: React Context providers for state management
- `src/pages/`: Main application views
- `src/data/`: Static data for API documentation

## Technologies

- **React**: Frontend library for building user interfaces
- **React Router**: For navigation between views
- **Tailwind CSS**: For styling and responsive design
- **Vite**: Build tool and development server

## Customization

### Adding Your Own APIs

Edit the `src/data/apiDocs.js` file to add your own API documentation. Follow the existing structure for compatibility.

### Connecting to a Real Backend

The chat functionality currently uses simulated responses. To connect to a real backend:

1. Update the `streamAssistantResponse` function in `src/pages/ChatPage.jsx`
2. Implement API calls using fetch or your preferred HTTP client
3. Update the streaming mechanism to work with your backend's response format

## License

MIT

## Acknowledgments

- Inspired by Swagger UI and OpenAI's ChatGPT interface
- Built with React and Tailwind CSS
