# Model Comparison Demo Frontend

This project is a React-based frontend application for comparing different language models' responses.

## Prerequisites

- Node.js (v14.0.0 or higher)
- npm (v6.0.0 or higher)

## Installation

1. Clone the repository:

git clone <your-repository-url>
cd demo-flask/demo-llm-frontend

2. Install the required dependencies:

npm install

## Usage


This will install all necessary dependencies including:
- @mui/material
- @emotion/react
- @emotion/styled
- axios
- react
- react-dom
- typescript

## Running the Application

1. Start the development server:

npm start

2. Open your browser and navigate to:

http://localhost:3000


## Backend Connection

The frontend is configured to connect to a Flask backend running on `http://127.0.0.1:5000`. Make sure the backend server is running before using the application.

## Features

- Dark theme UI using Material-UI
- Text input for prompts (up to 8000 characters)
- Parallel comparison of three different language models:
  - LLM-JP-172B
  - GPT-4o
  - Llama3-405B
- Real-time response display
- Loading states and error handling

## Development

- The application uses TypeScript for type safety
- Material-UI (MUI) for the component library
- Axios for API calls
- React for the UI framework

## Contributing

1. Fork the repository
2. Create a new branch for your changes
