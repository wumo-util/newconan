from os import chdir as cd, makedirs, system, getcwd as pwd
from os.path import exists, join, dirname
import argparse
import re

def mkdirs(*dirs):
    for dir in dirs:
        if not exists(dir):
            makedirs(dir)

data_dir = join(dirname(__file__), "data")

def RMW(file, op, outputFile=None):
    with open(join(data_dir, file), "r") as fin:
        content = fin.read()
    content = op(content)
    with open(outputFile if outputFile else file, "w") as fout:
        fout.write(content)

def regularize(name):
    return name[0].upper() + name[1:]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("project_name", help="The name of your project.")
    parser.add_argument("-t", "--type", choices=["exe", "static", "shared"], default="exe",
                        help="The type of your project, choices are exe(default), static, shared.")
    args = parser.parse_args()
    project_name = args.project_name.strip()
    if not re.match(r"[a-zA-Z][a-zA-Z0-9_\-]*", project_name):
        print("Invalid project name! name pattern: [a-zA-Z][a-zA-Z0-9_-]*")
        return
    # project_name = ''.join(regularize(x) for x in re.split(r"[_\-]+", project_name))
    project_type = args.type
    mkdirs(project_name)
    cd(project_name)
    project_path = pwd()
    mkdirs("cmake", "src", "test")
    
    replace_project_name = lambda content: content.replace("{project_name}", project_name)
    replace_library_shared = lambda content: content.replace("{project_name}", project_name).replace(
        "{library_type}", 'SHARED')
    replace_library_static = lambda content: content.replace("{project_name}", project_name).replace(
        "{library_type}", 'STATIC')
    copy = lambda content: content
    if project_type == 'exe':
        RMW("ExeCMakeLists.txt", replace_project_name, "CMakeLists.txt")
    elif project_type == 'static':
        RMW("LibraryCMakeLists.txt", replace_library_static, "CMakeLists.txt")
    elif project_type == 'shared':
        RMW("LibraryCMakeLists.txt", replace_library_shared, "CMakeLists.txt")
    else:
        raise Exception('Unknown project type! should be one of [exe, static, shared]!')
    RMW("conanfile.py", replace_project_name)
    RMW("CMakeSettings.json", copy)
    RMW(".clang-format", copy)
    RMW("gitignore", copy, ".gitignore")
    RMW("README.md", replace_project_name)
    
    cd("src")
    if project_type == 'exe':
        RMW("main.cpp", copy)
    else:
        RMW("mainlibrary.cpp", copy, "main.cpp")
        RMW("main.h", copy)
    
    cd("../test")
    if project_type == 'exe':
        RMW("test.cpp", copy)
    else:
        RMW("testLibrary.cpp", copy, "test.cpp")
    
    cd("../cmake")
    RMW("conan.cmake", copy)
    RMW("symlink.cmake", replace_project_name)
    RMW("symlink.py", copy)
    
    cd("..")
    system("git init")
    system("git add .gitignore")
    system("git add -A")
    print(f'Created new {project_type}'
          f'{" " if project_type == "exe" else " library "}project: '
          f'{project_name} ({project_path})')
