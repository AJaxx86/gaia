from functions.get_file_content import get_file_content

print(f"Results for 'main.py':\n{get_file_content("calculator", "main.py")}")
print(f"Results for 'pkg/calculator.py':\n{get_file_content("calculator", "pkg/calculator.py")}")
print(f"Results for '/bin/cat':\n{get_file_content("calculator", "/bin/cat")}")
print(f"Results for 'pkg/does_not_exist.py':\n{get_file_content("calculator", "pkg/does_not_exist.py")}")