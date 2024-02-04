"""
nanor bind loading and building it
"""
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

def repo():
    http_archive(
        name = "nanobind",
        strip_prefix = "nanobind-1.5.2",
        sha256 = "2574b91ba15d6160cbc819eb72da3c885601b0468e0d9eda83fc14d3be996113",
        urls = ["https://github.com/wjakob/nanobind/archive/refs/tags/v1.5.2.tar.gz"],
        build_file = "//third_party/nanobind:BUILD.bazel",
    )