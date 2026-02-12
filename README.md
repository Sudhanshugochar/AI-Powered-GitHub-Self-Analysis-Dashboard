# AI-Powered GitHub Self-Analysis Dashboard

## 🚀 Overview
An interactive dashboard that analyzes your GitHub profile using local LLMs (Ollama) and traditional data science techniques. Get insights into your coding habits, sentiment, skills, and future activity.

## ✨ Features
- **Data Collection**: Fetches repositories, commits, and READMEs via GitHub API.
- **LLM Analysis**: Uses local Llama 3.1 & Mistral models for:
    - Sentiment Analysis of commit messages.
    - Skill Extraction from READMEs.
    - Code Quality Reviews.
- **Traditional Data Science**:
    - Clustering of repositories based on stars, forks, and size.
    - Time-series forecasting of commit activity (Prophet).
- **Interactive Dashboard**: Streamlit-based UI with Plotly visualizations.
- **Model Comparison**: Benchmark different local LLMs.

## 🛠 Prerequisites
- **Python 3.10+**
- **Ollama** installed and running.
    - Pull models: `ollama pull llama3.1`, `ollama pull mistral`
- **Git**

## 📦 Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd ai-github-dashboard
    ```

2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment**:
    - Copy `.env.example` to `.env` (optional, can also input in UI).
    - Set `GITHUB_TOKEN` and `GITHUB_USERNAME`.

## 🏃‍♂️ Usage

1.  **Start Ollama**:
    Ensure Ollama is running in the background (`ollama serve`).

2.  **Run the Dashboard**:
    ```bash
    streamlit run app/dashboard.py
    ```

3.  **Explore**:
    - Enter your GitHub username and token (if not in `.env`).
    - Click "Fetch Data".
    - Navigate tabs for insights.

## 📂 Project Structure
- `app/`: Streamlit dashboard application.
- `src/`: Core logic modules.
    - `data_collection.py`: GitHub API fetcher.
    - `llm_analysis.py`: Ollama integration.
    - `traditional_ds.py`: Clustering and forecasting.
- `data/`: Stores fetched JSON data.
- `notebooks/`: EDA notebooks.
- `tests/`: Unit tests.

## 🤝 Contributing
Contributions used to be welcome!

## 📄 License
MIT
