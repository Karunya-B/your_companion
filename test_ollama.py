import requests
import sys
import os

# Add the project directory to sys.path
project_root = r"c:\Users\karun\OneDrive\Documents\karunya_companion"
sys.path.append(project_root)

def test_ollama_connection():
    print("Checking Ollama connection...")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [m["name"] for m in models]
            print(f"Ollama is running. Available models: {model_names}")
            if "mistral" in [m.split(":")[0] for m in model_names]:
                print("SUCCESS: 'mistral' model found.")
            else:
                print("WARNING: 'mistral' model NOT found. Please run 'ollama pull mistral'.")
        else:
            print(f"FAILED: Ollama returned status {response.status_code}")
    except Exception as e:
        print(f"FAILED: Could not connect to Ollama. Is it running? Error: {e}")

if __name__ == "__main__":
    test_ollama_connection()
