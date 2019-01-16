cmake_minimum_required(VERSION 2.8.12)
project(PackageTest CXX)

set(CMAKE_VERBOSE_MAKEFILE ON)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

find_package(prometheus-cpp CONFIG REQUIRED)

add_executable(sample_server sample_server.cc)
target_link_libraries(sample_server ${CONAN_LIBS})
set_target_properties(sample_server PROPERTIES CXX_STANDARD 11)
