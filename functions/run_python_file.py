import os
import subprocess

def run_python_file(working_dir: str, file_path: str, args: list[str]=[]):
    full_path = os.path.abspath(os.path.join(working_dir, file_path))

    if not full_path.startswith(os.path.abspath(working_dir)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'
    if not full_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        result = subprocess.run(['python', full_path, *args], capture_output=True, text=True, timeout=30)
        if not result.stdout and not result.stderr:
            return f'No output produced.'
        
        return_text = f"STDOUT:\n{'N/A' if not result.stdout else result.stdout}\nSTDERR:\n{'N/A' if not result.stderr else result.stderr}"
        if result.returncode != 0:
            return_text += f'Process exited with code {result.returncode}'

        return return_text

    except Exception as e:
        return f'Error: executing Python file: {str(e)}'