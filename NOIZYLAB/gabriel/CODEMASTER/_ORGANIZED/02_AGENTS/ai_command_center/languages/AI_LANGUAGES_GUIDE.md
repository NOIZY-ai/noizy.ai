# 💻 AI/LLM PROGRAMMING LANGUAGES MASTERY GUIDE

> **Complete guide to every language used in AI development**

---

## 🏆 TIER 1: ESSENTIAL (Learn These First)

### Python 🐍
**The foundation of AI/ML**

```python
# PyTorch example
import torch
import torch.nn as nn

class TransformerBlock(nn.Module):
    def __init__(self, d_model, nhead):
        super().__init__()
        self.attn = nn.MultiheadAttention(d_model, nhead)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_model * 4),
            nn.GELU(),
            nn.Linear(d_model * 4, d_model)
        )
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
    
    def forward(self, x):
        x = x + self.attn(self.norm1(x), self.norm1(x), self.norm1(x))[0]
        x = x + self.ffn(self.norm2(x))
        return x
```

**Key Libraries:**
| Library | Purpose |
|---------|---------|
| PyTorch | Deep learning, research |
| TensorFlow | Production ML |
| JAX | Functional, TPU-optimized |
| HuggingFace | Pre-trained models |
| LangChain | LLM applications |
| vLLM | Fast LLM serving |

---

### CUDA 🔥
**GPU programming for maximum performance**

```cuda
// Matrix multiplication kernel
__global__ void matmul(float *A, float *B, float *C, int N) {
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;
    
    if (row < N && col < N) {
        float sum = 0.0f;
        for (int k = 0; k < N; k++) {
            sum += A[row * N + k] * B[k * N + col];
        }
        C[row * N + col] = sum;
    }
}

// Flash Attention pattern
__global__ void flash_attention_kernel(
    float *Q, float *K, float *V, float *O,
    int seq_len, int head_dim
) {
    // Tiled attention with shared memory
    __shared__ float Q_tile[TILE_SIZE][HEAD_DIM];
    __shared__ float K_tile[TILE_SIZE][HEAD_DIM];
    // ... implementation
}
```

**When to use CUDA:**
- Custom attention mechanisms
- Quantization kernels
- Fused operations
- Maximum inference speed

---

### Triton ⚡
**OpenAI's GPU programming language (easier than CUDA)**

```python
import triton
import triton.language as tl

@triton.jit
def fused_attention_kernel(
    Q, K, V, Out,
    stride_qm, stride_qk,
    stride_km, stride_kn,
    stride_vm, stride_vn,
    stride_om, stride_on,
    N_CTX,
    BLOCK_M: tl.constexpr,
    BLOCK_N: tl.constexpr,
    BLOCK_K: tl.constexpr,
):
    start_m = tl.program_id(0)
    offs_m = start_m * BLOCK_M + tl.arange(0, BLOCK_M)
    offs_n = tl.arange(0, BLOCK_N)
    offs_k = tl.arange(0, BLOCK_K)
    
    # Load Q tile
    q = tl.load(Q + offs_m[:, None] * stride_qm + offs_k[None, :] * stride_qk)
    
    # Compute attention
    acc = tl.zeros([BLOCK_M, BLOCK_N], dtype=tl.float32)
    for start_n in range(0, N_CTX, BLOCK_N):
        k = tl.load(K + offs_n[None, :] * stride_km + offs_k[:, None] * stride_kn)
        qk = tl.dot(q, k)
        acc += qk
    
    tl.store(Out + offs_m[:, None] * stride_om + offs_n[None, :] * stride_on, acc)
```

**Triton vs CUDA:**
| Aspect | Triton | CUDA |
|--------|--------|------|
| Learning curve | 2 weeks | 3 months |
| Performance | 90-95% of CUDA | 100% |
| Debugging | Better | Harder |
| Portability | Multi-GPU | NVIDIA only |

---

## 🏆 TIER 2: PRODUCTION & PERFORMANCE

### Rust 🦀
**For production inference engines**

