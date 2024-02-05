#include "nanobind/nanobind.h"

namespace nb = nanobind;
using namespace nb::literals;

int cpu_add(int a, int b = 1) {
    int c = a+ b;
     return c;     
     }

__global__ void add_kernel(const int *a, const int *b, int *c) { 
    int e,g,t;
    e = 10;
    g = 3;
    t = e+g;
    c[0] = a[0] + b[0]; 
    }

int gpu_add(int a, int b) {
    int  c;
    int *d_a, *d_b, *d_c;
    cudaMalloc((void **)&d_a, sizeof(a));
    cudaMalloc((void **)&d_b, sizeof(b));
    cudaMalloc((void **)&d_c, sizeof(c));
    cudaMemcpy(d_a, &a, sizeof(a), cudaMemcpyHostToDevice);
    cudaMemcpy(d_b, &b, sizeof(b), cudaMemcpyHostToDevice);
    add_kernel<<<1, 1>>>(d_a, d_b, d_c);
    cudaMemcpy(&c, d_c, sizeof(c), cudaMemcpyDeviceToHost);
    cudaFree(d_a);
    cudaFree(d_b);
    cudaFree(d_c);
    return c;
}

NB_MODULE(ext, m) {
    m.def("cpu_add", &cpu_add, "a"_a, "b"_a = 1);
    m.def("gpu_add", &gpu_add, "a"_a, "b"_a );
}