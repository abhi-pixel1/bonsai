import os
import json

def gen_tree(root):
    walker = next(os.walk(root))
    if not walker[1]:
        return {os.path.basename(root):[walker[2]]}
    

    temp_tree = {os.path.basename(root):[]}
    for i in walker[1]:
        temp_tree[os.path.basename(root)].append(gen_tree(os.path.join(root, i)))

    # for i in walker[2]:
    #     temp_tree[os.path.basename(root)].append(i)
    temp_tree[os.path.basename(root)].append(walker[2])
    return temp_tree








dict = gen_tree(r"C:\Users\abhin\Desktop")
json_object = json.dumps(dict, indent=4)
print(json_object)


with open("sample.json", "w") as f:
    f.write(json_object)