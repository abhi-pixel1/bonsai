import os
import stat

def file_permissions(filepath):
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


# Example usage
filepath = r"c:\Users\abhin\D_drive\AA_WORKSPACE\BONSAI\bonsai\test\file_permission.py"
permissions = file_permissions(filepath)
print(permissions)