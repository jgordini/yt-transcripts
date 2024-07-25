import openai
import os
import sys

# Set your OpenAI API key from environment variable
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Check if the API key is set
if not openai.api_key:
    print("Error: OPENAI_API_KEY environment variable is not set.")
    sys.exit(1)

def read_files(input_folder):
    print(f"Reading files from {input_folder}...")
    files_content = {}
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            file_path = os.path.join(input_folder, filename)
            print(f"Reading file: {file_path}")
            with open(file_path, 'r') as file:
                files_content[filename] = file.read()
    return files_content

def format_and_convert_to_markdown(text, filename):
    print(f"Converting file {filename} to Markdown...")
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # Replace with the correct model name
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Format the following text as an article and convert it to Markdown:\n\n{text}"}
        ],
        max_tokens=2048
    )
    return response['choices'][0]['message']['content'].strip()

def write_files(output_folder, files_content):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output directory: {output_folder}")
    
    for filename, content in files_content.items():
        md_filename = filename.replace('.txt', '.md')
        file_path = os.path.join(output_folder, md_filename)
        print(f"Writing file: {file_path}")
        with open(file_path, 'w') as file:
            file.write(content)

def main():
    input_folder = 'transcripts'
    output_folder = 'mkdown'
    
    files_content = read_files(input_folder)
    
    md_files_content = {}
    for filename, content in tqdm(files_content.items(), desc="Processing files"):
        md_files_content[filename] = format_and_convert_to_markdown(content, filename)
    
    write_files(output_folder, md_files_content)
    
    print("Conversion completed successfully!")

if __name__ == "__main__":
    main()

