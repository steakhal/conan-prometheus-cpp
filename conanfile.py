#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from conans import ConanFile, CMake, tools


class PrometheusCppConan(ConanFile):
    name = "prometheus-cpp"
    version = "0.6.0"
    license = "MIT"
    author = "Balazs Benics <benicsbalazs@gmail.com>"
    url = "https://github.com/steakhal/conan-prometheus-cpp"
    homepage = "https://github.com/jupp0r/prometheus-cpp"
    description = "This library aims to enable Metrics-Driven Development for C++ services"
    topics = ("conan", "prometheus-cpp","metrics", "measure", "statistics", "profile", "log")
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "enable_pull": [True, False],
        "enable_push": [True, False],
        "enable_compression": [True, False],
        "override_cxx_standard_flags": [True, False]
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "enable_pull": True,
        "enable_push": True,
        "enable_compression": True,
        "override_cxx_standard_flags": True
    }
    exports = "LICENSE"
    exports_sources = "CMakeLists.txt"
    generators = "cmake"
    _source_subfolder = "source_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        tools.get("{0}/archive/v{1}.zip".format(self.homepage, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def requirements(self):
        self.requires("civetweb/1.11@civetweb/stable")
        self.requires("OpenSSL/1.0.2q@conan/stable", override=True)
        if self.options.enable_pull:
            self.requires.add("zlib/1.2.11@conan/stable")
        if self.options.enable_push:
            self.requires.add("libcurl/7.61.1@bincrafters/stable")

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["ENABLE_PULL"] = self.options.enable_pull
        cmake.definitions["ENABLE_PUSH"] = self.options.enable_push
        cmake.definitions["ENABLE_COMPRESSION"] = self.options.enable_compression
        cmake.definitions["OVERRIDE_CXX_STANDARD_FLAGS"] = self.options.override_cxx_standard_flags
        cmake.definitions["ENABLE_TESTING"] = False
        cmake.definitions["USE_THIRDPARTY_LIBRARIES"] = False
        cmake.configure()
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        if self.options.enable_pull:
            self.cpp_info.libs.append("prometheus-cpp-pull")
        if self.options.enable_push:
            self.cpp_info.libs.append("prometheus-cpp-push")
        self.cpp_info.libs.append("prometheus-cpp-core")
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")

