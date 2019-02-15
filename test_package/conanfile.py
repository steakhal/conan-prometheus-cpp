#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, time, subprocess, requests
from conans import ConanFile, CMake, tools


class PrometheuscppTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        assert os.path.exists(os.path.join(self.deps_cpp_info["prometheus-cpp"].rootpath, "licenses", "LICENSE"))
        if tools.cross_building(self.settings):
            self.output.warn("Cross Building: Skipping Test Package")
            return

        if not self.options["prometheus-cpp"].enable_pull:
            self.output.warn("Enable Pull disabled: Skipping Test Package")
            return

        sample_server_path = os.path.join("bin", 'sample_server')
        sample_server = subprocess.Popen([sample_server_path])
        self.output.info("Running sample server")
        time.sleep(3)
        try:
            response = requests.get("http://localhost:8080/metrics")
        finally:
            sample_server.kill()
            assert response.ok

