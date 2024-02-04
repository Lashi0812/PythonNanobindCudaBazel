"""
XLA Workspace
"""

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

XLA_COMMIT = "492c50766d96ecce2e57447d12c34feaa4acacaf"
XLA_SHA256 = "1afe2995fa06347fdf33766e8682b7da1275ec0e4120cbe42e32190a4e06c7d1"

def repo():
    http_archive(
        name = "xla",
        urls = ["https://github.com/openxla/xla/archive/{commit}.tar.gz".format(commit = XLA_COMMIT)],
        strip_prefix = "xla-{commit}".format(commit = XLA_COMMIT),
        sha256 = XLA_SHA256,
    )
