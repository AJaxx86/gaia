import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


if len(sys.argv) < 2:
	print("Error: prompt not provided. Exiting GAIA...")
	exit(1)

load_dotenv()
api_key: str = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
user_prompt = sys.argv[1]
messages = [
	types.Content(role="user", parts=[types.Part(text=user_prompt)])
]


def main():
	response = client.models.generate_content(
		model="gemini-2.0-flash-001",
		contents=messages
	)
	prompt_tokens: int = response.usage_metadata.prompt_token_count
	completion_tokens: int = response.usage_metadata.candidates_token_count

	print(f"{response.text}\nPrompt tokens: {prompt_tokens}\nResponse tokens: {completion_tokens}")



if __name__ == "__main__":
	main()
