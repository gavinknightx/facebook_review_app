# Facebook Reviews Analyzer
A comprehensive tool for analyzing Facebook business profile reviews using AI-powered sentiment analysis and natural language processing. This project helps businesses understand customer feedback through automated analysis of their Facebook reviews.

## 📁 Project Structure
```
.
├── api
│   ├── analyze.py
│   ├── api.py
│   ├── config
│   │   ├── **init**.py
│   │   ├── llm_config.py
│   │   ├── prompts.py
│   │   └── tokens.json
│   ├── data
│   │   └── reviews.json
│   ├── fb_reviews.py
│   └── **init**.py
├── app
│   └── app.py
└── requirements.txt
```

## 🛠️ Installation

### Prerequisites
- [Docker Engine](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/gavinknightx/facebook_review_app.git
   cd facebook_review_app
   ```

2. Add your OpenAI API key to `.env` file in the root directory:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

3. Start the application using Docker Compose:
   ```bash
   docker-compose up --build
   ```

## 🚦 Running the Application
The application will start automatically after running docker-compose. You can access:
- FastAPI backend at `http://localhost:8000`
- Streamlit frontend will open automatically in your default browser

## 📱 How to Use
1. Navigate to the web interface that opens in your browser after starting the Streamlit frontend.

2. You can analyze reviews for supported companies by typing phrases like:
   ```
   "Analyze reviews for Dialog"
   ```

3. Currently supported companies:
   - Dialog
   - SLT
   - Elephant House

## 🔧 Configuration
- Configure LLM settings in `api/config/llm_config.py`
- Adjust prompts in `api/config/prompts.py`
- Update token configurations in `api/config/tokens.json`
