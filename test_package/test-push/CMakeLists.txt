add_executable(sample_client
  sample_client.cc
)

set_target_properties(sample_client
  PROPERTIES
    CXX_STANDARD 11
)

target_link_libraries(sample_client
  PRIVATE
    CONAN_PKG::libcurl CONAN_PKG::prometheus-cpp
)
