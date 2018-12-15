from conans import ConanFile, CMake, tools


class PrometheuscppConan(ConanFile):
    name = "prometheus-cpp"
    version = "0.6"
    license = "MIT"
    author = "Balazs Benics <benicsbalazs@gmail.com>"
    url = "https://github.com/steakhal/conan-prometheus-cpp"
    homepage = "https://github.com/jupp0r/prometheus-cpp"
    description = "This library aims to enable Metrics-Driven Development for C++ services. It implements the Prometheus Data Model, a powerful abstraction on which to collect and expose metrics. We offer the possibility for metrics to be collected by Prometheus, but other push/pull collections can be added as plugins."
    topics = ("metrics", "measure", "statistics", "profile", "log")
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "enable_pull": [True, False],
        "enable_push": [True, False],
        "enable_compression": [True, False],
        "override_cxx_standard_flags": [True, False]
    }
    default_options = {
        "shared": False,
        "enable_pull": True,
        "enable_push": True,
        "enable_compression": True,
        "override_cxx_standard_flags": True
    }
    generators = "cmake"
    requires = "civetweb/1.10@steakhal/stable"

    def source(self):
        git = tools.Git(folder=self.name)
        git.clone(self.homepage)

        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("prometheus-cpp/CMakeLists.txt", "project(prometheus-cpp)",
                              '''project(prometheus-cpp)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def requirements(self):
        if self.options.enable_pull:
            self.requires.add("zlib/1.2.11@conan/stable")
        if self.options.enable_push:
            self.requires.add("libcurl/7.61.1@bincrafters/stable")
            self.requires.add("OpenSSL/1.1.1a@conan/stable",  override=True)
    
    def configure_cmake(self):
        onoff = lambda b: "On" if b else "Off"
        cmake = CMake(self)
        
        cmake.definitions["BUILD_SHARED_LIBS"] = onoff(self.options.shared)
        cmake.definitions["ENABLE_PULL"] = onoff(self.options.enable_pull)
        cmake.definitions["ENABLE_PUSH"] = onoff(self.options.enable_push)
        cmake.definitions["ENABLE_COMPRESSION"] = onoff(self.options.enable_compression)
        cmake.definitions["OVERRIDE_CXX_STANDARD_FLAGS"] = onoff(self.options.override_cxx_standard_flags)
        cmake.definitions["ENABLE_TESTING"] = "Off"
        cmake.definitions["USE_THIRDPARTY_LIBRARIES"] = "Off"
        
        cmake.configure(source_folder="prometheus-cpp")
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        cmake = self.configure_cmake()
        cmake.install()
        self.copy("license*", dst="licenses",  ignore_case=True, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["prometheus-cpp-core"]
        if self.options.enable_pull:
            self.cpp_info.libs.append("prometheus-cpp-pull")
        if self.options.enable_push:
            self.cpp_info.libs.append("prometheus-cpp-push")

