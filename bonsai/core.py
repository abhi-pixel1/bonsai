import os
import json


def generate_directory_tree(root):
    walker = next(os.walk(root))
    if not walker[1]:
        return {os.path.basename(root):[walker[2]]}
    

    temp_tree = {os.path.basename(root):[]}
    for i in walker[1]:
        temp_tree[os.path.basename(root)].append(generate_directory_tree(os.path.join(root, i)))

    temp_tree[os.path.basename(root)].append(walker[2])
    return temp_tree



def visualize_tree(json_tree_object, indent=0, branch_positions=[0], last_branch = None):
    prefix = ("----"*indent)
    for i in branch_positions:
        if i<indent*4:
            prefix = (" " * i) + prefix[i:]
            prefix = prefix[:i] + "|" + prefix[i + 1:]

    if last_branch:
        prefix = prefix[:last_branch] + "+" + prefix[last_branch + 1:]

    temp_tree = prefix + list(json_tree_object.keys())[0] + "\n"

    sub_dirs = json_tree_object[list(json_tree_object.keys())[0]][:-1]
    files = json_tree_object[list(json_tree_object.keys())[0]][-1]

    for i in range(0, len(sub_dirs)-1):
        temp_tree = temp_tree + visualize_tree(sub_dirs[i], indent+1, [indent*4]+branch_positions)
    
    if sub_dirs and files:
        temp_tree = temp_tree + visualize_tree(sub_dirs[-1], indent+1, [indent*4]+branch_positions)
    elif sub_dirs:
        temp_tree = temp_tree + visualize_tree(sub_dirs[-1], indent+1, [indent*4]+branch_positions, indent*4)
        
    for i in files:
        if last_branch:
            prefix = prefix[:last_branch] + " " + prefix[last_branch + 1:]
        temp_tree = temp_tree + prefix.replace('-', ' ') + ("|----") + i + "\n"
    
    return temp_tree