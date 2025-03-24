import os

def print_tree(startpath, level=2):
    for root, dirs, files in os.walk(startpath):
        depth = root.replace(startpath, '').count(os.sep)
        if depth >= level:
            continue
        indent = ' ' * 4 * (depth)
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 4 * (depth + 1)
        for f in files:
            print(f'{subindent}{f}')

if __name__ == "__main__":
    print("Project Directory Tree:")
    print_tree('.', level=2)