```rust
use candle_core::{Device, Tensor, DType};
use candle_nn::{Linear, Module, VarBuilder};

struct TransformerLayer {
    attn: MultiHeadAttention,
    ffn: FeedForward,
    ln1: LayerNorm,
    ln2: LayerNorm,
}

impl TransformerLayer {
    fn forward(&self, x: &Tensor) -> Result<Tensor> {
        let residual = x;
        let x = self.ln1.forward(x)?;
        let x = self.attn.forward(&x)?;
        let x = (residual + x)?;
        
        let residual = &x;
        let x = self.ln2.forward(&x)?;
        let x = self.ffn.forward(&x)?;
        residual + x
    }
}

// Inference server
async fn inference_handler(
    State(model): State<Arc<Model>>,
    Json(request): Json<InferenceRequest>,
) -> Json<InferenceResponse> {
    let tokens = model.tokenize(&request.prompt);
    let output = model.generate(tokens, request.max_tokens).await;
    Json(InferenceResponse { text: output })
}
```

**Rust AI Frameworks:**
| Crate | Purpose |
|-------|---------|
| `candle` | HuggingFace's Rust ML |
| `burn` | Deep learning framework |
| `tch-rs` | PyTorch bindings |
| `tokenizers` | Fast tokenization |
| `safetensors` | Model weights format |

---

### Mojo 🔥
**Python syntax, C performance**

```mojo
from tensor import Tensor
from algorithm import vectorize, parallelize

struct TransformerBlock:
    var weights: Tensor[DType.float32]
    var dim: Int
    
    fn __init__(inout self, dim: Int):
        self.dim = dim
        self.weights = Tensor[DType.float32](dim, dim)
    
    fn forward(self, x: Tensor[DType.float32]) -> Tensor[DType.float32]:
        # Vectorized matrix multiply
        var result = Tensor[DType.float32](x.shape())
        
        @parameter
        fn compute_row(i: Int):
            @parameter
            fn dot_product[simd_width: Int](j: Int):
                var sum = SIMD[DType.float32, simd_width](0)
                for k in range(self.dim):
                    sum += x.load[simd_width](i, k) * self.weights.load[simd_width](k, j)
                result.store[simd_width](i, j, sum)
            vectorize[dot_product, 8](self.dim)
        
        parallelize[compute_row](x.shape()[0])
        return result
```

**Mojo Benefits:**
- 35,000x faster than Python for some operations
- Python-compatible syntax
- SIMD and parallelization built-in
- Memory safety

---

### C++ ⚙️
**For llama.cpp and low-level inference**

```cpp
#include "llama.h"

class LlamaInference {
private:
    llama_model* model;
    llama_context* ctx;
    
public:
    LlamaInference(const std::string& model_path) {
        llama_backend_init();
        
        auto params = llama_model_default_params();
        params.n_gpu_layers = 99;  // Offload all to GPU
        
        model = llama_load_model_from_file(model_path.c_str(), params);
        
        auto ctx_params = llama_context_default_params();
        ctx_params.n_ctx = 4096;
        ctx_params.n_batch = 512;
        
        ctx = llama_new_context_with_model(model, ctx_params);
    }
    
    std::string generate(const std::string& prompt, int max_tokens) {
        auto tokens = llama_tokenize(ctx, prompt, true);
        
        llama_batch batch = llama_batch_init(512, 0, 1);
        for (size_t i = 0; i < tokens.size(); i++) {
            llama_batch_add(batch, tokens[i], i, {0}, false);
        }
        batch.logits[batch.n_tokens - 1] = true;
        
        llama_decode(ctx, batch);
        
        std::string result;
        for (int i = 0; i < max_tokens; i++) {
            auto logits = llama_get_logits(ctx);
            auto next_token = sample_token(logits);
            result += llama_token_to_piece(ctx, next_token);
            
            llama_batch_clear(batch);
            llama_batch_add(batch, next_token, tokens.size() + i, {0}, true);
            llama_decode(ctx, batch);
        }
        
        return result;
    }
};
```

