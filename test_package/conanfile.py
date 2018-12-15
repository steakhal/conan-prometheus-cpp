#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, time, subprocess
from conans import ConanFile, CMake, tools


class PrometheuscppTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")
        self.copy('*.so*', dst='bin', src='lib')

    def test(self):
        assert os.path.exists(os.path.join(self.deps_cpp_info["prometheus-cpp"].rootpath, "licenses", "LICENSE"))
        if tools.cross_building(self.settings):
            return

        assert(self.options["enable_pull"]) # must be enabled for testing 'sample_server'

        # TODO: cleanup this mess :D
        os.chdir("bin")
        sample_server_path = os.path.join(os.getcwd(), 'sample_server')
        sample_server = subprocess.Popen([sample_server_path])
        time.sleep(1)
        curl = subprocess.Popen("curl -s http://localhost:8080/metrics", shell=True, stdout=subprocess.PIPE)
        curl.wait()
        sample_server.kill()
        
        assert(curl.returncode == 0)

