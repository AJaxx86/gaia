import os
import sys
from dotenv import load_dotenv
from google import genai
from functions import schemas
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file
from google.genai import types

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request,  make a function call plan and immediately execute it. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

tests.py files never have arguments when running them.
"""

available_functions = types.Tool(
	function_declarations=[
		schemas.schema_get_files_info,
		schemas.schema_get_file_content,
		schemas.schema_write_file,
		schemas.schema_run_python_file,
	]
)

if len(sys.argv) < 2:
	print("Error: prompt not provided. Exiting GAIA...")
	exit(1)

load_dotenv()
api_key: str = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
user_prompt = sys.argv[1]
verbose = "--verbose" in sys.argv
messages = [
	types.Content(role="user", parts=[types.Part(text=user_prompt)])
]


def main():
	response = client.models.generate_content(
		model="gemini-2.0-flash-001",
		contents=messages,
		config=types.GenerateContentConfig(
			system_instruction=system_prompt,
			tools=[available_functions]
		)
	)

	print(f"User prompt: {user_prompt}")

	if response.function_calls:
		for function_call_part in response.function_calls:
			function_result = call_function(function_call_part, verbose)
			function_response = function_result.parts[0].function_response.response

			if not function_response:
				raise Exception(f"Function {function_call_part.name} returned no response")
			else:
				print(f"-> {function_response.get('result')}")

	print(f"Response: {'Called functions' if not response.text else response.text}")

	if verbose:
		prompt_tokens: int = response.usage_metadata.prompt_token_count
		response_tokens: int = response.usage_metadata.candidates_token_count
		print(f"Prompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}")


def call_function(function_call: types.FunctionCall, verbose: bool = False):
	if verbose:
		print(f"Calling function: {function_call.name}({function_call.args})")
	else:
		print(f" - Calling function: {function_call.name}")
	
	working_dir = "./calculator"
	schema_dict = {
		"get_files_info": get_files_info,
		"get_file_content": get_file_content,
		"write_file": write_file,
		"run_python_file": run_python_file,
	}

	if function_call.name not in schema_dict:
		return types.Content(
			role="tool",
			parts=[
				types.Part.from_function_response(
					name=function_call.name,
					response={"error": f"Unknown function: {function_call.name}"},
				)
			],
		)

	function_result = schema_dict[function_call.name](working_dir, **function_call.args)
	return types.Content(
		role="tool",
		parts=[
			types.Part.from_function_response(
				name=function_call.name,
				response={"result": function_result},
			)
		],
	)

if __name__ == "__main__":
	main()
