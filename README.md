- [Extend Python with nanobind and cuda](#extend-python-with-nanobind-and-cuda)
  - [nvcc fatal   : No input files specified](#nvcc-fatal----no-input-files-specified)
  - [Missing -G flag in tsl (Tensor Standard library)](#missing--g-flag-in-tsl-tensor-standard-library)
    - [Generate a Git Diff](#generate-a-git-diff)
    - [Use patch file in bazel](#use-patch-file-in-bazel)
  - [Alternative way to add nvcc\_flags such -G](#alternative-way-to-add-nvcc_flags-such--g)
  - [Debugging python ,C++,Cuda](#debugging-python-ccuda)
    - [CUDA C++: Attach](#cuda-c-attach)
    - [Python: Current File](#python-current-file)

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

## Debugging python ,C++,Cuda  

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
