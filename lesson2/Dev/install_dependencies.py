#!/usr/bin/env python3
"""
Installation script for USB Keyboard Host dependencies
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a Python package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install {package}: {e}")
        return False

def check_package(package):
    """Check if a package is already installed"""
    try:
        __import__(package)
        print(f"✓ {package} is already installed")
        return True
    except ImportError:
        print(f"✗ {package} is not installed")
        return False

def main():
    """Main installation function"""
    print("USB Keyboard Host - Dependency Installer")
    print("=" * 40)
    
    # Required packages
    packages = {
        'usb': 'pyusb>=1.2.1',
        'usb.core': 'pyusb>=1.2.1'
    }
    
    print("Checking dependencies...")
    
    # Check if packages are already installed
    all_installed = True
    for package, pip_name in packages.items():
        if not check_package(package):
            all_installed = False
    
    if all_installed:
        print("\n✓ All dependencies are already installed!")
        return
    
    print("\nInstalling missing dependencies...")
    
    # Install missing packages
    success = True
    for package, pip_name in packages.items():
        if not check_package(package):
            if not install_package(pip_name):
                success = False
    
    if success:
        print("\n✓ All dependencies installed successfully!")
        print("\nYou can now run the USB keyboard host application.")
    else:
        print("\n✗ Some dependencies failed to install.")
        print("Please install them manually:")
        print("pip install pyusb>=1.2.1")
    
    # Platform-specific notes
    print("\nPlatform-specific notes:")
    if os.name == 'nt':  # Windows
        print("- Windows: You may need to install libusb drivers")
        print("- Download from: https://libusb.info/")
        print("- Or install via: pip install libusb1")
    elif os.name == 'posix':  # Linux/Unix
        print("- Linux: You may need to run with sudo or add udev rules")
        print("- Ubuntu/Debian: sudo apt-get install python3-usb")
    else:
        print("- Please check your platform's USB library requirements")

if __name__ == "__main__":
    main()

