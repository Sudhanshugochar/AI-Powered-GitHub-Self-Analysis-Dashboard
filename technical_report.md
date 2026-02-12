# Technical Report: AI-Powered GitHub Self-Analysis Dashboard

## 1. Executive Summary
This project aims to provide a comprehensive analysis of a developer's GitHub activity using a hybrid approach of traditional data science and modern Large Language Models (LLMs). By leveraging local instances of Llama 3.1 and Mistral via Ollama, the dashboard offers privacy-preserving, cost-effective, and deep insights into coding style, sentiment, and skill progression, complemented by statistical forecasting and clustering.

## 2. Architecture Overview
The system is built on a modular architecture:

- **Data Layer**:
  - Source: GitHub REST API.
  - Storage: Local JSON files (`data/raw_data.json`).
  - Privacy: No data leaves the local machine (except for GitHub API requests).

- **Analysis Layer**:
  - **Traditional DS (`src/traditional_ds.py`)**: Uses `scikit-learn` for KMeans clustering of repositories based on metadata (stars, forks, size) and `Prophet` for time-series forecasting of commit activity.
  - **LLM/AI (`src/llm_analysis.py`)**: Integrates with `Ollama` to run quantized, local LLMs. It performs sentiment analysis on commit messages, topic classification, and skill extraction from READMEs.

- **Presentation Layer**:
  - **Streamlit Dashboard (`app/dashboard.py`)**: A reactive web interface using `Plotly` for interactive visualizations. It allows real-time data fetching and analysis triggering.

## 3. Methodology

### 3.1 Data Collection
Data is fetched using a custom `GitHubFetcher` class. It retrieves:
- User profile metadata.
- Repository repositories (including stars, forks, languages).
- Commit history (messages, dates).
- README content (decoded from Base64).

### 3.2 Machine Learning & Statistics
- **Clustering**: K-Means algorithm groups repositories into clusters (e.g., "Popular & Large", "Small & Niche") to identify project types. Features used: Stars, Forks, Size, README length.
- **Forecasting**: Facebook's Prophet model decomposes time-series data to predict future commit frequency, accounting for daily/weekly seasonality.

### 3.3 Large Language Models
- **Models**: Llama 3.1 (8B) and Mistral (7B) are used for their balance of performance and resource efficiency.
- **Tasks**:
  - *Sentiment Analysis*: Classifying commit messages to gauge project mood.
  - *Skill Extraction*: NER-like extraction from README text.
  - *Code Review*: (Planned) Summarizing code quality.
- **Benchmarking**: A dedicated script (`run_benchmark.py`) compares model response times and quality for specific tasks.

## 4. Challenges & Solutions
- **Rate Limits**: GitHub API has strict rate limits. **Solution**: Implemented authentication (PAT) support and pagination handling.
- **LLM Latency**: Local inference can be slow on CPU. **Solution**: Used smaller quantized models and asynchronous UI updates in Streamlit to prevent freezing (spinners).
- **Data Noise**: READMEs vary wildly in format. **Solution**: Truncated input context for LLMs to focus on the top 2000 characters where key info usually resides.

## 5. Future Improvements
- **RAG Integration**: Use RAG to query across all codebases for "How did I solve X?".
- **Advanced Code Analysis**: Static analysis tools (AST) combined with LLM for deeper code quality metrics.
- **Cloud Deployment**: Containerize with Docker for easy deployment (though local LLM requirement makes this complex).

## 6. Conclusion
This project demonstrates the power of combining deterministic code analysis with the semantic understanding of LLMs, resulting in a holistic developer portfolio tool.
