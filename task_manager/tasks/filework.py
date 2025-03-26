import os

script_dir = os.path.dirname(__file__)
filepath = os.path.join(script_dir, 'sample.txt')
file_content = 'Hello world!'

with open(filepath, 'r+', encoding='utf-8') as file:
    content = file.write(file_content)