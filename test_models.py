import os
import sys
from google import genai

def main():
    api_key = sys.argv[1] if len(sys.argv) > 1 else os.environ.get('GEMINI_API_KEY')
    if not api_key:
        print("Please provide API key")
        return
    client = genai.Client(api_key=api_key)
    for model in client.models.list():
        print(model.name)

if __name__ == '__main__':
    main()
