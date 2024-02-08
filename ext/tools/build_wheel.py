"""
This script is used with bazel, dont use it directly
"""

import argparse
import tempfile
import pathlib
import shutil
import functools
import subprocess
import sys
import logging

from bazel_tools.tools.python.runfiles import runfiles

logger = logging.getLogger(__file__)

parser = argparse.ArgumentParser()
parser.add_argument(
    "--sources_path",
    default=None,
    help="Path in which the wheel's sources should be prepared. Optional. If "
    "omitted, a temporary directory will be used.",
)
parser.add_argument(
    "--output_path",
    default=None,
    required=True,
    help="Path to which the output wheel should be written. Required.",
)
args = parser.parse_args()

r = runfiles.Create()


def copy_files(
    runfiles,
    src_filepaths: str | list[str],
    dst_dir: pathlib.Path,
    dst_filename: str | None = None,
) -> None:
    dst_dir.mkdir(parents=True, exist_ok=True)
    if isinstance(src_filepaths, str):
        src_filepaths = [src_filepaths]

    for src_filepath in src_filepaths:
        src_file_rloc = runfiles.Rlocation(src_filepath)
        if src_file_rloc is None:
            raise ValueError(f"Unable to find wheel source file {src_filepath}")
        dst_filepath = (
            dst_dir
            / f"{dst_filename if dst_filename else pathlib.Path(src_file_rloc).name}"
        )

        shutil.copy(src_file_rloc, dst_filepath)


def prepare_wheel(sources_path: pathlib.Path | str) -> None:
    if isinstance(sources_path, str):
        sources_path = pathlib.Path(sources_path)

    copy_runfiles = functools.partial(copy_files, runfiles=r)

    # ? ROOT DIR
    copy_runfiles(
        src_filepaths=[
            "__main__/ext/tools/LICENSE.txt",
            "__main__/ext/tools/README.md",
            "__main__/ext/tools/pyproject.toml",
        ],
        dst_dir=sources_path,
    )

    # ? EXT dir
    sources_path = sources_path / "ext"
    copy_runfiles(src_filepaths="__main__/ext/ext.so", dst_dir=sources_path)
    # TODO NEED to pass the __init__.py
    return None


def build_wheel(
    sources_path: pathlib.Path, out_path: pathlib.Path, package_name: str
) -> None:
    try:
        subprocess.run(
            [sys.executable, "-m", "build", "-n", "-w"], check=True, cwd=sources_path
        )
    except Exception as e:
        print(e)

    for wheel in sources_path.glob("dist/*.whl"):
        output_file = out_path / wheel.name
        sys.stderr.write(f"Output wheel: {output_file}\n\n")
        sys.stderr.write(f"To install the newly-built {package_name} wheel, run:\n")
        sys.stderr.write(f"  pip install {output_file} --force-reinstall\n\n")
        shutil.copy(wheel, out_path)
    return None


def build_editable(
    sources_path: pathlib.Path, out_path: pathlib.Path, package_name: str
) -> None:
    sys.stderr.write(
        f"To install the editable {package_name} build, run:\n\n"
        f"  pip install -e {out_path}\n\n"
    )
    shutil.rmtree(out_path, ignore_errors=True)
    shutil.copytree(sources_path, out_path)


tmp_dir = None

if args.sources_path is None:
    tmp_dir = tempfile.TemporaryDirectory(prefix="ext")
    sources_path = pathlib.Path(tmp_dir.name)
else:
    sources_path = pathlib.Path(args.sources_path)

try:
    out_path = pathlib.Path(args.output_path)
    out_path.mkdir(parents=True, exist_ok=True)
    prepare_wheel(sources_path)
    package_name = "ext"
    build_wheel(sources_path, out_path, package_name)
finally:
    if tmp_dir:
        tmp_dir.cleanup()
