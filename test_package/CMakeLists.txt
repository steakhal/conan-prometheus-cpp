cmake_minimum_required(VERSION 3.0)
project(PackageTest CXX)

set(CMAKE_VERBOSE_MAKEFILE ON)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

find_package(prometheus-cpp CONFIG REQUIRED)

if(TEST_PROMETHEUS_PULL)
  add_subdirectory(test-pull)
else()
  add_subdirectory(test-push)
endif()
