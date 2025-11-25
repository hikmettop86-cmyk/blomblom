#!/usr/bin/env python3
"""Test PyTorch CUDA installation"""

print("=" * 60)
print("PyTorch CUDA Test")
print("=" * 60)

try:
    import torch
    print(f"\n✅ PyTorch kurulu: {torch.__version__}")

    # CUDA availability
    cuda_available = torch.cuda.is_available()
    print(f"\n🔍 CUDA Available: {cuda_available}")

    if cuda_available:
        print(f"   ✅ CUDA Version: {torch.version.cuda}")
        print(f"   ✅ GPU Count: {torch.cuda.device_count()}")
        print(f"   ✅ GPU Name: {torch.cuda.get_device_name(0)}")
        print(f"   ✅ Current Device: {torch.cuda.current_device()}")

        # Test tensor on GPU
        try:
            x = torch.randn(3, 3).cuda()
            print(f"   ✅ GPU tensor test: SUCCESS")
            print(f"   ✅ Tensor device: {x.device}")
        except Exception as e:
            print(f"   ❌ GPU tensor test FAILED: {e}")
    else:
        print(f"\n❌ CUDA NOT AVAILABLE!")
        print(f"\n🔍 Possible reasons:")
        print(f"   1. PyTorch CPU-only version installed")
        print(f"   2. NVIDIA driver not installed/outdated")
        print(f"   3. CUDA toolkit not installed")
        print(f"   4. Wrong PyTorch version for your CUDA")

        print(f"\n💡 Solution:")
        print(f"   1. Uninstall current PyTorch:")
        print(f"      pip uninstall torch torchvision torchaudio")
        print(f"   2. Install CUDA version:")
        print(f"      pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121")
        print(f"   3. Restart terminal/IDE")

except ImportError:
    print(f"\n❌ PyTorch not installed!")
    print(f"\n💡 Install with:")
    print(f"   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121")

print("\n" + "=" * 60)
