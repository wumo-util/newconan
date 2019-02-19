find_package (Python)
execute_process(COMMAND ${Python_EXECUTABLE} ${CMAKE_CURRENT_LIST_DIR}/symlink.py
    ${CMAKE_CURRENT_SOURCE_DIR}/assets
    ${CMAKE_CURRENT_BINARY_DIR}/bin/assets)
