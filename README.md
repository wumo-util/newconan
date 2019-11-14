`newconan` creates default project structure that is convenient for developing in IDEs like Clion and Visual Studio.<!--more-->

## Requirements

`cmake` >= 3.14 

## Installation
```shell
$ pip install newconan
```

## Create Project
```shell
$ newconan TestExe                      # create exe project
$ newconan TestSharedLibrary -shared    # create shared library project
$ newconan TestStaticLibrary -static    # create static library project
```

## Project Structure

```
TestSharedLibrary
├── .git
├── .travis
│   ├── install.sh
│   └── run.sh
├── assets
│   └── public
│       └── TestSharedLibrary
├── cmake
│   ├── conan.cmake
│   ├── symlink.cmake
│   └── symlink.py
├── src
│   ├── main.cpp
│   └── main.h
├── test
│   └── test.cpp
├── .clang-format
├── .gitignore
├── .gitlab-ci.yml
├── .travis.yml
├── appveyor.yml
├── build.py
├── CMakeLists.txt
├── CMakeSettings.json
├── conanfile.py
└── README.md
```
* `newconan` will automatically create the git repository which is `.git` folder.
* `assets` folder will contains resource files which will be symlink to `${CMAKE_CURRENT_BINARY_DIR}/bin/assets`. In this way, your binary can use the relative path `./assets` to access the resource files.
* `cmake` folder contains some `cmake macros` to symlink folder and setup `conan`.
* `src` folder contains the main source code for your project.
* `test` folder contains all the test `cpp` files.
* `.clang-format` is the default format that `clang-format` will use.
* `.gitignore` ignores everything except exisiting folders and files. You can edit this file to add other folders to git.
* `.gitlab-ci.yml` is the default ci configuration for `gitlab`.
* `.travis.yml` and folder `.travis` is the default ci configuration for `travis`.
* `appveyor.yml` is the default ci configuration for `appveyor`.
* `build.py` will be used by `gitlab-ci` to build and upload this project as `conan recipe` for others to use your library.
* `CMakeLists.txt` will define a target for your project and link all the necessary libraries against it. `CMakeLists.txt` also scans `test` folder and create corresponding a test target for each `cpp` file.
* `CMakeSettings.json` is used by `Visual Studio`. This file will make `Visual Studio` put the `build` folder relative to your project rather than some hashed folder which you can't find easily.
* `conanfile.py` defines the library dependencies. `conan` will download and compile all the required libraries and copy `*.dll/*.dylib` to `${CMAKE_CURRENT_BINARY_DIR}/bin` folder. At the same time, dependent library resource files will also be copied.
* `README.md` shows how to build this project using `cmake` and `conan`.

## Add dependency
You can add library dependencies to your project by modifying the `requires` attribute of `conanfile.py`:
```python
class ProjectNameConan(ConanFile):
    name = "ProjectName"
    version = "1.0.0"
    settings = "os", "compiler", "build_type", "arch"
    requires = ( # Add dependencies here.
        "library1/1.0.0@conan/stable", 
        "library2/2.0.0@conan/testing",
        ...
    ) 
```
And then refresh `cmake`, `conan` will download and compile all the listed dependencies.