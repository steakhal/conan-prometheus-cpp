cmake_minimum_required(VERSION 3.0)

project(cmake_wrapper)
message(STATUS "Conan CMake Wrapper")

if(EXISTS ${CMAKE_BINARY_DIR}/../conanbuildinfo.cmake)
  include(${CMAKE_BINARY_DIR}/../conanbuildinfo.cmake)
  conan_basic_setup()
else()
  message(WARNING "The file conanbuildinfo.cmake doesn't exist, you have to run conan install first")
endif()

include(CMakeListsOriginal.txt)
