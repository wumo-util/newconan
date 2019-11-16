find_package (Python)

function(symlink src dst)
  execute_process(COMMAND ${Python_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/cmake/symlink.py
    "${CMAKE_CURRENT_SOURCE_DIR}/${src}"
    "${CMAKE_CURRENT_BINARY_DIR}/${dst}")
endfunction()

