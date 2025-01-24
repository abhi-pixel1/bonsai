# import os



# def validate_directory(func):
#     def inner(root):
#         if os.path.isdir(root):
#             return func(root)
#         else:
#             raise Exception(f"Directory '{root}' does not exist.")
#     return inner




# def check_file_access(filepath):
#     try:
#         readable = os.access(filepath, os.R_OK)
#         writable = os.access(filepath, os.W_OK)
#         access = ""
#         if readable:
#             access += "(r)"
#         if writable:
#             access += "(w)"
#         if not access:
#             access = "(*)"  # No access
#         return f"{os.path.basename(filepath)} {access}"
#     except Exception:
#         return f"{os.path.basename(filepath)} (*)"  # Skip errors safely


# @validate_directory
# def generate_directory_tree(root):
#     walker = next(os.walk(root))
#     sub_dirs = walker[1]
#     files = walker[2]

#     # Base case: No subdirectories or files
#     if not sub_dirs and not files:
#         return {os.path.basename(root): []}

#     temp_tree = {os.path.basename(root): []}

#     # Add subdirectories
#     for sub_dir in sub_dirs:
#         temp_tree[os.path.basename(root)].append(generate_directory_tree(os.path.join(root, sub_dir)))

#     # Add files
#     temp_tree[os.path.basename(root)].append([check_file_access(os.path.join(root, f)) for f in files])
#     # temp_tree[os.path.basename(root)].append(files)

#     return temp_tree


# def visualize_tree(json_tree_object, indent=0, branch_positions=None, last_branch=None):
#     if branch_positions is None:
#         branch_positions = []

#     # Prefix construction
#     prefix = ""
#     for i in range(indent):
#         if i * 4 in branch_positions:
#             prefix += "|   "
#         else:
#             prefix += "    "

#     if last_branch:
#         prefix += "+--- "
#     else:
#         prefix += "|--- "

#     # Extract current directory or file name
#     dir_name = list(json_tree_object.keys())[0]
#     temp_tree = prefix + dir_name + "\n"

#     # Get subdirectories and files
#     sub_dirs_and_files = json_tree_object[dir_name]
#     sub_dirs = sub_dirs_and_files[:-1] if len(sub_dirs_and_files) > 1 else []
#     files = sub_dirs_and_files[-1] if sub_dirs_and_files else []

#     # Update branch_positions for the current level
#     new_branch_positions = branch_positions + [indent * 4]

#     # Process subdirectories
#     for i, sub_dir in enumerate(sub_dirs):
#         is_last = i == len(sub_dirs) - 1 and not files
#         temp_tree += visualize_tree(sub_dir, indent + 1, new_branch_positions, is_last)

#     # Process files
#     if files:
#         for i, file in enumerate(files):
#             is_last = i == len(files) - 1
#             file_prefix = ""
#             for j in range(indent + 1):
#                 if j * 4 in new_branch_positions:
#                     file_prefix += "|   "
#                 else:
#                     file_prefix += "    "
#             file_prefix += "+--- " if is_last else "|--- "
#             temp_tree += file_prefix + file + "\n"

#     return temp_tree


# def get_relative_path(destination_path, base_path=None):
#     """
#     Returns the relative path to the DESTINATION_PATH from the BASE_PATH.
#     If BASE_PATH is not provided, the current working directory is used.

#     Raises:
#         ValueError: If the destination or base path does not exist.
#     """
#     base_path = base_path or os.getcwd()

#     # Check if the paths exist
#     if not os.path.exists(destination_path):
#         raise ValueError(f"The destination path '{destination_path}' does not exist.")
#     if not os.path.exists(base_path):
#         raise ValueError(f"The base path '{base_path}' does not exist.")

#     try:
#         relative_path = os.path.relpath(destination_path, base_path)
#         return relative_path
#     except Exception as e:
#         raise Exception(f"An error occurred while calculating the relative path: {e}")








########################################################################################v3

import os
import stat
from colorama import Fore, Style

# Box-drawing characters using Unicode
VERTICAL = '\u2502'       # │
HORIZONTAL = '\u2500'     # ─
T_JUNCTION = '\u251C'     # ├
L_JUNCTION = '\u2514'     # └


