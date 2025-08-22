from functions.write_file import write_file

print(f"Results for test1:\n{write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")}")
print(f"Results for test2:\n{write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")}")
print(f"Results for test3:\n{write_file("calculator", "/tmp/temp.txt", "this should not be allowed")}")