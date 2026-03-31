"""
Setup Verification Script
=========================
Run this script to verify that all dependencies are correctly installed.

Usage:
    python verify_setup.py
"""

import sys


def check_python_version():
    """Check Python version."""
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("  ❌ Python 3.8 or higher is required!")
        return False
    else:
        print("  ✅ Python version OK")
        return True


def check_package(package_name, import_name=None):
    """Check if a package is installed."""
    if import_name is None:
        import_name = package_name
    
    try:
        module = __import__(import_name)
        version = getattr(module, '__version__', 'unknown')
        print(f"  ✅ {package_name}: {version}")
        return True
    except ImportError:
        print(f"  ❌ {package_name}: Not installed")
        return False


def check_cuda():
    """Check CUDA availability."""
    try:
        import torch
        if torch.cuda.is_available():
            print(f"  ✅ CUDA available: {torch.cuda.get_device_name(0)}")
            print(f"     CUDA version: {torch.version.cuda}")
            return True
        else:
            print("  ⚠️  CUDA not available (CPU mode)")
            return True
    except Exception as e:
        print(f"  ❌ Error checking CUDA: {e}")
        return False


def main():
    """Run all verification checks."""
    print("="*60)
    print("VQA BLIP Activity - Setup Verification")
    print("="*60)
    
    results = []
    
    # Check Python version
    print("\n[1] Checking Python Version...")
    results.append(check_python_version())
    
    # Check required packages
    print("\n[2] Checking Required Packages...")
    packages = [
        ("torch", "torch"),
        ("torchvision", "torchvision"),
        ("transformers", "transformers"),
        ("Pillow", "PIL"),
        ("accelerate", "accelerate"),
    ]
    
    for pkg, imp in packages:
        results.append(check_package(pkg, imp))
    
    # Check optional packages
    print("\n[3] Checking Optional Packages...")
    optional_packages = [
        ("gradio", "gradio"),
        ("jupyter", "jupyter"),
        ("numpy", "numpy"),
        ("pandas", "pandas"),
        ("tqdm", "tqdm"),
    ]
    
    for pkg, imp in optional_packages:
        check_package(pkg, imp)  # These are optional, don't add to results
    
    # Check CUDA
    print("\n[4] Checking GPU Support...")
    check_cuda()
    
    # Summary
    print("\n" + "="*60)
    if all(results):
        print("✅ All required dependencies are installed!")
        print("\nYou're ready to start the VQA activity!")
        print("\nQuick Start:")
        print("  python quick_start.py <image_path>")
        print("\nOr launch the web interface:")
        print("  python scripts/gradio_demo.py")
    else:
        print("❌ Some dependencies are missing!")
        print("\nPlease install missing packages:")
        print("  pip install -r requirements.txt")
    print("="*60)


if __name__ == "__main__":
    main()
