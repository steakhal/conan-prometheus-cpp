cmake_minimum_required(VERSION 2.8.12)
project(PackageTest CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(sample_server sample_server.cc)
target_link_libraries(sample_server ${CONAN_LIBS})
