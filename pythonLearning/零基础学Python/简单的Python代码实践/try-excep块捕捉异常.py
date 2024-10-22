try:
    with open('pythonLearning/example.txt', 'r') as file:
        content = file.read()
        print(content)
except FileNotFoundError:
    print('File not found!')
finally:
    print('Execution complete.')