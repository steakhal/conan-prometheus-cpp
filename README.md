[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://travis-ci.org/steakhal/conan-prometheus-cpp.svg)](https://travis-ci.org/steakhal/conan-prometheus-cpp)
[![Build Status](https://ci.appveyor.com/api/projects/status/github/steakhal/conan-prometheus-cpp)](https://ci.appveyor.com/project/steakhal/conan-prometheus-cpp)
[![Download](https://api.bintray.com/packages/steakhal/conan/prometheus-cpp%3Acivetweb/images/download.svg)](https://bintray.com/steakhal/conan/prometheus-cpp%3Acivetweb/_latestVersion)

# conan-prometheus-cpp

## Basic setup

    $ conan install . prometheus-cpp/0.7.0@steakhal/stable -o prometheus-cpp:mode=pull
    
## Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*
    
    [requires]
      prometheus-cpp/0.7.0@steakhal/stable

    [options]
      prometheus-cpp:mode=pull                         # REQUIRED, you must specify 'pull' xor 'push'
      prometheus-cpp:shared=False                      # default is False
      prometheus-cpp:enable_compression=True           # default is True
      prometheus-cpp:override_cxx_standard_flags=True  # default is True
      prometheus-cpp:fPIC=True                         # default is True

    [generators]
      cmake

Complete the installation of requirements for your project running:

    conan install .

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.cmake* with all the 
paths and variables that you need to link with your dependencies.

