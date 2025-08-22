import os

def get_files_info(working_directory, directory=".") -> str:
	def format_info(info: tuple) -> str:
		return f"- {info[0]}: file_size={info[1]}, is_dir={info[2]}"
	
	full_path = os.path.abspath(os.path.join(working_directory, directory))
	
	if not full_path.startswith(os.path.abspath(working_directory)):
		return f'Error: cannot list "{directory}" as it is outside the permitted directory'
	if not os.path.isdir(full_path):
		return f'Error: "{directory}" is not a directory'
	
	try:
		file_names = os.listdir(full_path)
		file_details = list(map(lambda file: (file, os.path.getsize(os.path.join(full_path, file)), os.path.isdir(os.path.join(full_path, file))), file_names))
		
		return "\n".join(map(format_info, file_details))
	
	except Exception as e:
		return f"Error: {e}"