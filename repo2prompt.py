import os
import argparse

def get_file_content(file_path):
    """
    Retrieves the content of a file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def build_directory_tree(path='', indent=0, file_paths=[]):
    """
    Builds a string representation of the directory tree and collects file paths.
    """
    tree_str = ""
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if '.git' in item_path.split(os.sep):
            continue
        if os.path.isdir(item_path):
            tree_str += ' ' * indent + f"[{item}/]\n"
            tree_str += build_directory_tree(item_path, indent + 1, file_paths)[0]
        else:
            tree_str += ' ' * indent + f"{item}\n"
            # Indicate which file extensions should be included in the prompt!
            if item.endswith(('.py', '.ipynb', '.html', '.css', '.js', '.jsx', '.rst', '.md')):
                file_paths.append((indent, item_path))
    return tree_str, file_paths

def retrieve_repo_info():
    """
    Retrieves and formats repository information, including README, the directory tree, and file contents,
    while ignoring the .git folder.
    """
    try:
        readme_path = 'README.md'
        if os.path.isfile(readme_path):
            readme_content = get_file_content(readme_path)
            formatted_string = f"README.md:\n```\n{readme_content}\n```\n\n"
        else:
            formatted_string = "README.md: Not found\n\n"
    except Exception as e:
        formatted_string = "Error fetching README\n\n"

    directory_tree, file_paths = build_directory_tree()
    formatted_string += f"Directory Structure:\n{directory_tree}\n"

    for indent, path in file_paths:
        file_content = get_file_content(path)
        formatted_string += '\n' + ' ' * indent + f"{path}:\n" + ' ' * indent + '```\n' + file_content + '\n' + ' ' * indent + '```\n'
    
    return formatted_string

def main():
    parser = argparse.ArgumentParser(description="Retrieve repository information.")
    args = parser.parse_args()

    repo_info = retrieve_repo_info()
    print(repo_info)

if __name__ == "__main__":
    main()
