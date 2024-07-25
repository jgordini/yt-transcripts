import openai
import os
import sys

# Set your OpenAI API key from environment variable
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Check if the API key is set
if not openai.api_key:
    print("Error: OPENAI_API_KEY environment variable is not set.")
    sys.exit(1)

def get_file_pairs(folder_path):
    apl_files = [f for f in os.listdir(folder_path) if f.endswith('.apl')]
    md_files = [f for f in os.listdir(folder_path) if f.endswith('.md')]
    
    file_pairs = []
    for apl_file in apl_files:
        base_name = apl_file.split('.')[0]
        md_file = next((md for md in md_files if md.endswith(f"-{base_name}.md")), None)
        if md_file:
            file_pairs.append((os.path.join(folder_path, apl_file), os.path.join(folder_path, md_file)))
    return file_pairs

def process_files(apl_file_path, md_file_path):
    with open(apl_file_path, 'r') as apl_file:
        apl_content = apl_file.read()

    with open(md_file_path, 'r') as md_file:
        md_content = md_file.read()

    # Create the prompt for the ChatGPT API
    prompt = f"""You are to incorporate the APL examples into the Markdown text.
APL File Content:
{apl_content}

Markdown File Content:
{md_content}

Incorporate the APL examples into the relevant sections of the Markdown file."""

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert in APL and Markdown documentation."},
            {"role": "user", "content": prompt}
        ]
    )

    updated_md_content = response.choices[0].message['content']

    with open(md_file_path, 'w') as md_file:
        md_file.write(updated_md_content)

    print(f"Processed {apl_file_path} into {md_file_path}")
    print("Updated Markdown Content:")
    print(updated_md_content)
    print(f"Confirmed: {md_file_path} has been updated.\n")

def main():
    if len(sys.argv) != 2:
        print("Usage: python script_name.py foldername")
        sys.exit(1)

    folder_path = sys.argv[1]
    file_pairs = get_file_pairs(folder_path)

    for apl_file_path, md_file_path in file_pairs:
        print(f"Processing pair: {apl_file_path}, {md_file_path}")
        process_files(apl_file_path, md_file_path)

if __name__ == "__main__":
    main()

