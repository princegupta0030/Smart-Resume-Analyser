import sys
from google import genai

def main():
    if len(sys.argv) < 2:
        print("Usage: python list_models.py <YOUR_API_KEY>")
        return
    api_key = sys.argv[1]

    print("Initializing client...")
    client = genai.Client(api_key=api_key)

    print("Fetching models...")
    try:
        models = client.models.list()
        print("Available models:")
        for m in models:
            print(f"- {m.name}")
    except Exception as e:
        print(f"Error fetching models: {e}")

if __name__ == '__main__':
    main()
