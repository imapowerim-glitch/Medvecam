"""
MedVeCam Ultra 2.0 Configuration Module
Advanced configuration settings for medical camera applications
"""

import json
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, Any, Tuple

@dataclass
class VideoConfig:
    """Video recording configuration"""
    # 2K recording support
    resolution: Tuple[int, int] = (2560, 1440)
    framerate: int = 30
    bitrate: int = 25000000  # 25 Mbps
    
    # H264 codec optimization
    h264_profile: str = "high"
    h264_level: str = "4.1"
    quality: int = 23  # CRF value for quality
    
    # Performance optimizations
    buffer_size: int = 1024 * 1024  # 1MB buffer
    max_threads: int = 4
    preset: str = "medium"  # encoding speed preset
    
@dataclass
class PreviewConfig:
    """Preview display configuration"""
    resolution: Tuple[int, int] = (640, 480)
    framerate: int = 30
    buffer_size: int = 3  # Reduced buffering for responsiveness
    color_format: str = "RGB888"
    
@dataclass
class CameraConfig:
    """Camera hardware configuration"""
    # Auto-detection settings
    auto_detect: bool = True
    preferred_camera: int = 0
    
    # Sensor settings
    sensor_mode: int = 2  # Optimized for 2K recording
    analogue_gain: float = 1.0
    digital_gain: float = 1.0
    
    # Auto-exposure and auto-white balance
    auto_exposure: bool = True
    exposure_time: int = 33000  # microseconds
    awb_mode: str = "auto"
    
    # Image processing
    saturation: float = 1.0
    contrast: float = 1.0
    brightness: float = 0.0
    sharpness: float = 1.0
    
@dataclass
class ColorCorrectionConfig:
    """Advanced color correction settings"""
    # Gamma correction
    gamma: float = 1.0
    gamma_curve: str = "linear"
    
    # Color matrix
    color_matrix: list = None
    
    # LUT support
    lut_enabled: bool = False
    lut_file: str = ""
    
    # White balance fine-tuning
    wb_red_gain: float = 1.0
    wb_blue_gain: float = 1.0
    
    # Color temperature
    color_temperature: int = 5500  # Kelvin
    
@dataclass
class PerformanceConfig:
    """Performance optimization settings"""
    # Threading
    use_multithreading: bool = True
    preview_threads: int = 2
    recording_threads: int = 2
    
    # Memory management
    max_memory_mb: int = 512
    frame_buffer_count: int = 6
    
    # CPU optimization
    cpu_affinity: list = None  # CPU cores to use
    priority: int = 0  # Process priority
    
    # GPU acceleration (if available)
    use_gpu: bool = False
    gpu_memory_mb: int = 128

@dataclass
class AudioConfig:
    """Audio recording configuration"""
    enabled: bool = True
    sample_rate: int = 48000
    channels: int = 2
    bitrate: int = 128000  # 128 kbps
    format: str = "AAC"

