import os
import argparse

def get_file_content(file_path):
    """
    Retrieves the content of a file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except (IOError, UnicodeDecodeError) as e:
        print(f"Error reading file: {file_path}. Skipping...")
        return None

def build_directory_tree(path, indent, file_paths, include_hidden, max_depth, extensions):
    """
    Builds a string representation of the directory tree and collects file paths.
    """
    tree_str = ""
    if indent > max_depth:
        return tree_str, file_paths
    for item in os.listdir(path):
        if not include_hidden and item.startswith('.'):
            continue
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            tree_str += ' ' * indent + f"[{item}/]\n"
            tree_str_sub, file_paths = build_directory_tree(item_path, indent + 1, file_paths, include_hidden, max_depth, extensions)
            tree_str += tree_str_sub
        else:
            tree_str += ' ' * indent + f"{item}\n"
            if item.endswith(tuple(extensions)):
                file_paths.append((indent, item_path))
    return tree_str, file_paths

def generate_prompt(repo_path, include_hidden=False, max_depth=10, extensions=None):
    """
    Generates a prompt string for the specified repository path.
    """
    if not extensions:
        extensions = ['.py', '.ipynb', '.html', '.css', '.js', '.jsx', '.rst', '.md']
    
    try:
        readme_path = os.path.join(repo_path, 'README.md')
        if os.path.isfile(readme_path):
            readme_content = get_file_content(readme_path)
            prompt = f"README.md:\n```\n{readme_content}\n```\n\n"
        else:
            prompt = "README.md: Not found\n\n"
    except Exception as e:
        prompt = "Error fetching README\n\n"

    directory_tree, file_paths = build_directory_tree(repo_path, 0, [], include_hidden, max_depth, extensions)
    prompt += f"Directory Structure:\n{directory_tree}\n"

    for indent, path in file_paths:
        file_content = get_file_content(path)
        if file_content:
            prompt += '\n' + ' ' * indent + f"{path}:\n" + ' ' * indent + '```\n' + file_content + '\n' + ' ' * indent + '```\n'
    
    return prompt

def save_prompt_to_file(prompt, output_path):
    """
    Saves the generated prompt to a file.
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(prompt)
        print(f"Prompt saved to: {output_path}")
    except IOError as e:
        print(f"Error writing prompt to file: {output_path}. {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Generate a prompt from a repository.")
    parser.add_argument("repo_path", default=".", help="Path to the repository directory")
    parser.add_argument("-o", "--output", default="prompt.txt", help="Output file path")
    parser.add_argument("-i", "--include-hidden", action="store_true", help="Include hidden files and directories")
    parser.add_argument("-d", "--max-depth", type=int, default=10, help="Maximum depth of directory traversal")
    parser.add_argument("-e", "--extensions", nargs="+", default=['.py', '.ipynb', '.html', '.css', '.js', '.jsx', '.rst', '.md'], help="File extensions to include")
    args = parser.parse_args()

    prompt = generate_prompt(args.repo_path, args.include_hidden, args.max_depth, args.extensions)
    save_prompt_to_file(prompt, args.output)

if __name__ == "__main__":
    main()
