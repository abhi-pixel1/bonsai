import os



def validate_directory(func):
    def inner(root):
        if os.path.isdir(root):
            return func(root)
        else:
            raise Exception(f"Directory '{root}' does not exist.")
    return inner




def check_file_access(filepath):
    try:
        readable = os.access(filepath, os.R_OK)
        writable = os.access(filepath, os.W_OK)
        access = ""
        if readable:
            access += "(r)"
        if writable:
            access += "(w)"
        if not access:
            access = "(*)"  # No access
        return f"{os.path.basename(filepath)} {access}"
    except Exception:
        return f"{os.path.basename(filepath)} (*)"  # Skip errors safely


@validate_directory
def generate_directory_tree(root):
    walker = next(os.walk(root))
    sub_dirs = walker[1]
    files = walker[2]

    # Base case: No subdirectories or files
    if not sub_dirs and not files:
        return {os.path.basename(root): []}

    temp_tree = {os.path.basename(root): []}

    # Add subdirectories
    for sub_dir in sub_dirs:
        temp_tree[os.path.basename(root)].append(generate_directory_tree(os.path.join(root, sub_dir)))

    # Add files
    temp_tree[os.path.basename(root)].append([check_file_access(os.path.join(root, f)) for f in files])
    # temp_tree[os.path.basename(root)].append(files)

    return temp_tree


def visualize_tree(json_tree_object, indent=0, branch_positions=None, last_branch=None):
    if branch_positions is None:
        branch_positions = []

    # Prefix construction
    prefix = ""
    for i in range(indent):
        if i * 4 in branch_positions:
            prefix += "|   "
        else:
            prefix += "    "

    if last_branch:
        prefix += "+--- "
    else:
        prefix += "|--- "

    # Extract current directory or file name
    dir_name = list(json_tree_object.keys())[0]
    temp_tree = prefix + dir_name + "\n"

    # Get subdirectories and files
    sub_dirs_and_files = json_tree_object[dir_name]
    sub_dirs = sub_dirs_and_files[:-1] if len(sub_dirs_and_files) > 1 else []
    files = sub_dirs_and_files[-1] if sub_dirs_and_files else []

    # Update branch_positions for the current level
    new_branch_positions = branch_positions + [indent * 4]

    # Process subdirectories
    for i, sub_dir in enumerate(sub_dirs):
        is_last = i == len(sub_dirs) - 1 and not files
        temp_tree += visualize_tree(sub_dir, indent + 1, new_branch_positions, is_last)

    # Process files
    if files:
        for i, file in enumerate(files):
            is_last = i == len(files) - 1
            file_prefix = ""
            for j in range(indent + 1):
                if j * 4 in new_branch_positions:
                    file_prefix += "|   "
                else:
                    file_prefix += "    "
            file_prefix += "+--- " if is_last else "|--- "
            temp_tree += file_prefix + file + "\n"

    return temp_tree


def get_relative_path(destination_path, base_path=None):
    """
    Returns the relative path to the DESTINATION_PATH from the BASE_PATH.
    If BASE_PATH is not provided, the current working directory is used.

    Raises:
        ValueError: If the destination or base path does not exist.
    """
    base_path = base_path or os.getcwd()

    # Check if the paths exist
    if not os.path.exists(destination_path):
        raise ValueError(f"The destination path '{destination_path}' does not exist.")
    if not os.path.exists(base_path):
        raise ValueError(f"The base path '{base_path}' does not exist.")

    try:
        relative_path = os.path.relpath(destination_path, base_path)
        return relative_path
    except Exception as e:
        raise Exception(f"An error occurred while calculating the relative path: {e}")