#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import shutil
from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration
from conans.model.version import Version


class PrometheusCppConan(ConanFile):

    name = 'prometheus-cpp'
    version = '0.6.0'
    license = 'MIT'
    url = 'https://github.com/steakhal/conan-prometheus-cpp'
    homepage = 'https://github.com/jupp0r/prometheus-cpp'
    description = \
        'This library aims to enable Metrics-Driven Development for C++ services'
    topics = (
        'conan',
        'prometheus-cpp',
        'metrics',
        'measure',
        'statistics',
        'profile',
        'log',
        )
    author = 'Balazs Benics <benicsbalazs@gmail.com>'
    settings = ('os', 'compiler', 'build_type', 'arch')
    options = {
        'shared': [True, False],
        'fPIC': [True, False],
        'enable_pull': [True, False],
        'enable_push': [True, False],
        'enable_compression': [True, False],
        'override_cxx_standard_flags': [True, False],
        }
    default_options = {
        'shared': False,
        'fPIC': True,
        'enable_pull': True,
        'enable_push': True,
        'enable_compression': True,
        'override_cxx_standard_flags': True,
        }
    _source_subfolder = 'source_subfolder'
    _build_subfolder = 'build_subfolder'
    exports = 'LICENSE.md'
    exports_sources = ['CMakeLists.txt', _source_subfolder]
    generators = 'cmake'

    def config_options(self):
        """Remove fPIC option on Windows platform
        """

        if self.settings.os == 'Windows':
            self.options.remove('fPIC')

    def source(self):
        """Download and unzip the sources than wrap the original CMake file to call conan_basic_setup
        """

        tools.get('%s/archive/v%s.zip' % (self.homepage, self.version))
        os.rename('prometheus-cpp-%s' % self.version,
                  self._source_subfolder)
        os.rename(os.path.join(self._source_subfolder, 'CMakeLists.txt'
                  ), os.path.join(self._source_subfolder,
                  'CMakeListsOriginal.txt'))
        shutil.move('CMakeLists.txt',
                    os.path.join(self._source_subfolder,
                    'CMakeLists.txt'))

    def configure(self):
        if not self.options.enable_push \
            and not self.options.enable_pull:
            raise ConanInvalidConfiguration('You must enable at least one of push or pull for this package.'
                    )

        cc = self.settings.compiler
        if self.options.enable_push and cc == 'Visual Studio' \
            and Version(cc.version) < '14':
            raise ConanInvalidConfiguration('Visual Studio >= 14 is required, yours is %s'
                     % cc.version)

    def requirements(self):
        if self.options.enable_pull:
            self.requires('civetweb/1.11@civetweb/stable')
            if self.options.enable_compression:
                self.requires.add('zlib/1.2.11@conan/stable')

        if self.options.enable_push:
            self.requires.add('libcurl/7.61.1@bincrafters/stable')
            if self.options.enable_pull:

                # required to resolve version mismatch between civetweb and libcurl
                self.requires('OpenSSL/1.0.2q@conan/stable',
                              override=True)

    def _configure_cmake(self):
        """Create CMake instance and execute configure step
        """

        cmake = CMake(self)
        cmake.definitions['BUILD_SHARED_LIBS'] = self.options.shared

        if self.settings.compiler != 'Visual Studio':
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = \
                self.options.fPIC

        cmake.definitions['ENABLE_PULL'] = self.options.enable_pull
        cmake.definitions['ENABLE_PUSH'] = self.options.enable_push
        cmake.definitions['ENABLE_COMPRESSION'] = \
            self.options.enable_compression
        cmake.definitions['OVERRIDE_CXX_STANDARD_FLAGS'] = \
            self.options.override_cxx_standard_flags

        cmake.definitions['ENABLE_TESTING'] = False
        cmake.definitions['USE_THIRDPARTY_LIBRARIES'] = False

        cmake.configure(build_folder=self._build_subfolder,
                        source_folder=self._source_subfolder)
        return cmake

    def build(self):
        """Configure, build and install prometheus-cpp using CMake.
        """

        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        """Copy prometheus-cpp' artifacts to package folder
        """

        cmake = self._configure_cmake()
        cmake.install()
        self.copy('LICENSE', dst='licenses', src=self._source_subfolder)

        # self.copy(pattern="flathash*", dst="bin", src="bin")
        # self.copy(pattern="flatc*", dst="bin", src="bin")
        # if self.settings.os == "Windows" and self.options.shared:
        #     if self.settings.compiler == "Visual Studio":
        #         shutil.move(os.path.join(self.package_folder, "lib", "%s.dll" % self.name),
        #                     os.path.join(self.package_folder, "bin", "%s.dll" % self.name))
        #     elif self.settings.compiler == "gcc":
        #         shutil.move(os.path.join(self.package_folder, "lib", "lib%s.dll" % self.name),
        #                     os.path.join(self.package_folder, "bin", "lib%s.dll" % self.name))

    def package_info(self):

        self.cpp_info.libs.append("prometheus-cpp-core")

        if self.options.enable_pull:
            self.cpp_info.libs.append('prometheus-cpp-pull')
        if self.options.enable_push:
            self.cpp_info.libs.append('prometheus-cpp-push')

        if self.settings.os == 'Linux':
            self.cpp_info.libs.append('pthread')
            self.cpp_info.libs.append('rt')
            if self.options.shared:
                self.cpp_info.libs.append('dl')

        # gcc's atomic library not linked automatically on clang

        if self.settings.compiler == 'clang':
            self.cpp_info.libs.append('atomic')
