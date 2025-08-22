import os
from .config import GET_FILE_CONTENT_CHAR_LIMIT as max_chars

def get_file_content(working_directory, file_path) -> str:
    full_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not full_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        file_content: str = ""
        with open(full_path, "r") as f:
            file_content = f.read(max_chars)
        
        if len(file_content) == max_chars:
            file_content += f"...File {file_path} truncated at {max_chars} characters"
        
        return file_content

    except Exception as e:
        return f"Error: {e}"