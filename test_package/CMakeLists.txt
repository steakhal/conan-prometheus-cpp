cmake_minimum_required(VERSION 2.8.12)
project(PackageTest CXX)

set(CMAKE_VERBOSE_MAKEFILE ON)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

find_package(prometheus-cpp CONFIG REQUIRED)

if(TEST_PROMETHEUS_PULL)
  add_subdirectory(test-pull)
endif()

if(TEST_PROMETHEUS_PUSH)
  add_subdirectory(test-push)
endif()
