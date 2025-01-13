import json


def see_tree(json_tree_object, indent=0, pipe_locations=[0], last_folder = None):
    prefix = ("----"*indent)
    for i in pipe_locations:
        if i<indent*4:
            prefix = (" " * i) + prefix[i:]
            prefix = prefix[:i] + "|" + prefix[i + 1:]

    if last_folder:
        prefix = prefix[:last_folder] + "+" + prefix[last_folder + 1:]
    print(prefix + list(json_tree_object.keys())[0])

    dirs = json_tree_object[list(json_tree_object.keys())[0]][:-1]
    files = json_tree_object[list(json_tree_object.keys())[0]][-1]

    for i in range(0, len(dirs)-1):
        see_tree(dirs[i], indent+1, [indent*4]+pipe_locations)
    
    if dirs and files:
        see_tree(dirs[-1], indent+1, [indent*4]+pipe_locations)
    elif dirs:
        see_tree(dirs[-1], indent+1, [indent*4]+pipe_locations, indent*4)
        
    for i in files:
        if last_folder:
            prefix = prefix[:last_folder] + " " + prefix[last_folder + 1:]
        print(prefix.replace('-', ' ') + ("|----") + i)








with open('sample1.json', 'r') as file:
    sample = json.load(file)

see_tree(sample)