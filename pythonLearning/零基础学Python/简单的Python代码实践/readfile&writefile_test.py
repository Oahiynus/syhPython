with open('pythonLearning/example.txt', 'r') as file:
    content = file.read()
    print(content)

with open('pythonLearning/output.txt', 'w') as file:
    file.write('Hello, World!\n')

    lines = ['line 1\n', 'line 2\n', 'line 3\n']
    file.writelines(lines)