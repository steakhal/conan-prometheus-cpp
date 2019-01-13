#!/usr/bin/env python
# -*- coding: utf-8 -*
from conans import ConanFile, tools, CMake

class PrometheuscppConan(ConanFile):
    name = "prometheus-cpp"
    version = "0.6"
    license = "MIT"
    url = "https://github.com/steakhal/conan-prometheus-cpp"
    homepage = "https://github.com/jupp0r/prometheus-cpp"
    description = "Metrics-Driven Development for C++ in Prometheus Data Model"
    author = "Balazs Benics <benicsbalazs@gmail.com>"
    topics = ("metrics", "measure", "statistics", "profile", "log")
    exports = ("LICENSE.md", "README.md")
    exports_sources = ("src/*", "cmake/*", "include/*", "CMakeLists.txt")
    generators = "cmake"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "enable_pull": [True, False],
        "enable_push": [True, False],
        "enable_compression": [True, False]
    }
    default_options = {
        "shared": False,
        "enable_pull": True,
        "enable_push": True,
        "enable_compression": True
    }
    requires = "civetweb/1.11@civetweb/testing"

    def source(self):
        git = tools.Git(folder=self.name)
        git.clone(self.homepage)
        
        tools.replace_in_file(file_path=self.name + "/CMakeLists.txt",
                              search="project(prometheus-cpp)",
                              replace="""project(prometheus-cpp)
                                 include(../conanbuildinfo.cmake)
                                 conan_basic_setup()""")

    def requirements(self):
        if self.options.enable_pull and self.options.enable_compression:
            self.requires.add("zlib/1.2.11@conan/stable")
        if self.options.enable_push:
            self.requires.add("libcurl/7.61.1@bincrafters/stable")
            self.requires.add("OpenSSL/1.1.1a@conan/stable",  override=True)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.verbose = True
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        cmake.definitions["ENABLE_PULL"] = self.options.enable_pull
        cmake.definitions["ENABLE_PUSH"] = self.options.enable_push
        cmake.definitions["ENABLE_COMPRESSION"] = self.options.enable_compression
        cmake.definitions["OVERRIDE_CXX_STANDARD_FLAGS"] = False
        cmake.definitions["ENABLE_TESTING"] = False
        cmake.definitions["USE_THIRDPARTY_LIBRARIES"] = False
        cmake.configure(source_folder="prometheus-cpp", build_folder="build")
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("LICENSE.md", dst="licenses")
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["prometheus-cpp-core"]
        if self.options.enable_pull:
            self.cpp_info.libs.append("prometheus-cpp-pull")
        if self.options.enable_push:
            self.cpp_info.libs.append("prometheus-cpp-push")
