from bonsai.core import generate_directory_tree
import json


if __name__ == '__main__':
  d = json.dumps(generate_directory_tree('C:\\Users\\abhin\\Desktop\\'), indent=4)
  with open("sample.json",'w') as f:
    f.write(d)