class MedVeCamConfig:
    """Main configuration class for MedVeCam Ultra 2.0"""
    
    def __init__(self, config_file: str = None):
        """Initialize configuration"""
        self.config_file = config_file or str(Path.home() / ".medvecam_config.json")
        
        # Initialize default configurations
        self.video = VideoConfig()
        self.preview = PreviewConfig()
        self.camera = CameraConfig()
        self.color_correction = ColorCorrectionConfig()
        self.performance = PerformanceConfig()
        self.audio = AudioConfig()
        
        # Application settings
        self.app_settings = {
            "version": "2.0",
            "auto_save_settings": True,
            "output_directory": str(Path.home() / "MedVeCam_Recordings"),
            "log_level": "INFO",
            "theme": "dark",
            "language": "en"
        }
        
        # Load existing configuration if available
        self.load_config()
        
    def load_config(self):
        """Load configuration from file"""
        try:
            if Path(self.config_file).exists():
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    
                # Update configurations
                if 'video' in data:
                    self.video = VideoConfig(**data['video'])
                if 'preview' in data:
                    self.preview = PreviewConfig(**data['preview'])
                if 'camera' in data:
                    self.camera = CameraConfig(**data['camera'])
                if 'color_correction' in data:
                    self.color_correction = ColorCorrectionConfig(**data['color_correction'])
                if 'performance' in data:
                    self.performance = PerformanceConfig(**data['performance'])
                if 'audio' in data:
                    self.audio = AudioConfig(**data['audio'])
                if 'app_settings' in data:
                    self.app_settings.update(data['app_settings'])
                    
        except Exception as e:
            print(f"Warning: Could not load config file: {e}")
            print("Using default configuration")
            
    def save_config(self):
        """Save configuration to file"""
        try:
            config_data = {
                'video': asdict(self.video),
                'preview': asdict(self.preview),
                'camera': asdict(self.camera),
                'color_correction': asdict(self.color_correction),
                'performance': asdict(self.performance),
                'audio': asdict(self.audio),
                'app_settings': self.app_settings
            }
            
            with open(self.config_file, 'w') as f:
                json.dump(config_data, f, indent=4)
                
        except Exception as e:
            print(f"Warning: Could not save config file: {e}")
            
    def get_picamera2_config(self):
        """Get configuration dictionary for Picamera2"""
        return {
            "main": {
                "size": self.video.resolution,
                "format": "RGB888"
            },
            "lores": {
                "size": self.preview.resolution,
                "format": "YUV420"
            },
            "controls": {
                "AnalogueGain": self.camera.analogue_gain,
                "DigitalGain": self.camera.digital_gain,
                "ExposureTime": self.camera.exposure_time,
                "AwbMode": self.camera.awb_mode,
                "Saturation": self.camera.saturation,
                "Contrast": self.camera.contrast,
                "Brightness": self.camera.brightness,
                "Sharpness": self.camera.sharpness
            }
        }
        
    def get_encoder_config(self):
        """Get H264 encoder configuration"""
        return {
            "bitrate": self.video.bitrate,
            "profile": self.video.h264_profile,
            "level": self.video.h264_level,
            "quality": self.video.quality,
            "repeat": True,
            "sps_timing": True,
            "intra_period": self.video.framerate  # I-frame every second
        }
        
    def update_video_settings(self, **kwargs):
        """Update video configuration settings"""
        for key, value in kwargs.items():
            if hasattr(self.video, key):
                setattr(self.video, key, value)
                
        if self.app_settings.get("auto_save_settings", True):
            self.save_config()
            
    def update_camera_settings(self, **kwargs):
        """Update camera configuration settings"""
        for key, value in kwargs.items():
            if hasattr(self.camera, key):
                setattr(self.camera, key, value)
                
        if self.app_settings.get("auto_save_settings", True):
            self.save_config()
            
    def update_color_correction(self, **kwargs):
        """Update color correction settings"""
        for key, value in kwargs.items():
            if hasattr(self.color_correction, key):
                setattr(self.color_correction, key, value)
                
        if self.app_settings.get("auto_save_settings", True):
            self.save_config()
            
    def get_resolution_options(self):
        """Get available resolution options"""
        return [
            (2560, 1440, "2K"),
            (1920, 1080, "Full HD"),
            (1280, 720, "HD"),
            (640, 480, "VGA")
        ]
        
    def get_bitrate_options(self):
        """Get bitrate options in Mbps"""
        return [5, 10, 15, 20, 25, 30, 40, 50]
        
    def get_framerate_options(self):
        """Get framerate options"""
        return [15, 24, 25, 30, 50, 60]
        
    def optimize_for_raspberry_pi(self):
        """Optimize settings for Raspberry Pi performance"""
        # Reduce memory usage
        self.performance.max_memory_mb = 256
        self.performance.frame_buffer_count = 4
        
        # Optimize encoding
        self.video.preset = "ultrafast"
        self.video.max_threads = 2
        
        # Reduce preview quality for better performance
        self.preview.resolution = (480, 360)
        self.preview.buffer_size = 2
        
        # Conservative camera settings
        self.camera.sensor_mode = 1
        
        print("Configuration optimized for Raspberry Pi")
        
    def optimize_for_desktop(self):
        """Optimize settings for desktop/laptop performance"""
        # Use more memory
        self.performance.max_memory_mb = 1024
        self.performance.frame_buffer_count = 8
        
        # Better encoding quality
        self.video.preset = "medium"
        self.video.max_threads = 4
        
        # Higher preview quality
        self.preview.resolution = (800, 600)
        self.preview.buffer_size = 4
        
        print("Configuration optimized for desktop")
        
    def get_medical_optimizations(self):
        """Get medical imaging optimizations"""
        return {
            "high_contrast": {
                "contrast": 1.2,
                "sharpness": 1.3,
                "saturation": 0.9
            },
            "skin_tone": {
                "color_temperature": 5200,
                "wb_red_gain": 1.1,
                "wb_blue_gain": 0.95
            },
            "detail_enhancement": {
                "sharpness": 1.5,
                "gamma": 0.9,
                "contrast": 1.1
            }
        }
        
    def validate_settings(self):
        """Validate configuration settings"""
        errors = []
        
        # Check video resolution
        if self.video.resolution[0] <= 0 or self.video.resolution[1] <= 0:
            errors.append("Invalid video resolution")
            
        # Check bitrate
        if self.video.bitrate <= 0:
            errors.append("Invalid bitrate")
            
        # Check framerate
        if self.video.framerate <= 0 or self.video.framerate > 120:
            errors.append("Invalid framerate")
            
        # Check memory limits
        if self.performance.max_memory_mb <= 0:
            errors.append("Invalid memory limit")
            
        return errors
        
    def reset_to_defaults(self):
        """Reset all settings to default values"""
        self.video = VideoConfig()
        self.preview = PreviewConfig()
        self.camera = CameraConfig()
        self.color_correction = ColorCorrectionConfig()
        self.performance = PerformanceConfig()
        self.audio = AudioConfig()
        
        print("Configuration reset to defaults")
        
    def __str__(self):
        """String representation of configuration"""
        return f"""MedVeCam Ultra 2.0 Configuration:
Video: {self.video.resolution[0]}x{self.video.resolution[1]} @ {self.video.framerate}fps, {self.video.bitrate//1000000}Mbps
Camera: Mode {self.camera.sensor_mode}, AG={self.camera.analogue_gain}, AWB={self.camera.awb_mode}
Performance: {self.performance.max_threads} threads, {self.performance.max_memory_mb}MB memory
"""