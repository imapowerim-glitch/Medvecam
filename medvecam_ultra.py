#!/usr/bin/env python3
"""
MedVeCam Ultra 2.0 - Advanced Medical Camera Application
Main application file with enhanced video quality and performance optimizations
"""

import sys
import os
import threading
import time
import logging
from datetime import datetime
from pathlib import Path

try:
    import cv2
    import numpy as np
    from picamera2 import Picamera2
    from picamera2.encoders import H264Encoder
    from picamera2.outputs import FileOutput
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox
    from PIL import Image, ImageTk
except ImportError as e:
    print(f"Missing required dependencies: {e}")
    print("Please install requirements: pip install -r requirements.txt")
    sys.exit(1)

from config import MedVeCamConfig
from camera_handler import CameraHandler
from video_processor import VideoProcessor
from medical_presets import MedicalPresets

class MedVeCamUltra:
    """Main MedVeCam Ultra 2.0 Application"""
    
    def __init__(self):
        self.config = MedVeCamConfig()
        self.camera_handler = None
        self.video_processor = VideoProcessor()
        self.medical_presets = MedicalPresets()
        
        # Application state
        self.is_recording = False
        self.is_previewing = False
        self.recording_start_time = None
        self.output_dir = Path.home() / "MedVeCam_Recordings"
        self.output_dir.mkdir(exist_ok=True)
        
        # Threading
        self.preview_thread = None
        self.recording_thread = None
        self.stop_preview = threading.Event()
        
        # GUI components
        self.root = None
        self.preview_label = None
        self.status_var = None
        self.quality_var = None
        self.preset_var = None
        
        # Setup logging
        self.setup_logging()
        
    def setup_logging(self):
        """Setup application logging"""
        log_dir = Path.home() / "MedVeCam_Logs"
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / f"medvecam_{datetime.now().strftime('%Y%m%d')}.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("MedVeCam Ultra 2.0 initialized")
        
    def initialize_camera(self):
        """Initialize camera with optimized settings"""
        try:
            self.camera_handler = CameraHandler(self.config)
            self.camera_handler.initialize()
            self.logger.info("Camera initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize camera: {e}")
            messagebox.showerror("Camera Error", f"Failed to initialize camera: {e}")
            return False
            
    def create_gui(self):
        """Create the enhanced GUI interface"""
        self.root = tk.Tk()
        self.root.title("MedVeCam Ultra 2.0 - Medical Camera System")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        
        # Create main frames
        self.create_preview_frame()
        self.create_control_panel()
        self.create_status_panel()
        
        # Setup menu
        self.create_menu()
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def create_preview_frame(self):
        """Create video preview frame"""
        preview_frame = ttk.LabelFrame(self.root, text="Live Preview", padding=10)
        preview_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Preview display
        self.preview_label = tk.Label(preview_frame, bg='black', text="No Preview Available")
        self.preview_label.pack(fill=tk.BOTH, expand=True)
        
        # Preview controls
        preview_controls = ttk.Frame(preview_frame)
        preview_controls.pack(fill=tk.X, pady=5)
        
        ttk.Button(preview_controls, text="Start Preview", 
                  command=self.start_preview).pack(side=tk.LEFT, padx=5)
        ttk.Button(preview_controls, text="Stop Preview", 
                  command=self.stop_preview_func).pack(side=tk.LEFT, padx=5)
        
    def create_control_panel(self):
        """Create control panel with medical presets and settings"""
        control_frame = ttk.LabelFrame(self.root, text="Control Panel", padding=10)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        
        # Recording controls
        record_frame = ttk.LabelFrame(control_frame, text="Recording", padding=5)
        record_frame.pack(fill=tk.X, pady=5)
        
        self.record_btn = ttk.Button(record_frame, text="Start Recording", 
                                    command=self.toggle_recording)
        self.record_btn.pack(fill=tk.X, pady=2)
        
        # Medical presets
        preset_frame = ttk.LabelFrame(control_frame, text="Medical Presets", padding=5)
        preset_frame.pack(fill=tk.X, pady=5)
        
        self.preset_var = tk.StringVar(value="General")
        preset_combo = ttk.Combobox(preset_frame, textvariable=self.preset_var,
                                   values=list(self.medical_presets.get_preset_names()))
        preset_combo.pack(fill=tk.X, pady=2)
        preset_combo.bind("<<ComboboxSelected>>", self.apply_preset)
        
        ttk.Button(preset_frame, text="Apply Preset", 
                  command=self.apply_preset).pack(fill=tk.X, pady=2)
        
        # Quality settings
        quality_frame = ttk.LabelFrame(control_frame, text="Quality Settings", padding=5)
        quality_frame.pack(fill=tk.X, pady=5)
        
        # Resolution
        ttk.Label(quality_frame, text="Resolution:").pack(anchor=tk.W)
        res_var = tk.StringVar(value="2560x1440")
        ttk.Combobox(quality_frame, textvariable=res_var,
                    values=["2560x1440", "1920x1080", "1280x720"]).pack(fill=tk.X, pady=2)
        
        # Bitrate
        ttk.Label(quality_frame, text="Bitrate (Mbps):").pack(anchor=tk.W)
        bitrate_var = tk.StringVar(value="25")
        ttk.Spinbox(quality_frame, from_=5, to=50, textvariable=bitrate_var).pack(fill=tk.X, pady=2)
        
        # Color correction
        color_frame = ttk.LabelFrame(control_frame, text="Color Correction", padding=5)
        color_frame.pack(fill=tk.X, pady=5)
        
        # Gamma correction
        ttk.Label(color_frame, text="Gamma:").pack(anchor=tk.W)
        gamma_scale = ttk.Scale(color_frame, from_=0.5, to=3.0, orient=tk.HORIZONTAL)
        gamma_scale.set(1.0)
        gamma_scale.pack(fill=tk.X, pady=2)
        
        # Brightness
        ttk.Label(color_frame, text="Brightness:").pack(anchor=tk.W)
        brightness_scale = ttk.Scale(color_frame, from_=-100, to=100, orient=tk.HORIZONTAL)
        brightness_scale.set(0)
        brightness_scale.pack(fill=tk.X, pady=2)
        
        # Contrast
        ttk.Label(color_frame, text="Contrast:").pack(anchor=tk.W)
        contrast_scale = ttk.Scale(color_frame, from_=0.5, to=3.0, orient=tk.HORIZONTAL)
        contrast_scale.set(1.0)
        contrast_scale.pack(fill=tk.X, pady=2)
        
    def create_status_panel(self):
        """Create status panel with indicators"""
        status_frame = ttk.Frame(self.root)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        
        # Status indicators
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.pack(side=tk.LEFT)
        
        # Quality indicator
        self.quality_var = tk.StringVar(value="Quality: Excellent")
        quality_label = ttk.Label(status_frame, textvariable=self.quality_var)
        quality_label.pack(side=tk.RIGHT)
        
    def create_menu(self):
        """Create application menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Output Folder", command=self.open_output_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        
        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Camera Settings", command=self.open_camera_settings)
        settings_menu.add_command(label="Advanced Settings", command=self.open_advanced_settings)
        
    def start_preview(self):
        """Start camera preview with optimized buffering"""
        if not self.camera_handler:
            if not self.initialize_camera():
                return
                
        if not self.is_previewing:
            self.is_previewing = True
            self.stop_preview.clear()
            self.preview_thread = threading.Thread(target=self._preview_loop)
            self.preview_thread.daemon = True
            self.preview_thread.start()
            self.status_var.set("Preview Active")
            self.logger.info("Preview started")
            
    def stop_preview_func(self):
        """Stop camera preview"""
        if self.is_previewing:
            self.is_previewing = False
            self.stop_preview.set()
            if self.preview_thread:
                self.preview_thread.join(timeout=2.0)
            self.status_var.set("Preview Stopped")
            self.logger.info("Preview stopped")
            
    def _preview_loop(self):
        """Preview loop with optimized performance"""
        try:
            while self.is_previewing and not self.stop_preview.is_set():
                frame = self.camera_handler.capture_frame()
                if frame is not None:
                    # Resize for preview (reduce computational load)
                    preview_frame = cv2.resize(frame, (640, 480))
                    
                    # Convert to RGB for Tkinter
                    rgb_frame = cv2.cvtColor(preview_frame, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(rgb_frame)
                    photo = ImageTk.PhotoImage(img)
                    
                    # Update GUI in main thread
                    self.root.after(0, self._update_preview, photo)
                    
                # Control frame rate to reduce CPU usage
                time.sleep(1/30)  # ~30 FPS
                
        except Exception as e:
            self.logger.error(f"Preview error: {e}")
            self.root.after(0, lambda: self.status_var.set(f"Preview Error: {e}"))
            
    def _update_preview(self, photo):
        """Update preview display"""
        if self.preview_label:
            self.preview_label.configure(image=photo)
            self.preview_label.image = photo  # Keep a reference
            
    def toggle_recording(self):
        """Toggle video recording"""
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
            
    def start_recording(self):
        """Start video recording with 2K quality"""
        if not self.camera_handler:
            if not self.initialize_camera():
                return
                
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = self.output_dir / f"medvecam_recording_{timestamp}.mp4"
            
            self.camera_handler.start_recording(str(filename))
            self.is_recording = True
            self.recording_start_time = time.time()
            
            self.record_btn.configure(text="Stop Recording")
            self.status_var.set("Recording...")
            self.logger.info(f"Recording started: {filename}")
            
            # Start recording timer thread
            self.recording_thread = threading.Thread(target=self._recording_timer)
            self.recording_thread.daemon = True
            self.recording_thread.start()
            
        except Exception as e:
            self.logger.error(f"Failed to start recording: {e}")
            messagebox.showerror("Recording Error", f"Failed to start recording: {e}")
            
    def stop_recording(self):
        """Stop video recording"""
        if self.is_recording:
            try:
                self.camera_handler.stop_recording()
                self.is_recording = False
                self.recording_start_time = None
                
                self.record_btn.configure(text="Start Recording")
                self.status_var.set("Recording Stopped")
                self.logger.info("Recording stopped")
                
            except Exception as e:
                self.logger.error(f"Failed to stop recording: {e}")
                messagebox.showerror("Recording Error", f"Failed to stop recording: {e}")
                
    def _recording_timer(self):
        """Update recording timer"""
        while self.is_recording and self.recording_start_time:
            elapsed = time.time() - self.recording_start_time
            minutes, seconds = divmod(int(elapsed), 60)
            timer_text = f"Recording... {minutes:02d}:{seconds:02d}"
            self.root.after(0, lambda: self.status_var.set(timer_text))
            time.sleep(1)
            
    def apply_preset(self, event=None):
        """Apply medical preset settings"""
        preset_name = self.preset_var.get()
        preset = self.medical_presets.get_preset(preset_name)
        
        if preset and self.camera_handler:
            self.camera_handler.apply_settings(preset)
            self.status_var.set(f"Applied preset: {preset_name}")
            self.logger.info(f"Applied medical preset: {preset_name}")
            
    def open_output_folder(self):
        """Open output folder in file manager"""
        import subprocess
        import platform
        
        if platform.system() == "Linux":
            subprocess.run(["xdg-open", str(self.output_dir)])
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", str(self.output_dir)])
        elif platform.system() == "Windows":
            subprocess.run(["explorer", str(self.output_dir)])
            
    def open_camera_settings(self):
        """Open camera settings dialog"""
        # Placeholder for camera settings dialog
        messagebox.showinfo("Camera Settings", "Camera settings dialog - To be implemented")
        
    def open_advanced_settings(self):
        """Open advanced settings dialog"""
        # Placeholder for advanced settings dialog
        messagebox.showinfo("Advanced Settings", "Advanced settings dialog - To be implemented")
        
    def on_closing(self):
        """Handle application closing"""
        if self.is_recording:
            if messagebox.askokcancel("Quit", "Recording is active. Stop recording and quit?"):
                self.stop_recording()
            else:
                return
                
        self.stop_preview_func()
        
        if self.camera_handler:
            self.camera_handler.cleanup()
            
        self.logger.info("MedVeCam Ultra 2.0 shutting down")
        self.root.destroy()
        
    def run(self):
        """Run the application"""
        self.logger.info("Starting MedVeCam Ultra 2.0 GUI")
        
        # Initialize camera
        if not self.initialize_camera():
            self.logger.error("Failed to initialize camera, continuing without camera")
            
        # Create and run GUI
        self.create_gui()
        self.root.mainloop()

def main():
    """Main entry point"""
    try:
        app = MedVeCamUltra()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
    except Exception as e:
        print(f"Unexpected error: {e}")
        logging.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()