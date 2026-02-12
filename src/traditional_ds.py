import pandas as pd
import numpy as np
import json
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from prophet import Prophet
import plotly.express as px
import plotly.graph_objects as go
import os

class TraditionalAnalyzer:
    def __init__(self, data_path="data/raw_data.json"):
        self.data_path = data_path
        self.repos_df = None
        self.commits_df = None
        self.profile_data = {}

    def load_data(self):
        if not os.path.exists(self.data_path):
            print(f"Data file not found at {self.data_path}")
            return False

        with open(self.data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.profile_data = data.get("profile", {})
        repos = data.get("repositories", [])

        # Process Repositories
        repo_list = []
        all_commits = []

        for item in repos:
            repo_meta = item.get("metadata", {})
            repo_details = item.get("details", {})
            
            repo_list.append({
                "name": repo_meta.get("name"),
                "stars": repo_meta.get("stargazers_count", 0),
                "forks": repo_meta.get("forks_count", 0),
                "language": repo_meta.get("language", "Unknown"),
                "size": repo_meta.get("size", 0),
                "created_at": pd.to_datetime(repo_meta.get("created_at"), errors='coerce'),
                "updated_at": pd.to_datetime(repo_meta.get("updated_at"), errors='coerce'),
                "topics": repo_meta.get("topics", []),
                "readme_length": len(repo_details.get("readme", "")),
                "readme_content": repo_details.get("readme", "")
            })

            # Process Commits
            commits = repo_details.get("recent_commits", [])
            if commits:
                for commit in commits:
                    c_meta = commit.get("commit", {})
                    author_date = c_meta.get("author", {}).get("date")
                    if author_date:
                        all_commits.append({
                            "repo_name": repo_meta.get("name"),
                            "date": pd.to_datetime(author_date),
                            "message": c_meta.get("message"),
                            "author": c_meta.get("author", {}).get("name")
                        })

        self.repos_df = pd.DataFrame(repo_list)
        self.commits_df = pd.DataFrame(all_commits)
        print("Data loaded successfully.")
        return True

    def get_basic_stats(self):
        if self.repos_df is None: return {}
        return {
            "total_repos": len(self.repos_df),
            "total_stars": self.repos_df['stars'].sum(),
            "top_languages": self.repos_df['language'].value_counts().to_dict(),
            "total_commits_tracked": len(self.commits_df) if self.commits_df is not None else 0
        }

    def perform_clustering(self, n_clusters=3):
        if self.repos_df is None or self.repos_df.empty:
            return None
        
        # Features for clustering: stars, forks, size, readme_length
        features = self.repos_df[['stars', 'forks', 'size', 'readme_length']].fillna(0)
        
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features)
        
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(scaled_features)
        
        self.repos_df['cluster'] = clusters
        return self.repos_df[['name', 'cluster', 'stars', 'forks']]

    def forecast_activity(self):
        if self.commits_df is None or self.commits_df.empty:
            return None

        # Prepare data for Prophet
        daily_counts = self.commits_df.set_index('date').resample('D').size().reset_index()
        daily_counts.columns = ['ds', 'y']
        
        # Prophet requires timezone-naive datetime
        daily_counts['ds'] = pd.to_datetime(daily_counts['ds']).dt.tz_localize(None)
        
        # Prophet requires at least 2 rows
        if len(daily_counts) < 2:
            return None

        m = Prophet(yearly_seasonality=True)
        m.fit(daily_counts)
        
        future = m.make_future_dataframe(periods=90) # Forecast 3 months
        forecast = m.predict(future)
        
        return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

if __name__ == "__main__":
    analyzer = TraditionalAnalyzer()
    if analyzer.load_data():
        print(analyzer.get_basic_stats())
        print(analyzer.perform_clustering())
