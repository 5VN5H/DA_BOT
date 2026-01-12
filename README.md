<p align="center">
  <img src="b.png" alt="Data Structure Tutor Chatbot Banner" width="100%">
</p>

# DA_BOT - Data Structure Tutor

A modern web-based chatbot application that serves as an intelligent Data Structure tutor. Built with FastAPI backend and a clean, responsive frontend interface.

## Features

- 💬 **Interactive Chat Interface** - Modern, user-friendly chat UI with dark mode support
- 🤖 **AI-Powered Responses** - Powered by Meta's Llama 3 8B model via OpenRouter
- 🖼️ **Image Analysis** - Upload diagrams and get explanations using GPT-4o-mini vision
- 📝 **Context-Aware Conversations** - Maintains chat history for follow-up questions
- 🎨 **Responsive Design** - Clean, modern UI that works across devices

## File Structure

```
DA_BOT/
├── .env                    # Environment variables (API keys)
├── .git/                   # Git repository data
├── myenv/                  # Python virtual environment
├── main.py                 # FastAPI backend server
├── requirements.txt        # Python dependencies
├── index.html              # Main frontend HTML file
├── style.css               # Stylesheet for the UI
├── script.js               # Frontend JavaScript logic
├── bot.html                # Legacy HTML file (deprecated)
├── server.log              # Server logs
└── README.md               # This file
```

## Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **OpenAI SDK** - For interacting with AI models via OpenRouter
- **Python-dotenv** - Environment variable management
- **Uvicorn** - ASGI server for running FastAPI

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling with modern UI/UX
- **Vanilla JavaScript** - Interactive functionality

### AI Models
- **Meta Llama 3 8B Instruct** - For text-based conversations
- **GPT-4o-mini** - For image analysis and vision tasks

## Setup Instructions

### Prerequisites
- Python 3.8+
- OpenRouter API key (or OpenAI API key)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Chatbot
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv myenv
   source myenv/bin/activate  # On Windows: myenv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   # OR
   OPENAI_API_KEY=your_openai_api_key_here
   ```

### Running the Application

1. **Start the backend server**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Access the application**
   
   Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

   Or directly open the `index.html` file in your browser.

## API Endpoints

### `GET /`
- **Description**: Health check endpoint
- **Response**: `{"status": "Backend running"}`

### `POST /chat`
- **Description**: Send a text message to the chatbot
- **Request Body**:
  ```json
  {
    "user_id": "unique_user_id",
    "query": "Your question here"
  }
  ```
- **Response**:
  ```json
  {
    "reply": "AI response"
  }
  ```

### `POST /image-chat`
- **Description**: Upload an image for analysis
- **Request**: Form data with `user_id` and `image` file
- **Response**:
  ```json
  {
    "reply": "Image explanation"
  }
  ```

## Features in Detail

### Chat History Management
- Automatically maintains conversation context per user
- Limits history to last 4 exchanges to optimize token usage
- Separate history tracking for each user ID

### Error Handling
- Graceful error responses for API failures
- API key validation
- Image format detection and handling

### CORS Configuration
- Enabled for all origins (development mode)
- Supports all methods and headers

## Development Notes

- **bot.html**: Legacy file kept for reference, use `index.html` instead
- **Chat Context**: Limited to 8 messages (4 exchanges) to manage API costs
- **Models**: Text uses Llama 3 8B, vision uses GPT-4o-mini

## Future Enhancements

- [ ] User authentication and session management
- [ ] Database integration for persistent chat history
- [ ] Additional AI model options
- [ ] Export chat history feature
- [ ] Code syntax highlighting in responses
- [ ] Voice input/output support

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions, please open an issue in the repository.

---

**Note**: Make sure to keep your `.env` file secure and never commit it to version control. The `.env` file should be added to `.gitignore`.
