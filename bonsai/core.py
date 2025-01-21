# import os
# import json


# def generate_directory_tree(root):
#     walker = next(os.walk(root))
#     if not walker[1]:
#         return {os.path.basename(root):[walker[2]]}
    

#     temp_tree = {os.path.basename(root):[]}
#     for i in walker[1]:
#         temp_tree[os.path.basename(root)].append(generate_directory_tree(os.path.join(root, i)))

#     temp_tree[os.path.basename(root)].append(walker[2])
#     return temp_tree



# def visualize_tree(json_tree_object, indent=0, branch_positions=[0], last_branch = None):
#     prefix = ("----"*indent)
#     for i in branch_positions:
#         if i<indent*4:
#             prefix = (" " * i) + prefix[i:]
#             prefix = prefix[:i] + "|" + prefix[i + 1:]

#     if last_branch:
#         prefix = prefix[:last_branch] + "+" + prefix[last_branch + 1:]

#     temp_tree = prefix + list(json_tree_object.keys())[0] + "\n"

#     sub_dirs = json_tree_object[list(json_tree_object.keys())[0]][:-1]
#     files = json_tree_object[list(json_tree_object.keys())[0]][-1]

#     for i in range(0, len(sub_dirs)-1):
#         temp_tree = temp_tree + visualize_tree(sub_dirs[i], indent+1, [indent*4]+branch_positions)
    
#     if sub_dirs and files:
#         temp_tree = temp_tree + visualize_tree(sub_dirs[-1], indent+1, [indent*4]+branch_positions)
#     elif sub_dirs:
#         temp_tree = temp_tree + visualize_tree(sub_dirs[-1], indent+1, [indent*4]+branch_positions, indent*4)
        
#     for i in files:
#         if last_branch:
#             prefix = prefix[:last_branch] + " " + prefix[last_branch + 1:]
#         temp_tree = temp_tree + prefix.replace('-', ' ') + ("|----") + i + "\n"
    
#     return temp_tree





###################################################v2

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