
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
import ollama
import os
import json
import argparse
from dotenv import load_dotenv
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from prophet import Prophet

# Local imports
# Assuming src module is in the python path or same directory
try:
    from src.data_collection import GitHubFetcher
    from src.llm_analysis import OllamaAnalyzer
except ImportError:
    st.error("Could not import local modules. Make sure 'src' directory exists and contains data_collection.py and llm_analysis.py")

# Load environment variables
load_dotenv()

st.title("Data Science Dashboard")
st.write("Environment setup complete. All libraries imported successfully.")
