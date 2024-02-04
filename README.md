# Extend Python with nanobind and cuda

## nvcc fatal   : No input files specified

xla cross tool search source file with only have extension
```python
  src_files = [f for f in src_files if
               re.search('\.cpp$|\.cc$|\.c$|\.cxx$|\.C$', f)]
```
in this list there is no .cu that the reason `no input files specified error`