---

## 🏆 TIER 3: SPECIALIZED

### JAX (Python + XLA)
**Functional ML, Google's choice**

```python
import jax
import jax.numpy as jnp
from flax import linen as nn

class Attention(nn.Module):
    num_heads: int
    head_dim: int
    
    @nn.compact
    def __call__(self, x):
        B, L, D = x.shape
        
        qkv = nn.Dense(3 * self.num_heads * self.head_dim)(x)
        q, k, v = jnp.split(qkv, 3, axis=-1)
        
        q = q.reshape(B, L, self.num_heads, self.head_dim)
        k = k.reshape(B, L, self.num_heads, self.head_dim)
        v = v.reshape(B, L, self.num_heads, self.head_dim)
        
        # Flash attention style
        attn = jnp.einsum('blhd,bmhd->bhlm', q, k) / jnp.sqrt(self.head_dim)
        attn = jax.nn.softmax(attn, axis=-1)
        
        out = jnp.einsum('bhlm,bmhd->blhd', attn, v)
        return out.reshape(B, L, -1)

# JIT compile for speed
@jax.jit
def forward(params, x):
    return model.apply(params, x)

# Auto-parallelize across TPUs/GPUs
@jax.pmap
def parallel_forward(params, x):
    return model.apply(params, x)
```

---

### MLIR / LLVM
**Compiler infrastructure for ML**

```mlir
// MLIR for ML operations
func.func @matmul(%A: tensor<1024x1024xf32>, 
                   %B: tensor<1024x1024xf32>) -> tensor<1024x1024xf32> {
  %C = linalg.matmul ins(%A, %B : tensor<1024x1024xf32>, tensor<1024x1024xf32>)
                      outs(%C : tensor<1024x1024xf32>) -> tensor<1024x1024xf32>
  return %C : tensor<1024x1024xf32>
}

// Tiling transformation
#map = affine_map<(d0, d1, d2) -> (d0, d2)>
#map1 = affine_map<(d0, d1, d2) -> (d2, d1)>
#map2 = affine_map<(d0, d1, d2) -> (d0, d1)>

func.func @tiled_matmul(%A: tensor<1024x1024xf32>,
                         %B: tensor<1024x1024xf32>) -> tensor<1024x1024xf32> {
  %0 = scf.forall (%i, %j) in (32, 32) shared_outs(%arg0 = %C) -> tensor<1024x1024xf32> {
    // Tile computation
  }
  return %0 : tensor<1024x1024xf32>
}
```

---

## 📚 LEARNING PATH

### Week 1-2: Python Foundations
```bash
# Setup
pip install torch transformers accelerate

# Learn
- PyTorch basics (tensors, autograd, nn.Module)
- HuggingFace transformers
- Basic fine-tuning
```

### Week 3-4: Inference Optimization
```bash
# Tools
pip install vllm bitsandbytes

# Learn
- Quantization (INT8, INT4, GPTQ, AWQ)
- KV-cache optimization
- Batching strategies
```

### Week 5-8: GPU Programming
```bash
# Setup Triton
pip install triton

# Learn
- Triton kernel basics
- Fused attention
- Custom CUDA kernels
```

### Week 9-12: Production Systems
```bash
# Learn Rust
cargo install cargo-watch

# Build
- Inference servers
- Tokenizers
- Model serving
```

---

## 🛠️ ESSENTIAL TOOLS

| Tool | Purpose | Install |
|------|---------|---------|
| **nvcc** | CUDA compiler | CUDA Toolkit |
| **nsight** | GPU profiler | CUDA Toolkit |
| **Triton** | GPU kernels | `pip install triton` |
| **vLLM** | LLM serving | `pip install vllm` |
| **llama.cpp** | CPU/GPU inference | Build from source |
| **TensorRT** | NVIDIA optimization | NVIDIA SDK |
| **ONNX** | Model interchange | `pip install onnx` |

---

*NOIZYLAB AI Languages Guide • December 2024*
