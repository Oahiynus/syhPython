import ollama
response = ollama.chat(model='llama3.2', messages=[
  {
    'role': 'user',
    'content': '大海为什么是蓝色的？',
  },
])
print(response['message']['content'])