def file_permissions(filepath: str) -> str:
    """
    Returns the file permissions for a given file or directory.

    Args:
        filepath (str): The path to the file or directory for which the permissions are to be retrieved.

    Returns:
        str: A string representing the file permissions in the format:
            [d]rw-r--r-- where:
                - [d] indicates if it's a directory (d) or file (-)
                - The next three characters represent the owner's permissions (rwx)
                - The following three characters represent the group's permissions (rwx)
                - The last three characters represent others' permissions (rwx)
    """
    st = os.stat(filepath)
    mode = st.st_mode

    # Determine if it's a directory or a file
    is_dir = "d" if stat.S_ISDIR(mode) else "-"

    # Owner permissions
    owner_perms = (
        ("r" if mode & stat.S_IRUSR else "-") +
        ("w" if mode & stat.S_IWUSR else "-") +
        ("x" if mode & stat.S_IXUSR else "-")
    )

    # Group permissions
    group_perms = (
        ("r" if mode & stat.S_IRGRP else "-") +
        ("w" if mode & stat.S_IWGRP else "-") +
        ("x" if mode & stat.S_IXGRP else "-")
    )

    # Others permissions
    others_perms = (
        ("r" if mode & stat.S_IROTH else "-") +
        ("w" if mode & stat.S_IWOTH else "-") +
        ("x" if mode & stat.S_IXOTH else "-")
    )

    # Combine into full permissions string
    permissions = is_dir + owner_perms + group_perms + others_perms
    return permissions


def get_file_size(file_path: str) -> float:
    """
    Returns the size of a file in kilobytes (KB).
    """
    # Get the file size in bytes
    file_size_bytes = os.path.getsize(file_path)
    # Convert to kilobytes
    file_size_kb = file_size_bytes / 1024
    return file_size_kb


def generate_directory_tree(root: str) -> dict:
    """
    Generates a JSON-like object representing the directory tree starting from the given root directory.
    
    The resulting structure includes all details related to the directory, such as subdirectories,
    files, their permissions, and sizes.

    Args:
        root (str): The root directory path.

    Returns:
        dict: A nested dictionary representing the directory tree structure.
              - Each key is a directory name.
              - Each value is a list containing:
                - Nested dictionaries for subdirectories.
                - A list of files, where each file is represented as:
                  [filename, permissions, size (in KB)].

    Raises:
        Exception: If the provided root is not a valid directory.
    """
    # Validation: Ensure the root is a valid directory
    if not os.path.isdir(root):
        raise Exception(f"Directory '{root}' does not exist.")
    
    def _generate_directory_tree_recursive(root: str) -> dict:
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
        temp_tree[os.path.basename(root)].append([ [f, file_permissions(os.path.join(root, f)), get_file_size(os.path.join(root, f))] for f in files])
        # temp_tree[os.path.basename(root)].append(files)

        return temp_tree
    
    # Call the private recursive helper function
    return _generate_directory_tree_recursive(root)

# def visualize_tree(
#     json_tree_object: dict,
#     show_permissions=False,
#     show_size=False
# )->str:
#     """
#     Public function to visualize a directory tree.
#     It calls a private helper function to handle recursion.

#     Args:
#         json_tree_object (dict): The directory tree object.
#         show_permissions (bool): Whether to include file permissions.
#         show_size (bool): Whether to include file sizes.

#     Returns:
#         str: The visualized directory tree as a string.
#     """
#     def _visualize_tree_recursive(
#             json_tree_object: dict,
#             indent=0, 
#             branch_positions=None, 
#             last_branch=None
#     ) -> str:
#         if branch_positions is None:
#             branch_positions = []

#         # Prefix construction
#         prefix = ""
#         for i in range(indent):
#             if i * 4 in branch_positions:
#                 prefix += f"{VERTICAL}   " # Vertical line for continuing branches
#             else:
#                 prefix += "    "

#         if last_branch:
#             prefix += f"{L_JUNCTION}{HORIZONTAL * 2} "  # L-junction for the last branch
#         else:
#             prefix += f"{T_JUNCTION}{HORIZONTAL * 2} "  # T-junction for intermediate branches

#         # Extract current directory or file name
#         dir_name = list(json_tree_object.keys())[0]
#         temp_tree = prefix + Fore.BLUE + dir_name + Style.RESET_ALL + "\n"

#         # Get subdirectories and files
#         sub_dirs_and_files = json_tree_object[dir_name]
#         sub_dirs = sub_dirs_and_files[:-1] if len(sub_dirs_and_files) > 1 else []
#         files = sub_dirs_and_files[-1] if sub_dirs_and_files else []

