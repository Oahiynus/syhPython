import ollama

stream = ollama.chat(
    model='llama3.2',
    messages=[{'role': 'user', 'content': '大海为什么是蓝色的？'}],
    stream=True,
)

for chunk in stream:
  print(chunk['message']['content'], end='', flush=True)