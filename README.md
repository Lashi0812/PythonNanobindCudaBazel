- [Extend Python with nanobind and cuda](#extend-python-with-nanobind-and-cuda)
  - [nvcc fatal   : No input files specified](#nvcc-fatal----no-input-files-specified)
  - [Missing -G flag in tsl (Tensor Standard library)](#missing--g-flag-in-tsl-tensor-standard-library)
    - [Generate a Git Diff](#generate-a-git-diff)
    - [Use patch file in bazel](#use-patch-file-in-bazel)
  - [Alternative way to add nvcc\_flags such -G](#alternative-way-to-add-nvcc_flags-such--g)
  - [Debugging Python ,C++,Cuda](#debugging-python-ccuda)
    - [CUDA C++: Attach](#cuda-c-attach)
    - [Python: Current File](#python-current-file)
  - [Building and Installing a Python Package with Bazel](#building-and-installing-a-python-package-with-bazel)
    - [1. Building the Script and Copying Shared Libraries](#1-building-the-script-and-copying-shared-libraries)
    - [2. Building the Wheel](#2-building-the-wheel)
    - [3. Installing the Wheel](#3-installing-the-wheel)

# Extend Python with nanobind and cuda

## nvcc fatal   : No input files specified

xla cross tool search source file with only have extension

```python
  src_files = [f for f in src_files if
               re.search('\.cpp$|\.cc$|\.c$|\.cxx$|\.C$', f)]
```

in this list there is no .cu that the reason `no input files specified error`

## Missing -G flag in tsl (Tensor Standard library)

In tsl they used the template for generating the cross compiler executable `external/local_config_cuda/crosstool/clang/bin/crosstool_wrapper_driver_is_not_gcc` in file they generate the command for nvcc

### Generate a Git Diff

Use Git diff for the changes generate patch:

```bash
# this command done in xla project repo
git diff source_branch target_branch  > my_patch.diff
```

### Use patch file in bazel

Once we generated the command , we specify the patch file in `http_archive`, this will apply patch while extracting the repo .

```python
# third_party/xla/workspace.bzl
 patch_file = [
            "//third_party/xla:tsl.patch"
        ]
```

## Alternative way to add nvcc_flags such -G

Instead of using patch we can use `-nvcc_options` flag to specify the nvcc options.

```python
# these LOC from local_config_cuda/crosstool/clang/bin/crosstool_wrapper_driver_is_not_gcc file
nvcc_compiler_options = GetNvccOptions(argv)
parser.add_argument('-nvcc_options', nargs='*', action='append')
' '.join(['--'+a for a in options])
```

we need pass `long-form name` after the `-nvcc_options`

```python
copts = [
        "-fexceptions",
        "-fno-strict-aliasing",
        "-nvcc_options","device-debug"
    ]
```

## Debugging Python ,C++,Cuda  

Create Configuration for both python and cuda Attach . first launch the python debugger and then attach the running process pid to to Cuda attach

### CUDA C++: Attach

```json
# Refer launch.json for paths
    {
      "name": "CUDA C++: Attach",
      "type": "cuda-gdb",
      "request": "attach",
      "debuggerPath": "/usr/local/cuda-12.1/bin/cuda-gdb",
      "processId": "${command:cuda.pickProcess}",
      "initCommands": [
        "directory ...",
        "set solib-search-path ...",
        "set substitute-path old_path crt_path"
        "set breakpoint pending on",
        "break ext.cu.cc:12",
      ],
    }
```

- **initCommands**:
  - `directory ...`: Sets the source directory for the CUDA GDB session.
  - `set solib-search-path ...`: Sets the path for the shared library.
  - `set substitute-path old_path crt_path`: Specifies path substitution for source files.
  - `set breakpoint pending on`: Enables pending breakpoints.
  - `break ext.cu.cc:12`: Sets a breakpoint at line 12 of the `ext.cu.cc` file.
  - you place break point in IDE itself.

### Python: Current File

```json
{
      "name": "Python: Current File",
      "type": "debugpy",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "env": {
        "PYTHONPATH": "${workspaceFolder}/bazel-bin/test.runfiles/__main__"
      },
     
    }
```

- Sets the `PYTHONPATH` environment variable to include the specified path.


## Building and Installing a Python Package with Bazel

This document outlines the process of creating and installing a Python package using Bazel, a popular build and automation tool. We'll focus on including shared libraries within the package.

### 1. Building the Script and Copying Shared Libraries

1. **Shared Library Target:** Define a target in your `BUILD` file to build your shared library using the appropriate Bazel rules (e.g., `cc_binary` for C++ libraries).
```bazel
pybind_extension(
    name = "ext",
    srcs = ["ext.cu.cc"],
    ...)
```
2. **Build Script (`build_wheel.py`):**
    - Create a `build_wheel.py` script that performs the following:
        - **Access Shared Library:** Use the `runfiles` module to access the location of the built shared library from the target you defined in step 1.
        - **Copy Library:** Copy the shared library to the designated package directory.
        - **Prepare Other Files:** Copy other necessary files like modules, scripts, `LICENSE`, `README`, and `pyproject.toml` to the package directory.
3. **Bazel Target for Script:** Define a `py_binary` target in your `BUILD` file for `build_wheel.py`. This target depends on the shared library target (`deps`).
```bazel
py_binary(
    name = "build_wheel",
    srcs = ["build_wheel.py"],
    data = [
        "LICENSE.txt",
        "README.md",
        "pyproject.toml",
        "//ext",
    ],
    deps = [
        "@bazel_tools//tools/python/runfiles",
    ],
)
```

### 2. Building the Wheel

1. **Setuptools Integration:** Configure your project to use `setuptools` as the backend build system in `pyproject.toml`.
2. **Wheel Building Command:** After executing the script, use the following command to build the wheel:

```
python -m build -n -w
```

This command creates the wheel in the `dist` directory.

### 3. Installing the Wheel

```
pip install dist/your_package-version-py3-none-any.whl
```
