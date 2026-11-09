#include <metal_stdlib>
using namespace metal;

kernel void matmul_kernel(device const float* A [[buffer(0)]],
                          device const float* B [[buffer(1)]],
                          device float* C [[buffer(2)]],
                          constant uint& M [[buffer(3)]],
                          constant uint& N [[buffer(4)]],
                          constant uint& K [[buffer(5)]],
                          uint2 gid [[thread_position_in_grid]]) {
    
    // Simple naive matrix multiplication for stability first
    // C[row, col] = dot(A[row, :], B[:, col])
    
    uint row = gid.y;
    uint col = gid.x;
    
    if (row < M && col < N) {
        float sum = 0.0f;
        for (uint i = 0; i < K; i++) {
            sum += A[row * K + i] * B[i * N + col];
        }
        C[row * N + col] = sum;
    }
}
