from bonsai.core import generate_directory_tree, visualize_tree
import json


if __name__ == '__main__':
  dict = generate_directory_tree('C:\\Users\\abhin\\Desktop\\')
  # print(dict)
  json1 = json.dumps(dict, indent=4)
  print(visualize_tree(generate_directory_tree('C:\\Users\\abhin\\Desktop\\')))
  with open("sample.json",'w') as f:
    f.write(json1)