import os

def write_file(working_dir: str, file_path: str, content: str):
	full_path = os.path.abspath(os.path.join(working_dir, file_path))

	if not full_path.startswith(os.path.abspath(working_dir)):
		return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
	
	try:
		if not os.path.exists(full_path):
			os.makedirs(os.path.dirname(full_path), exist_ok=True)
		
		with open(full_path, "w") as file:
			file.write(content)

		return f'Successfully wrote to "{full_path}" ({len(content)} characters written)'

	except Exception as e:
		return f"Error: {e}"