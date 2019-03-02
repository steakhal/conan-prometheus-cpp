#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
from conans import ConanFile, CMake, tools
from conans.errors import ConanException
from conans.model.version import Version

class PrometheusCppConan(ConanFile):
    name = "prometheus-cpp"
    version = "0.6.0"
    license = "MIT"
    url = "https://github.com/steakhal/conan-prometheus-cpp"
    homepage = "https://github.com/jupp0r/prometheus-cpp"
    description = "This library aims to enable Metrics-Driven Development for C++ services"
    topics = ("conan", "prometheus-cpp","metrics", "measure", "statistics", "profile", "log")
    author = "Balazs Benics <benicsbalazs@gmail.com>"
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
    source_subfolder = "source_subfolder"
    exports = "LICENSE.md"
    exports_sources = ["CMakeLists.txt", source_subfolder]
    generators = "cmake"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        tools.get("%s/archive/v%s.zip" % (self.homepage, self.version))
        os.rename("prometheus-cpp-%s" % self.version, self.source_subfolder)
        os.rename(os.path.join(self.source_subfolder, "CMakeLists.txt"),
                  os.path.join(self.source_subfolder, "CMakeLists_original.txt"))
        shutil.copy("CMakeLists.txt",
                    os.path.join(self.source_subfolder, "CMakeLists.txt"))

    def configure(self):
        if not self.options.enable_push and not self.options.enable_pull:
            raise ConanException('You must enable at least one of push or pull for this package.')
        
        cc = self.settings.compiler
        if self.options.enable_push and cc == 'Visual Studio' and Version(cc.version) < '14':
            raise ConanException('Visual Studio >= 14 is required, yours is %s' % cc.version)

    def requirements(self):
        self.requires("civetweb/1.11@civetweb/stable")
        self.requires("OpenSSL/1.0.2q@conan/stable", override=True)
        
        if self.options.enable_pull and self.options.enable_compression:
            self.requires.add("zlib/1.2.11@conan/stable")
        if self.options.enable_push:
            self.requires.add("libcurl/7.61.1@bincrafters/stable")

    def build(self):
        cmake = CMake(self)
        cmake.definitions['BUILD_SHARED_LIBS'] = self.options.shared
        
        if self.settings.compiler != 'Visual Studio':
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
        
        cmake.definitions["ENABLE_PULL"] = self.options.enable_pull
        cmake.definitions["ENABLE_PUSH"] = self.options.enable_push
        cmake.definitions["ENABLE_COMPRESSION"] = self.options.enable_compression
        cmake.definitions["OVERRIDE_CXX_STANDARD_FLAGS"] = self.options.override_cxx_standard_flags
        
        cmake.definitions["ENABLE_TESTING"] = False
        cmake.definitions["USE_THIRDPARTY_LIBRARIES"] = False
        
        cmake.configure(source_dir=os.path.join(self.source_folder, self.source_subfolder))
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("LICENSE", dst="licenses", src=self.source_subfolder)
        # cmake = self._configure_cmake()
        # cmake.install()

    def package_info(self):
        #self.cpp_info.libs.append("prometheus-cpp-core")
        
        if self.options.enable_pull:
            self.cpp_info.libs.append("prometheus-cpp-pull")
        if self.options.enable_push:
            self.cpp_info.libs.append("prometheus-cpp-push")
        
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
        
        # gcc's atomic library not linked automatically on clang
        if self.settings.compiler == "clang":
            self.cpp_info.libs.append("atomic")
        
        if self.options.shared and self.settings.os == "Linux":
            self.cpp_info.libs.append("dl")