#         # Update branch_positions for the current level
#         new_branch_positions = branch_positions + [indent * 4]

#         # Process subdirectories
#         for i, sub_dir in enumerate(sub_dirs):
#             is_last = i == len(sub_dirs) - 1 and not files
#             temp_tree += _visualize_tree_recursive(sub_dir, indent + 1, new_branch_positions, is_last)

#         # Process files
#         if files:
#             for i, file in enumerate(files):
#                 is_last = i == len(files) - 1
#                 file_prefix = ""
#                 for j in range(indent + 1):
#                     if j * 4 in new_branch_positions:
#                         file_prefix += f"{VERTICAL}   "  # Vertical line for continuing branches
#                     else:
#                         file_prefix += "    "
#                 file_prefix += f"{L_JUNCTION}{HORIZONTAL * 2} " if is_last else f"{T_JUNCTION}{HORIZONTAL * 2} "
#                 file_info = Fore.GREEN + file[0] + Style.RESET_ALL  # File name
#                 if show_permissions:
#                     file_info += f" [{file[1]}]"  # File permissions
#                 if show_size:
#                     file_info += f" {round(file[2])}kb"  # File size in KB
#                 temp_tree += f"{file_prefix} {file_info}\n"

#         return temp_tree
    
#     # Call the private helper function with initial values
#     return _visualize_tree_recursive(json_tree_object, last_branch=True)


def visualize_tree(
    json_tree_object: dict,
    show_permissions=False,
    show_size=False
)->str:
    """
    Public function to visualize a directory tree.
    It calls a private helper function to handle recursion.

    Args:
        json_tree_object (dict): The directory tree object.
        show_permissions (bool): Whether to include file permissions.
        show_size (bool): Whether to include file sizes.

    Returns:
        str: The visualized directory tree as a string.
    """
    def _visualize_tree_recursive(
            json_tree_object: dict,
            indent=0, 
            branch_positions=None, 
            is_last_branch=None
    ) -> str:
        if branch_positions is None:
            branch_positions = []

        # Prefix construction
        prefix = ""
        if indent > 0:  # Skip prefix for the root directory
            for i in range(indent - 1):
                if i * 4 in branch_positions:
                    prefix += f"{VERTICAL}   " # Vertical line for continuing branches
                else:
                    prefix += "    "

            if is_last_branch is True:  # If it's the last branch at the current level
                prefix += f"{L_JUNCTION}{HORIZONTAL * 2} "  # L-junction for the last branch
            elif is_last_branch is False:
                prefix += f"{T_JUNCTION}{HORIZONTAL * 2} "  # T-junction for intermediate branches

        # Extract current directory or file name
        dir_name = list(json_tree_object.keys())[0]
        temp_tree = prefix + Fore.BLUE + dir_name + Style.RESET_ALL + "\n"

        # Get subdirectories and files
        sub_dirs_and_files = json_tree_object[dir_name]
        sub_dirs = sub_dirs_and_files[:-1] if len(sub_dirs_and_files) > 1 else []
        files = sub_dirs_and_files[-1] if sub_dirs_and_files else []

        # Update branch_positions for the current level
        new_branch_positions = branch_positions + [indent * 4]

        # Process subdirectories
        for i, sub_dir in enumerate(sub_dirs):
            is_last = i == len(sub_dirs) - 1 and not files
            temp_tree += _visualize_tree_recursive(sub_dir, indent + 1, new_branch_positions, is_last)

        # Process files
        if files:
            for i, file in enumerate(files):
                is_last = i == len(files) - 1
                file_prefix = ""
                for j in range(indent):
                    if j * 4 in new_branch_positions:
                        file_prefix += f"{VERTICAL}   "  # Vertical line for continuing branches
                    else:
                        file_prefix += "    "
                file_prefix += f"{L_JUNCTION}{HORIZONTAL * 2} " if is_last else f"{T_JUNCTION}{HORIZONTAL * 2} "
                file_info = Fore.GREEN + file[0] + Style.RESET_ALL  # File name
                if show_permissions:
                    file_info += f" [{file[1]}]"  # File permissions
                if show_size:
                    file_info += f" {round(file[2])}kb"  # File size in KB
                temp_tree += f"{file_prefix}{file_info}\n"

        return temp_tree
    
    # Call the private helper function with initial values
    return _visualize_tree_recursive(json_tree_object, is_last_branch=True)


























































def get_relative_path(destination_path: str, base_path=None) -> str:
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