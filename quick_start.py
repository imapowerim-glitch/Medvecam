#!/usr/bin/env python3
"""
MedVeCam Ultra 2.0 Quick Start Example
Demonstrates basic usage without GUI for testing
"""

import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Quick start demonstration"""
    print("=" * 60)
    print("MedVeCam Ultra 2.0 - Quick Start Demo")
    print("=" * 60)
    
    try:
        # Test configuration
        print("\n1. Loading Configuration...")
        from config import MedVeCamConfig
        
        config = MedVeCamConfig()
        print(f"   ✓ Video Resolution: {config.video.resolution}")
        print(f"   ✓ Bitrate: {config.video.bitrate // 1000000} Mbps")
        print(f"   ✓ H264 Profile: {config.video.h264_profile}")
        
        # Test medical presets
        print("\n2. Loading Medical Presets...")
        from medical_presets import MedicalPresets
        
        presets = MedicalPresets()
        print(f"   ✓ Available Presets: {len(presets.get_preset_names())}")
        
        # Show some presets
        key_presets = ["Surgery", "Dermatology", "Endoscopy"]
        for preset_name in key_presets:
            preset = presets.get_preset(preset_name)
            print(f"   ✓ {preset_name}: {preset.description}")
        
        # Test video processor
        print("\n3. Testing Video Processor...")
        from video_processor import VideoProcessor
        
        processor = VideoProcessor()
        processor.update_settings({
            "gamma": 1.2,
            "brightness": 10,
            "contrast": 1.1
        })
        print("   ✓ Video processor configured")
        print(f"   ✓ Current settings: {processor.get_processing_info()}")
        
        # Test camera handler configuration (without actual camera)
        print("\n4. Camera Handler Configuration...")
        from camera_handler import CameraHandler
        
        # This will fail without a camera, but we can test the configuration
        try:
            handler = CameraHandler(config)
            print("   ✓ Camera handler created")
        except Exception as e:
            print(f"   ! Camera handler: {e} (expected without camera)")
        
        print("\n" + "=" * 60)
        print("✓ MedVeCam Ultra 2.0 Core System Ready!")
        print("=" * 60)
        
        print("\nTo start the full GUI application:")
        print("   python medvecam_ultra.py")
        
        print("\nTo run setup and optimization:")
        print("   python setup.py")
        
        print("\nFor full documentation:")
        print("   See README.md")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import Error: {e}")
        print("\nPlease install dependencies first:")
        print("   pip install -r requirements.txt")
        return False
        
    except Exception as e:
        print(f"✗ Unexpected Error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        print("\nQuick start demo failed. Please check the installation.")
        sys.exit(1)
    else:
        print("\n🎉 Quick start demo completed successfully!")
        sys.exit(0)