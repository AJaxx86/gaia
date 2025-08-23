from functions.run_python import run_python_file

print(f'Test 1:\n{run_python_file("calculator", "main.py")}')
print(f'Test 2:\n{run_python_file("calculator", "main.py", ["3 + 5"])}')
print(f'Test 3:\n{run_python_file("calculator", "tests.py")}')
print(f'Test 4:\n{run_python_file("calculator", "../main.py")}')
print(f'Test 4:\n{run_python_file("calculator", "nonexistent.py")}')