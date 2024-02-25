import os

def file_search(dir_path, depth=0):
    indent = '  ' * depth
    files = os.listdir(dir_path)
    for file in files:
        full_path = os.path.join(dir_path, file)  
        if os.path.isdir(full_path):
            print(f"{indent}|――{file}")
            file_search(full_path, depth + 1)  
        elif os.path.isfile(full_path):
            print(f"{indent}|{file}")
        else:
            pass

dir_path = input("디렉토리 입력:\n")
file_search(dir_path)