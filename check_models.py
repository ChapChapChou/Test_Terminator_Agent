import os
from dotenv import load_dotenv
from openai import OpenAI

def main():
    load_dotenv()
    
    # Initialize the OpenAI client
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    # List available models
    models = client.models.list()
    for model in models:
        print(f"Model ID: {model.id}")
        print(f"Created: {model.created}")
        print(f"Owned by: {model.owned_by}")
        print("-" * 50)

if __name__ == "__main__":
    main() 