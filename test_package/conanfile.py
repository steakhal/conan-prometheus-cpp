#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, time, subprocess, requests
from conans import ConanFile, CMake, tools


class PrometheuscppTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)

        if self.options["prometheus-cpp"].enable_pull:
            cmake.definitions['TEST_PROMETHEUS_PULL'] = True
        if self.options["prometheus-cpp"].enable_push:
            cmake.definitions['TEST_PROMETHEUS_PUSH'] = True

        cmake.configure()
        cmake.build()

    def test_pull(self):
        sample_server_path = os.path.join("bin", "test-pull", 'sample_server')
        sample_server = subprocess.Popen([sample_server_path])
        self.output.info("Running sample server")
        time.sleep(3)
        try:
            response = requests.get("http://localhost:8080/metrics")
        finally:
            sample_server.kill()
            assert(response.ok)

    def test_push(self):
        # check whether sample_client is working ...
        sample_client_path = os.path.join("bin", "test-push", 'sample_client')
        sample_client = subprocess.Popen([sample_client_path])
        self.output.info("Running sample client")
        time.sleep(3)
        try:
            response = requests.get("http://localhost:8080/metrics")
        finally:
            sample_client.kill()
            assert(response.ok)

    def test(self):
        assert(os.path.exists(os.path.join(self.deps_cpp_info["prometheus-cpp"].rootpath, "licenses", "LICENSE")))
        if tools.cross_building(self.settings):
            self.output.warn("Cross Building: Skipping Test Package")
            return

        pull = self.options["prometheus-cpp"].enable_pull
        push = self.options["prometheus-cpp"].enable_push

        if not pull and not push:
            self.output.warn("Enable Pull and Push are disabled: Skipping Test Package")
            return

        if pull:
            test_pull(self)
        if push:
            test_push(self)

        

