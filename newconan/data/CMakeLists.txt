cmake_minimum_required(VERSION 3.12)
project({project_name} LANGUAGES C CXX)

set(CMAKE_VERBOSE_MAKEFILE ON)
set(CMAKE_CXX_STANDARD 17)

include(${CMAKE_CURRENT_LIST_DIR}/cmake/conan.cmake)
conan_cmake_run(
    BASIC_SETUP
    CONANFILE conanfile.py
    BUILD missing)

file(COPY ${CMAKE_SOURCE_DIR}/bin DESTINATION ${CMAKE_BINARY_DIR})

add_executable({project_name}
    src/main.cpp
    )

target_include_directories({project_name} PUBLIC
    ${CMAKE_CURRENT_LIST_DIR}/src)
target_compile_definitions({project_name}
    PRIVATE
    $<$<CONFIG:DEBUG>:DEBUG>)
target_link_libraries({project_name}
    PRIVATE
    ${CONAN_LIBS}
    $<$<PLATFORM_ID:Linux>:dl>)
