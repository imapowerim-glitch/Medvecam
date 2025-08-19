"""
MedVeCam Ultra 2.0 Camera Handler
Optimized camera handling with Raspberry Pi support and error handling
"""

import time
import threading
import logging
from typing import Optional, Dict, Any
import cv2
import numpy as np

try:
    from picamera2 import Picamera2
    from picamera2.encoders import H264Encoder, Quality
    from picamera2.outputs import FileOutput
    PICAMERA2_AVAILABLE = True
except ImportError:
    PICAMERA2_AVAILABLE = False
    print("Warning: picamera2 not available, using OpenCV fallback")

from config import MedVeCamConfig

class CameraHandler:
    """Advanced camera handler with optimization for medical applications"""
    
    def __init__(self, config: MedVeCamConfig):
        """Initialize camera handler"""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Camera objects
        self.picamera2 = None
        self.cv_camera = None
        self.encoder = None
        self.output = None
        
        # State management
        self.is_initialized = False
        self.is_recording = False
        self.is_previewing = False
        self.camera_type = None
        
        # Threading
        self.frame_lock = threading.Lock()
        self.latest_frame = None
        
        # Performance monitoring
        self.frame_count = 0
        self.dropped_frames = 0
        self.last_fps_check = time.time()
        
    def initialize(self):
        """Initialize camera with auto-detection"""
        self.logger.info("Initializing camera...")
        
        # Try Raspberry Pi camera first
        if PICAMERA2_AVAILABLE and self._init_picamera2():
            self.camera_type = "picamera2"
            self.logger.info("Initialized Raspberry Pi camera (picamera2)")
            
        # Fallback to USB/webcam
        elif self._init_opencv_camera():
            self.camera_type = "opencv"
            self.logger.info("Initialized USB/webcam (OpenCV)")
            
        else:
            raise RuntimeError("No compatible camera found")
            
        self.is_initialized = True
        self._configure_camera()
        
    def _init_picamera2(self):
        """Initialize Raspberry Pi camera using picamera2"""
        try:
            self.picamera2 = Picamera2()
            
            # Configure camera
            camera_config = self.config.get_picamera2_config()
            self.picamera2.configure(camera_config)
            
            # Start camera
            self.picamera2.start()
            
            # Wait for camera to stabilize
            time.sleep(2)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize picamera2: {e}")
            if self.picamera2:
                try:
                    self.picamera2.close()
                except:
                    pass
                self.picamera2 = None
            return False
            
    def _init_opencv_camera(self):
        """Initialize USB/webcam using OpenCV"""
        try:
            # Try different camera indices
            for camera_id in range(4):
                self.cv_camera = cv2.VideoCapture(camera_id)
                
                if self.cv_camera.isOpened():
                    # Test capture
                    ret, frame = self.cv_camera.read()
                    if ret and frame is not None:
                        self.logger.info(f"Found camera at index {camera_id}")
                        return True
                        
                self.cv_camera.release()
                self.cv_camera = None
                
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to initialize OpenCV camera: {e}")
            if self.cv_camera:
                self.cv_camera.release()
                self.cv_camera = None
            return False
            
    def _configure_camera(self):
        """Configure camera settings based on type"""
        if self.camera_type == "picamera2":
            self._configure_picamera2()
        elif self.camera_type == "opencv":
            self._configure_opencv()
            
    def _configure_picamera2(self):
        """Configure Raspberry Pi camera settings"""
        try:
            controls = {}
            
            # Basic controls
            controls["AnalogueGain"] = self.config.camera.analogue_gain
            controls["DigitalGain"] = self.config.camera.digital_gain
            controls["ExposureTime"] = self.config.camera.exposure_time
            
            # Auto settings
            if self.config.camera.auto_exposure:
                controls["AeEnable"] = True
            else:
                controls["AeEnable"] = False
                
            # White balance
            if self.config.camera.awb_mode == "auto":
                controls["AwbEnable"] = True
            else:
                controls["AwbEnable"] = False
                
            # Image quality
            controls["Saturation"] = self.config.camera.saturation
            controls["Contrast"] = self.config.camera.contrast
            controls["Brightness"] = self.config.camera.brightness
            controls["Sharpness"] = self.config.camera.sharpness
            
            # Apply controls
            self.picamera2.set_controls(controls)
            
            self.logger.info("Raspberry Pi camera configured")
            
        except Exception as e:
            self.logger.error(f"Failed to configure picamera2: {e}")
            
    def _configure_opencv(self):
        """Configure OpenCV camera settings"""
        try:
            # Set resolution
            width, height = self.config.video.resolution
            self.cv_camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.cv_camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            
            # Set framerate
            self.cv_camera.set(cv2.CAP_PROP_FPS, self.config.video.framerate)
            
            # Set format
            self.cv_camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
            
            # Image adjustments (if supported)
            self.cv_camera.set(cv2.CAP_PROP_BRIGHTNESS, self.config.camera.brightness)
            self.cv_camera.set(cv2.CAP_PROP_CONTRAST, self.config.camera.contrast)
            self.cv_camera.set(cv2.CAP_PROP_SATURATION, self.config.camera.saturation)
            
            # Buffer size (reduce latency)
            self.cv_camera.set(cv2.CAP_PROP_BUFFERSIZE, self.config.preview.buffer_size)
            
            self.logger.info("OpenCV camera configured")
            
        except Exception as e:
            self.logger.error(f"Failed to configure OpenCV camera: {e}")
            
    def capture_frame(self) -> Optional[np.ndarray]:
        """Capture a single frame"""
        if not self.is_initialized:
            return None
            
        try:
            with self.frame_lock:
                if self.camera_type == "picamera2":
                    return self._capture_picamera2_frame()
                elif self.camera_type == "opencv":
                    return self._capture_opencv_frame()
                    
        except Exception as e:
            self.logger.error(f"Frame capture error: {e}")
            return None
            
    def _capture_picamera2_frame(self) -> Optional[np.ndarray]:
        """Capture frame from Raspberry Pi camera"""
        try:
            # Capture array (for preview)
            frame = self.picamera2.capture_array()
            
            # Convert RGB to BGR for OpenCV compatibility
            if len(frame.shape) == 3 and frame.shape[2] == 3:
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                
            self.frame_count += 1
            self.latest_frame = frame
            return frame
            
        except Exception as e:
            self.logger.error(f"Picamera2 capture error: {e}")
            self.dropped_frames += 1
            return None
            
    def _capture_opencv_frame(self) -> Optional[np.ndarray]:
        """Capture frame from OpenCV camera"""
        try:
            ret, frame = self.cv_camera.read()
            
            if ret and frame is not None:
                self.frame_count += 1
                self.latest_frame = frame
                return frame
            else:
                self.dropped_frames += 1
                return None
                
        except Exception as e:
            self.logger.error(f"OpenCV capture error: {e}")
            self.dropped_frames += 1
            return None
            
    def start_recording(self, output_file: str):
        """Start video recording with optimized H264 encoding"""
        if self.is_recording:
            self.logger.warning("Recording already in progress")
            return
            
        try:
            if self.camera_type == "picamera2":
                self._start_picamera2_recording(output_file)
            elif self.camera_type == "opencv":
                self._start_opencv_recording(output_file)
                
            self.is_recording = True
            self.logger.info(f"Recording started: {output_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to start recording: {e}")
            raise
            
    def _start_picamera2_recording(self, output_file: str):
        """Start recording with Raspberry Pi camera"""
        try:
            # Create H264 encoder with optimized settings
            encoder_config = self.config.get_encoder_config()
            
            self.encoder = H264Encoder(
                bitrate=encoder_config["bitrate"],
                repeat=encoder_config["repeat"],
                iperiod=encoder_config.get("intra_period", 30)
            )
            
            # Create file output
            self.output = FileOutput(output_file)
            
            # Start recording
            self.picamera2.start_encoder(self.encoder, self.output)
            
        except Exception as e:
            self.logger.error(f"Picamera2 recording setup failed: {e}")
            raise
            
    def _start_opencv_recording(self, output_file: str):
        """Start recording with OpenCV camera"""
        try:
            # Create VideoWriter
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            width, height = self.config.video.resolution
            fps = self.config.video.framerate
            
            self.output = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
            
            if not self.output.isOpened():
                raise RuntimeError("Failed to open video writer")
                
            # Start recording thread
            self.recording_thread = threading.Thread(target=self._opencv_recording_loop)
            self.recording_thread.daemon = True
            self.recording_thread.start()
            
        except Exception as e:
            self.logger.error(f"OpenCV recording setup failed: {e}")
            raise
            
    def _opencv_recording_loop(self):
        """Recording loop for OpenCV camera"""
        try:
            while self.is_recording:
                frame = self.capture_frame()
                if frame is not None:
                    # Resize if necessary
                    width, height = self.config.video.resolution
                    if frame.shape[1] != width or frame.shape[0] != height:
                        frame = cv2.resize(frame, (width, height))
                        
                    self.output.write(frame)
                    
                # Control recording framerate
                time.sleep(1 / self.config.video.framerate)
                
        except Exception as e:
            self.logger.error(f"Recording loop error: {e}")
            
    def stop_recording(self):
        """Stop video recording"""
        if not self.is_recording:
            self.logger.warning("No recording in progress")
            return
            
        try:
            self.is_recording = False
            
            if self.camera_type == "picamera2":
                self._stop_picamera2_recording()
            elif self.camera_type == "opencv":
                self._stop_opencv_recording()
                
            self.logger.info("Recording stopped")
            
        except Exception as e:
            self.logger.error(f"Failed to stop recording: {e}")
            
    def _stop_picamera2_recording(self):
        """Stop Raspberry Pi camera recording"""
        try:
            if self.encoder:
                self.picamera2.stop_encoder()
                self.encoder = None
                
            if self.output:
                self.output.close()
                self.output = None
                
        except Exception as e:
            self.logger.error(f"Picamera2 recording stop error: {e}")
            
    def _stop_opencv_recording(self):
        """Stop OpenCV camera recording"""
        try:
            if hasattr(self, 'recording_thread'):
                self.recording_thread.join(timeout=5.0)
                
            if self.output:
                self.output.release()
                self.output = None
                
        except Exception as e:
            self.logger.error(f"OpenCV recording stop error: {e}")
            
    def apply_settings(self, settings: Dict[str, Any]):
        """Apply camera settings"""
        try:
            if self.camera_type == "picamera2":
                # Convert settings to picamera2 controls
                controls = {}
                
                if "brightness" in settings:
                    controls["Brightness"] = settings["brightness"]
                if "contrast" in settings:
                    controls["Contrast"] = settings["contrast"]
                if "saturation" in settings:
                    controls["Saturation"] = settings["saturation"]
                if "sharpness" in settings:
                    controls["Sharpness"] = settings["sharpness"]
                if "exposure_time" in settings:
                    controls["ExposureTime"] = settings["exposure_time"]
                if "analogue_gain" in settings:
                    controls["AnalogueGain"] = settings["analogue_gain"]
                    
                if controls:
                    self.picamera2.set_controls(controls)
                    
            elif self.camera_type == "opencv":
                # Apply OpenCV camera properties
                if "brightness" in settings:
                    self.cv_camera.set(cv2.CAP_PROP_BRIGHTNESS, settings["brightness"])
                if "contrast" in settings:
                    self.cv_camera.set(cv2.CAP_PROP_CONTRAST, settings["contrast"])
                if "saturation" in settings:
                    self.cv_camera.set(cv2.CAP_PROP_SATURATION, settings["saturation"])
                    
            self.logger.info(f"Applied camera settings: {settings}")
            
        except Exception as e:
            self.logger.error(f"Failed to apply settings: {e}")
            
    def get_camera_info(self) -> Dict[str, Any]:
        """Get camera information"""
        info = {
            "type": self.camera_type,
            "initialized": self.is_initialized,
            "recording": self.is_recording,
            "frame_count": self.frame_count,
            "dropped_frames": self.dropped_frames
        }
        
        try:
            if self.camera_type == "picamera2" and self.picamera2:
                # Get camera properties
                info.update({
                    "sensor_modes": "Available",
                    "controls": "Full picamera2 support"
                })
                
            elif self.camera_type == "opencv" and self.cv_camera:
                info.update({
                    "width": int(self.cv_camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
                    "height": int(self.cv_camera.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                    "fps": self.cv_camera.get(cv2.CAP_PROP_FPS)
                })
                
        except Exception as e:
            self.logger.error(f"Error getting camera info: {e}")
            
        return info
        
    def get_performance_stats(self) -> Dict[str, float]:
        """Get performance statistics"""
        current_time = time.time()
        time_diff = current_time - self.last_fps_check
        
        if time_diff >= 1.0:  # Update every second
            fps = self.frame_count / time_diff if time_diff > 0 else 0
            drop_rate = self.dropped_frames / max(self.frame_count + self.dropped_frames, 1) * 100
            
            stats = {
                "fps": round(fps, 2),
                "drop_rate": round(drop_rate, 2),
                "total_frames": self.frame_count,
                "dropped_frames": self.dropped_frames
            }
            
            # Reset counters
            self.frame_count = 0
            self.dropped_frames = 0
            self.last_fps_check = current_time
            
            return stats
            
        return {}
        
    def cleanup(self):
        """Cleanup camera resources"""
        try:
            if self.is_recording:
                self.stop_recording()
                
            if self.camera_type == "picamera2" and self.picamera2:
                self.picamera2.stop()
                self.picamera2.close()
                self.picamera2 = None
                
            elif self.camera_type == "opencv" and self.cv_camera:
                self.cv_camera.release()
                self.cv_camera = None
                
            self.is_initialized = False
            self.logger.info("Camera cleanup completed")
            
        except Exception as e:
            self.logger.error(f"Camera cleanup error: {e}")
            
    def __del__(self):
        """Destructor"""
        self.cleanup()