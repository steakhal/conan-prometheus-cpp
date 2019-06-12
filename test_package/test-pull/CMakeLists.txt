add_executable(sample_server
  sample_server.cc
)

set_target_properties(sample_server
  PROPERTIES
    CXX_STANDARD 11
)

target_link_libraries(sample_server
  PRIVATE
    CONAN_PKG::prometheus-cpp
)
