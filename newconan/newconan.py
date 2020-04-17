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

def W(content, outputFile):
    with open(outputFile, "w") as fout:
        fout.write(content)

def regularize(name):
    return name[0].upper() + name[1:]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("project_name", help="The name of your project.")
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-shared", action='store_true', help="shared library")
    group.add_argument("-exe", action='store_true', help="executable")
    group.add_argument("-static", action='store_true', help="static library")
    
    parser.add_argument("-noci", action='store_true', help="no ci")
    parser.add_argument("-noassets", action='store_true', help="don't create assets")
    parser.add_argument("-notest", action='store_true', help="don't create test")
    parser.add_argument("-basic", action='store_true', help="-noci -noassets -notest")
    
    args = parser.parse_args()
    if not args.exe and not args.shared and not args.static:
        args.exe = True
    if args.basic:
        args.noci = True
        args.noassets = True
        args.notest = True
    
    project_name = args.project_name.strip()
    if not re.match(r"[a-zA-Z][a-zA-Z0-9_\-]*", project_name):
        print("Invalid project name! name pattern: [a-zA-Z][a-zA-Z0-9_-]*")
        return
    mkdirs(project_name)
    cd(project_name)
    project_path = pwd()
    mkdirs("cmake", "src")
    if not args.notest:
        mkdirs("test")
    replace_project_name = lambda content: content.replace("{project_name}", project_name)
    replace_library_shared = lambda content: content.replace("{project_name}", project_name).replace(
        "{is_shared}", 'True')
    replace_library_static = lambda content: content.replace("{project_name}", project_name).replace(
        "{is_shared}", 'False')
    copy = lambda content: content
    
    create_assets = f'''
include(${{CMAKE_CURRENT_SOURCE_DIR}}/cmake/symlink.cmake)
symlink(assets bin/assets)
file(MAKE_DIRECTORY ${{CMAKE_CURRENT_SOURCE_DIR}}/assets/public/{project_name})'''
    
    create_library = f'''
if (BUILD_SHARED)
    add_library({project_name} SHARED ${{sources}})
else()
    add_library({project_name} STATIC ${{sources}})
endif()'''
    
    link_std = '''
    $<$<CXX_COMPILER_ID:GNU>:-static-libgcc>
    $<$<CXX_COMPILER_ID:GNU>:-static-libstdc++>'''
    
    build_test = f'''
if (BUILD_TEST)
    file(GLOB_RECURSE test-sources CONFIGURE_DEPENDS "test/*.cpp")
    foreach (file ${{test-sources}})
      get_filename_component(comp ${{file}} NAME_WE)
      add_executable(${{comp}} ${{file}})
      target_include_directories(${{comp}} PUBLIC
        ${{CMAKE_CURRENT_LIST_DIR}}/test)
      target_link_libraries(${{comp}} PRIVATE {'${CONAN_LIBS}' if args.exe else project_name})
    endforeach ()
endif ()
    '''
    
    content = f'''
cmake_minimum_required(VERSION 3.12)
project({project_name} LANGUAGES C CXX)

set(CMAKE_VERBOSE_MAKEFILE ON)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
{'set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)' if args.shared else ""}
{create_assets if not args.noassets else ''}
include(${{CMAKE_CURRENT_SOURCE_DIR}}/cmake/conan.cmake)
conan_cmake_run(BASIC_SETUP CONANFILE conanfile.py BUILD missing)
{'option(BUILD_TEST "Build test" ON)' if not args.notest else ''}
{'option(BUILD_SHARED "Build shared lib" ON)' if not args.exe else ''}
set(sources src/main.cpp)
{f'add_executable({project_name} ${{sources}})' if args.exe else ''}
{create_library if not args.exe else ''}

target_include_directories({project_name} PUBLIC
    ${{CMAKE_CURRENT_LIST_DIR}}/src)
target_compile_definitions({project_name}
    PRIVATE
    $<$<CONFIG:DEBUG>:DEBUG>)
target_link_libraries({project_name}
    PUBLIC
    ${{CONAN_LIBS}}
    $<$<PLATFORM_ID:Linux>:dl>
{link_std if not args.exe else ''}
)
{build_test if not args.notest else ''}
    '''
    
    W(content, 'CMakeLists.txt')
    if args.exe:
        RMW("conanfile.py", replace_library_static)
    elif args.static:
        RMW("conanfile.py", replace_library_static)
    elif args.shared:
        RMW("conanfile.py", replace_library_shared)
    else:
        raise Exception('Unknown project type! should be one of [exe, static, shared]!')
    if not args.noci:
        RMW(".gitlab-ci.yml", copy)
        RMW("appveyor.yml", copy)
        RMW(".travis.yml", copy)
        mkdirs(".travis")
        RMW(".travis/install.sh", copy)
        RMW(".travis/run.sh", copy)
    RMW("build.py", copy)
    RMW("CMakeSettings.json", copy)
    RMW(".clang-format", copy)
    RMW("gitignore", copy, ".gitignore")
    RMW("README.md", replace_project_name)
    
    cd("src")
    if args.exe:
        RMW("main.cpp", copy)
    else:
        RMW("mainlibrary.cpp", copy, "main.cpp")
        RMW("main.h", copy)
    
    if not args.notest:
        cd("../test")
        if args.exe:
            RMW("test.cpp", copy)
        else:
            RMW("testLibrary.cpp", copy, "test.cpp")
    
    cd("../cmake")
    RMW("conan.cmake", copy)
    if not args.noassets:
        RMW("symlink.cmake", replace_project_name)
        RMW("symlink.py", copy)
    
    cd("..")
    system("git init")
    system("git add .gitignore")
    system("git add -A")
    result = 'Created new '
    if args.exe:
        result += "exe"
    elif args.shared:
        result += "shared library"
    else:
        result += "static library"
    print(f'{result} project: {project_name} (located in {project_path})')
