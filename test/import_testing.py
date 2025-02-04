import bonzai

d = bonzai.generate_directory_tree(r"C:\Users\abhin\Desktop", show_permissions=True, show_size=True)

# print(d)
print(bonzai.visualize_tree(d))