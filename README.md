# AI Tweet Generator

AI-powered tweet generator using LangGraph workflow with iterative optimization. Features multi-agent system with specialized LLMs for generation, evaluation, and optimization to create viral-worthy tweets with emojis and hashtags.

## Features

- 🤖 **Multi-Agent AI System** - Uses LangGraph with specialized LLMs for generation, evaluation, and optimization
- 🔄 **Iterative Refinement** - Automatically improves tweets through AI feedback loops
- ✨ **Smart Formatting** - Generates tweets with natural emojis and relevant hashtags
- 🎨 **Neubrutalism UI** - Clean black and white interface with bold design
- ⚡ **Real-time Generation** - Fast tweet creation with live feedback

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **LangGraph** - Agent workflow orchestration
- **LangChain** - LLM integration framework
- **Groq** - High-performance LLM API
- **Python 3.12+**

### Frontend
- **Vanilla JavaScript** - No framework dependencies
- **HTML5/CSS3** - Neubrutalism design system
- **Responsive Design** - Works on all devices

## Installation

### Prerequisites
- Python 3.12 or higher
- Groq API key ([Get one here](https://console.groq.com))

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/AI-Tweet-Generator.git
cd AI-Tweet-Generator
```

2. **Create virtual environment**
```bash
python -m venv .venv
```

3. **Activate virtual environment**
- Windows:
```bash
.venv\Scripts\activate
```
- macOS/Linux:
```bash
source .venv/bin/activate
```

4. **Install dependencies**
```bash
cd backend
pip install -r requirements.txt
```

5. **Configure environment variables**

Create a `.env` file in the `backend` directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```

## Usage

### Start the Backend Server

```bash
cd backend
python -m uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Start the Frontend Server

```bash
cd frontend
python -m http.server 5173
```

Open your browser and navigate to `http://localhost:5173`

### Generate a Tweet

1. Enter a topic in the input field (e.g., "working from home", "coffee addiction")
2. Click "Generate Tweet"
3. Wait for the AI to generate and optimize your tweet
4. View the final tweet with iteration history
5. Copy to clipboard and share!

## API Documentation

### Generate Tweet

**Endpoint:** `POST /api/generate-tweet`

**Request Body:**
```json
{
  "topic": "string",
  "max_iteration": 3
}
```

**Response:**
```json
{
  "final_tweet": "string",
  "evaluation": "approved",
  "total_iterations": 2,
  "history": [
    {
      "iteration": 1,
      "tweet": "string",
      "feedback": "string",
      "evaluation": "needs_improvement"
    }
  ],
  "topic": "string"
}
```

### Health Check

**Endpoint:** `GET /api/health`

**Response:**
```json
{
  "status": "healthy",
  "service": "Tweet Generator API"
}
```

## Project Structure

```
AI-Tweet-Generator/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── models.py            # Pydantic models
│   │   ├── routes/
│   │   │   └── tweets.py        # API endpoints
│   │   └── services/
│   │       └── tweet_generator.py  # LangGraph workflow
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── .gitignore
└── README.md
```

## How It Works

The tweet generation uses a LangGraph workflow with three stages:

1. **Generation** - Creates initial tweet using Llama 3.3 70B
2. **Evaluation** - Critiques the tweet for humor, originality, and virality
3. **Optimization** - Improves tweet based on feedback (if needed)

The process repeats up to 3 iterations until an approved tweet is generated.

## Configuration

### Max Iterations
The default maximum iterations is set to 3. Modify in the frontend code or API request.

### LLM Models
All stages use `llama-3.3-70b-versatile` for consistent quality. You can modify models in `backend/app/services/tweet_generator.py`.

### Temperature Settings
- Generator: 0.9 (creative)
- Evaluator: 0.3 (critical)
- Optimizer: 0.7 (balanced)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph)
- Powered by [Groq](https://groq.com)
- UI inspired by Neubrutalism design

---

Made with ❤️ using AI
