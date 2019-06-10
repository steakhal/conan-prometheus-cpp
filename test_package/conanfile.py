#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, time, shutil, subprocess, requests, glob
from conans import ConanFile, CMake, tools

class PrometheusCppConanTest(ConanFile):
    settings = ('os', 'compiler', 'build_type', 'arch')
    generators = 'cmake'

    def build(self):
        cmake = CMake(self)
        cmake.definitions['TEST_PROMETHEUS_PULL'] = (self.options['prometheus-cpp'].mode == 'pull')
        cmake.configure()
        cmake.build()

    def test(self):
        prometheus_path = self.deps_cpp_info['prometheus-cpp'].rootpath

        prometheus_license    = os.path.join(prometheus_path, 'licenses', 'LICENSE')
        conan_package_license = os.path.join(prometheus_path, 'licenses', 'LICENSE.md')
        assert(os.path.exists(prometheus_license))
        assert(os.path.exists(conan_package_license))

        if tools.cross_building(self.settings):
            self.output.warn('Cross Building: Skipping Test Package')
            return

        libs = []
        libs.append(glob.glob(os.path.join(prometheus_path, 'bin', '*.dll')))
        libs.append(glob.glob(os.path.join(prometheus_path, 'lib', '*.so')))
        libs.append(glob.glob(os.path.join(prometheus_path, 'lib', '*.dylib')))
        for lib in [item for sublist in libs for item in sublist]:
          shutil.copy(src=lib, dst='bin')

        if self.options['prometheus-cpp'].mode == 'pull':
            sample_server_path = os.path.join('bin', 'sample_server')
            sample_server = subprocess.Popen([sample_server_path])
            self.output.info('Running sample server')
            time.sleep(1)
            try:
                response = requests.get('http://localhost:8080/metrics')
            finally:
                sample_server.kill()
                assert(response.ok)
                assert(-1 != response.text.find('How many seconds is this server running?'))
        else: # mode == 'push':
            self.output.warn('Test for push mode is not yet implemented: Skipping Test Package')
            # TODO finish
            return
            sample_client_path = os.path.join('bin', 'sample_client')
            sample_client = subprocess.Popen([sample_client_path])
            self.output.info('Running sample client')
            time.sleep(3)
            try:
                response = requests.get('127.0.0.1:9091')
            finally:
                sample_client.kill()
                assert(response.ok)
                assert(-1 != response.text.find('How many seconds is this server running?'))
