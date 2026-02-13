import ollama
import os
from dotenv import load_dotenv
import time

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

class OllamaAnalyzer:
    def __init__(self, model_name="llama3.1"):
        self.client = ollama.Client(host=OLLAMA_HOST)
        self.model = model_name

    def analyze_sentiment(self, text):
        prompt = f"Analyze the sentiment of the following commit message. Return only 'Positive', 'Neutral', or 'Negative'.\n\nCommit Message: {text}"
        try:
            response = self.client.chat(model=self.model, messages=[
                {'role': 'user', 'content': prompt}
            ])
            return response['message']['content'].strip()
        except Exception as e:
            print(f"Error in sentiment analysis: {e}")
            return "Error"

    def extract_skills(self, readme_content):
        prompt = f"Extract a list of technical skills, languages, and frameworks mentioned in the following README content. Return them as a comma-separated list.\n\nREADME:\n{readme_content[:2000]}" # Limit context
        try:
            response = self.client.chat(model=self.model, messages=[
                {'role': 'user', 'content': prompt}
            ])
            return response['message']['content'].strip()
        except Exception as e:
            print(f"Error in skill extraction: {e}")
            if "connection" in str(e).lower() or "refused" in str(e).lower():
                return "Error: Ollama is not running. Please start it."
            return f"Error: {str(e)}"

    def classify_topic(self, repo_description):
        prompt = f"Classify the following repository description into one of these topics: 'Web Development', 'Data Science', 'Machine Learning', 'Mobile App', 'DevOps', 'Other'. Return only the topic name.\n\nDescription: {repo_description}"
        try:
            response = self.client.chat(model=self.model, messages=[
                {'role': 'user', 'content': prompt}
            ])
            return response['message']['content'].strip()
        except Exception as e:
            print(f"Error in topic classification: {e}")
            return "Other"

    def compare_models(self, task_prompt, models=["llama3.1", "mistral"]):
        results = {}
        for model in models:
            start_time = time.time()
            try:
                response = self.client.chat(model=model, messages=[
                    {'role': 'user', 'content': task_prompt}
                ])
                duration = time.time() - start_time
                results[model] = {
                    "response": response['message']['content'],
                    "time": duration
                }
            except Exception as e:
                results[model] = {"error": str(e)}
        return results

    def generate_user_title(self, stats):
        prompt = f"""Based on the following GitHub stats, generate a creative, fun, RPG-style user title (max 5 words).
        Return ONLY the title.
        Stats:
        - Top Language: {stats.get('top_language')}
        - Longest Streak: {stats.get('longest_streak')} days
        - Most Productive Day: {stats.get('most_productive_day')}
        """
        try:
            response = self.client.chat(model=self.model, messages=[
                {'role': 'user', 'content': prompt}
            ])
            return response['message']['content'].strip().replace('"', '')
        except Exception as e:
            print(f"Error generating title: {e}")
            return "The GitHub Wanderer"

    def analyze_readme_quality(self, readme_content):
        prompt = f"""Analyze the quality of this README file.
        Provide a checklist of 3-5 improvements. Focus on missing standard sections (Installation, Usage, Contributing, License).
        Keep it concise and actionable.
        README Content (first 2000 chars):
        {readme_content[:2000]}
        """
        try:
            response = self.client.chat(model=self.model, messages=[
                {'role': 'user', 'content': prompt}
            ])
            return response['message']['content'].strip()
        except Exception as e:
            print(f"Error analyzing README: {e}")
            if "connection" in str(e).lower() or "refused" in str(e).lower():
                return "Error: Ollama is not running. Please start it."
            return f"Error: {str(e)}"


if __name__ == "__main__":
    analyzer = OllamaAnalyzer()
    print("Testing connection...")
    try:
        print(analyzer.analyze_sentiment("Initial commit - added core features"))
    except Exception as e:
        print(f"Ollama connection failed: {e}")
