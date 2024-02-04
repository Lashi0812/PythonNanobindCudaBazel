"""Robin map for nanobind dependency"""

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

def repo():
    http_archive(
        name = "robin_map",
        strip_prefix = "robin-map-1.2.1",
        sha256 = "2b54d2c1de2f73bea5c51d5dcbd64813a08caf1bfddcfdeee40ab74e9599e8e3",
        urls = ["https://github.com/Tessil/robin-map/archive/refs/tags/v1.2.1.tar.gz"],
        build_file = "//third_party/robin_map:BUILD.bazel",
    )
