#!/usr/bin/env python3
"""
MedVeCam Ultra 2.0 Setup Script
Automated installation and configuration
"""

import sys
import subprocess
import platform
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    return True

def detect_platform():
    """Detect platform and hardware"""
    system = platform.system()
    machine = platform.machine()
    
    is_raspberry_pi = False
    try:
        with open('/proc/cpuinfo', 'r') as f:
            cpuinfo = f.read()
            if 'Raspberry Pi' in cpuinfo or 'BCM' in cpuinfo:
                is_raspberry_pi = True
    except FileNotFoundError:
        pass
    
    return {
        'system': system,
        'machine': machine,
        'is_raspberry_pi': is_raspberry_pi
    }

def install_requirements(platform_info):
    """Install required packages based on platform"""
    print("Installing required packages...")
    
    # Install basic requirements
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✓ Basic requirements installed")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install basic requirements: {e}")
        return False
    
    # Install platform-specific packages
    if platform_info['is_raspberry_pi']:
        print("Detected Raspberry Pi - installing camera support...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "picamera2"
            ])
            print("✓ Raspberry Pi camera support installed")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install picamera2: {e}")
            print("You may need to install it manually with: sudo apt install python3-picamera2")
    
    return True

def setup_directories():
    """Create necessary directories"""
    directories = [
        Path.home() / "MedVeCam_Recordings",
        Path.home() / "MedVeCam_Logs",
        Path.home() / "MedVeCam_Presets"
    ]
    
    for directory in directories:
        directory.mkdir(exist_ok=True)
        print(f"✓ Created directory: {directory}")

def create_desktop_shortcut(platform_info):
    """Create desktop shortcut if possible"""
    if platform_info['system'] == 'Linux':
        desktop_path = Path.home() / "Desktop"
        if desktop_path.exists():
            shortcut_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=MedVeCam Ultra 2.0
Comment=Advanced Medical Camera System
Exec=python3 {Path.cwd() / 'medvecam_ultra.py'}
Icon={Path.cwd() / 'icon.png'}
Terminal=false
Categories=Graphics;Photography;Medical;
"""
            shortcut_path = desktop_path / "MedVeCam_Ultra.desktop"
            try:
                with open(shortcut_path, 'w') as f:
                    f.write(shortcut_content)
                os.chmod(shortcut_path, 0o755)
                print(f"✓ Desktop shortcut created: {shortcut_path}")
            except Exception as e:
                print(f"✗ Could not create desktop shortcut: {e}")

def test_installation():
    """Test if installation is working"""
    print("\nTesting installation...")
    
    try:
        # Test imports
        import cv2
        import numpy as np
        from PIL import Image
        print("✓ Core dependencies working")
        
        # Test camera detection
        camera = cv2.VideoCapture(0)
        if camera.isOpened():
            print("✓ Camera detected")
            camera.release()
        else:
            print("! No camera detected (this is normal if no camera is connected)")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import test failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False

def optimize_for_platform(platform_info):
    """Create optimized configuration for platform"""
    try:
        from config import MedVeCamConfig
        
        config = MedVeCamConfig()
        
        if platform_info['is_raspberry_pi']:
            config.optimize_for_raspberry_pi()
            print("✓ Configuration optimized for Raspberry Pi")
        else:
            config.optimize_for_desktop()
            print("✓ Configuration optimized for desktop")
            
        config.save_config()
        
    except Exception as e:
        print(f"✗ Could not optimize configuration: {e}")

def main():
    """Main setup function"""
    print("=" * 50)
    print("MedVeCam Ultra 2.0 Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Detect platform
    platform_info = detect_platform()
    print(f"Platform: {platform_info['system']} ({platform_info['machine']})")
    if platform_info['is_raspberry_pi']:
        print("Raspberry Pi detected")
    
    # Install requirements
    if not install_requirements(platform_info):
        print("Setup failed during package installation")
        sys.exit(1)
    
    # Setup directories
    setup_directories()
    
    # Create desktop shortcut
    create_desktop_shortcut(platform_info)
    
    # Test installation
    if not test_installation():
        print("Setup completed with warnings - some features may not work")
    else:
        print("✓ Installation test passed")
    
    # Optimize configuration
    optimize_for_platform(platform_info)
    
    print("\n" + "=" * 50)
    print("Setup Complete!")
    print("=" * 50)
    print("To start MedVeCam Ultra 2.0, run:")
    print("python3 medvecam_ultra.py")
    print("\nFor help and documentation, see README.md")
    print("=" * 50)

if __name__ == "__main__":
    main()