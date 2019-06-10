[![Build Status](https://travis-ci.org/steakhal/conan-prometheus-cpp.svg)](https://travis-ci.org/steakhal/conan-prometheus-cpp)
[![Build Status](https://ci.appveyor.com/api/projects/status/github/steakhal/conan-prometheus-cpp)](https://ci.appveyor.com/project/steakhal/conan-prometheus-cpp)


# conan-prometheus-cpp

## Basic setup

    $ conan install . prometheus-cpp/0.7.0@steakhal/stable 
    
## Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*
    
    [requires]
      prometheus-cpp/0.7.0@steakhal/stables

    [options]
      prometheus-cpp:mode=pull                         # no default, you can must specify 'pull' xor 'push'
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

