import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys

# Add parent dir to path to import src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_collection import GitHubFetcher
from src.llm_analysis import OllamaAnalyzer
from src.traditional_ds import TraditionalAnalyzer

st.set_page_config(page_title="AI-GitHub Dashboard", layout="wide")

st.title("🤖 AI-Powered GitHub Self-Analysis Dashboard")

# Sidebar for Configuration
st.sidebar.header("Configuration")
username = st.sidebar.text_input("GitHub Username", value=os.getenv("GITHUB_USERNAME", ""))
token = st.sidebar.text_input("GitHub Token (Optional)", value=os.getenv("GITHUB_TOKEN", ""), type="password")

if st.sidebar.button("Fetch Data"):
    with st.spinner("Fetching data from GitHub..."):
        fetcher = GitHubFetcher(username=username, token=token)
        data = fetcher.fetch_all_data()
        if data:
            fetcher.save_data(data)
            st.sidebar.success("Data fetched successfully!")
        else:
            st.sidebar.error("Failed to fetch data.")



if not username:
    st.info("Please enter a GitHub username to get started.")
    st.stop()

try:
    # Load Data
    analyzer = TraditionalAnalyzer()
    data_loaded = analyzer.load_data()
    
    # Check if data corresponds to the current user
    if data_loaded:
        loaded_user = analyzer.profile_data.get('login', '').lower()
        if loaded_user != username.lower():
            st.warning(f"Cached data belongs to '{loaded_user}'. Please click 'Fetch Data' to update for '{username}'.")
            st.stop()
    
    if not data_loaded:
        st.warning("No data found. Please fetch data using the sidebar.")
        st.stop()

    stats = analyzer.get_basic_stats()

    # Overview Section
    st.header("📊 Overview")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Repositories", stats.get("total_repos", 0))
    c2.metric("Total Stars", stats.get("total_stars", 0))
    c3.metric("Commits Tracked", stats.get("total_commits_tracked", 0))

    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Repositories & Clustering", "Language Breakdown", "LLM Insights", "Forecasting", "Model Comparison"])

    with tab1:
        st.subheader("Repository Clustering")
        if analyzer.repos_df is not None and not analyzer.repos_df.empty:
            clustered_df = analyzer.perform_clustering()
            if clustered_df is not None and not clustered_df.empty:
                fig = px.scatter(clustered_df, x="stars", y="forks", color="cluster", hover_data=["name"], title="Repository Clusters (Stars vs Forks)")
                st.plotly_chart(fig, use_container_width=True)
                st.dataframe(clustered_df)
            else:
                st.info("Not enough data for clustering.")
        else:
            st.info("No repository data available.")

    with tab2:
        st.subheader("Language Distribution")
        langs = stats.get("top_languages", {})
        if langs:
            fig = px.pie(values=list(langs.values()), names=list(langs.keys()), title="Top Languages")
            st.plotly_chart(fig)
        else:
            st.info("No language data available.")

    with tab3:
        st.subheader("🤖 LLM Analysis (Ollama)")
        ollama_model = st.selectbox("Select Model", ["llama3.1", "mistral"])
        llm = OllamaAnalyzer(model_name=ollama_model)

        if st.button("Analyze Recent Commit Sentiment"):
            if analyzer.commits_df is not None and not analyzer.commits_df.empty:
                sample_commit = analyzer.commits_df.iloc[0]['message']
                st.write(f"**Sample Commit:** {sample_commit}")
                with st.spinner("Analyzing..."):
                    sentiment = llm.analyze_sentiment(sample_commit)
                    st.write(f"**Sentiment:** {sentiment}")
            else:
                st.info("No commits to analyze.")

        st.markdown("### Skill Extraction")
        if analyzer.repos_df is not None and not analyzer.repos_df.empty:
            repo_names = analyzer.repos_df['name'].tolist()
            selected_repo = st.selectbox("Select Repository to Analyze", repo_names)
            
            if st.button("Extract Skills"):
                repo_data = analyzer.repos_df[analyzer.repos_df['name'] == selected_repo].iloc[0]
                readme_text = repo_data.get('readme_content', "")
                
                if readme_text:
                    with st.spinner(f"Extracting skills from {selected_repo}..."):
                        skills = llm.extract_skills(readme_text)
                        st.success("Skills Extracted!")
                        st.write(skills)
                else:
                    st.warning("No README found for this repository.")
        else:
            st.info("No repository data available.")

    with tab4:
        st.subheader("📈 Activity Forecasting")
        if st.button("Generate Forecast"):
            with st.spinner("Forecasting..."):
                try:
                    forecast = analyzer.forecast_activity()
                    if forecast is not None:
                        fig = px.line(forecast, x='ds', y='yhat', title="Predicted Commit Activity")
                        # Add confidence intervals
                        fig.add_scatter(x=forecast['ds'], y=forecast['yhat_lower'], mode='lines', line=dict(width=0), showlegend=False)
                        fig.add_scatter(x=forecast['ds'], y=forecast['yhat_upper'], fill='tonexty', mode='lines', line=dict(width=0), showlegend=False)
                        st.plotly_chart(fig)
                    else:
                        st.warning("Not enough data to forecast (need at least 2 days of commits).")
                except Exception as e:
                    st.error(f"Forecasting error: {e}")

    with tab5:
        st.subheader("⚔️ Model Comparison")
        prompt = st.text_area("Test Prompt", "Summarize the coding style based on these commits...")
        if st.button("Compare Llama 3.1 vs Mistral"):
            with st.spinner("Running comparison..."):
                results = llm.compare_models(prompt)
                for model_name, metrics in results.items():
                    st.write(f"### {model_name}")
                    if "error" in metrics:
                       st.error(metrics["error"])
                    else:
                       st.write(f"**Time:** {metrics['time']:.2f}s")
                       st.write(f"**Response:** {metrics['response']}")
                       st.divider()

except Exception as e:
    st.error(f"An error occurred: {e}")
    import traceback
    st.text(traceback.format_exc())

