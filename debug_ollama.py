
import sys
import subprocess

print(f"Python executing: {sys.executable}")

try:
    import ollama
    print("SUCCESS: 'ollama' module imported.")
except ImportError:
    print("ERROR: 'ollama' module NOT found.")

try:
    import dotenv
    print("SUCCESS: 'python-dotenv' module imported.")
except ImportError:
    print("ERROR: 'python-dotenv' module NOT found.")

# Check if Ollama service is running
try:
    client = ollama.Client(host='http://localhost:11434')
    print("Attempting to list models...")
    models = client.list()
    print(f"SUCCESS: Ollama connected. Models: {models}")
except Exception as e:
    print(f"ERROR: Failed to connect to Ollama: {e}")

# Check CLI
try:
    result = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"SUCCESS: Ollama CLI found: {result.stdout.strip()}")
    else:
        print(f"WARNING: Ollama CLI found but returned error: {result.stderr}")
except FileNotFoundError:
    print("ERROR: Ollama CLI not found in PATH.")

