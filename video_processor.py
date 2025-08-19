"""
MedVeCam Ultra 2.0 Video Processor
Advanced video processing with color correction, gamma, and LUT support
"""

import numpy as np
import cv2
import logging
from typing import Optional, Dict, Any, Tuple
from pathlib import Path

class VideoProcessor:
    """Advanced video processing for medical applications"""
    
    def __init__(self):
        """Initialize video processor"""
        self.logger = logging.getLogger(__name__)
        
        # Color correction state
        self.gamma = 1.0
        self.brightness = 0.0
        self.contrast = 1.0
        self.saturation = 1.0
        
        # LUT tables
        self.lut_enabled = False
        self.color_lut = None
        self.gamma_lut = self._generate_gamma_lut(1.0)
        
        # Color matrix for advanced color correction
        self.color_matrix = None
        
        # White balance
        self.wb_red_gain = 1.0
        self.wb_blue_gain = 1.0
        
        self.logger.info("Video processor initialized")
        
    def process_frame(self, frame: np.ndarray, settings: Dict[str, Any] = None) -> np.ndarray:
        """Process a single frame with all enhancements"""
        if frame is None:
            return None
            
        try:
            processed_frame = frame.copy()
            
            # Apply settings if provided
            if settings:
                self.update_settings(settings)
                
            # Apply processing pipeline
            processed_frame = self._apply_white_balance(processed_frame)
            processed_frame = self._apply_brightness_contrast(processed_frame)
            processed_frame = self._apply_gamma_correction(processed_frame)
            processed_frame = self._apply_saturation(processed_frame)
            processed_frame = self._apply_color_matrix(processed_frame)
            processed_frame = self._apply_lut(processed_frame)
            processed_frame = self._apply_sharpening(processed_frame)
            
            return processed_frame
            
        except Exception as e:
            self.logger.error(f"Frame processing error: {e}")
            return frame
            
    def _apply_white_balance(self, frame: np.ndarray) -> np.ndarray:
        """Apply white balance correction"""
        if self.wb_red_gain == 1.0 and self.wb_blue_gain == 1.0:
            return frame
            
        try:
            # Split channels (BGR)
            b, g, r = cv2.split(frame)
            
            # Apply gains
            r = np.clip(r.astype(np.float32) * self.wb_red_gain, 0, 255).astype(np.uint8)
            b = np.clip(b.astype(np.float32) * self.wb_blue_gain, 0, 255).astype(np.uint8)
            
            # Merge channels
            return cv2.merge([b, g, r])
            
        except Exception as e:
            self.logger.error(f"White balance error: {e}")
            return frame
            
    def _apply_brightness_contrast(self, frame: np.ndarray) -> np.ndarray:
        """Apply brightness and contrast adjustments"""
        if self.brightness == 0.0 and self.contrast == 1.0:
            return frame
            
        try:
            # Convert to float for calculations
            frame_float = frame.astype(np.float32)
            
            # Apply contrast (multiplicative)
            frame_float *= self.contrast
            
            # Apply brightness (additive)
            frame_float += self.brightness
            
            # Clip and convert back to uint8
            return np.clip(frame_float, 0, 255).astype(np.uint8)
            
        except Exception as e:
            self.logger.error(f"Brightness/contrast error: {e}")
            return frame
            
    def _apply_gamma_correction(self, frame: np.ndarray) -> np.ndarray:
        """Apply gamma correction using LUT"""
        if self.gamma == 1.0:
            return frame
            
        try:
            return cv2.LUT(frame, self.gamma_lut)
            
        except Exception as e:
            self.logger.error(f"Gamma correction error: {e}")
            return frame
            
    def _apply_saturation(self, frame: np.ndarray) -> np.ndarray:
        """Apply saturation adjustment"""
        if self.saturation == 1.0:
            return frame
            
        try:
            # Convert to HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)
            
            # Adjust saturation
            hsv[:, :, 1] *= self.saturation
            hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
            
            # Convert back to BGR
            return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
            
        except Exception as e:
            self.logger.error(f"Saturation error: {e}")
            return frame
            
    def _apply_color_matrix(self, frame: np.ndarray) -> np.ndarray:
        """Apply color matrix transformation"""
        if self.color_matrix is None:
            return frame
            
        try:
            # Reshape frame for matrix multiplication
            height, width, channels = frame.shape
            frame_reshaped = frame.reshape(-1, channels).astype(np.float32)
            
            # Apply color matrix
            transformed = np.dot(frame_reshaped, self.color_matrix.T)
            
            # Clip and reshape back
            transformed = np.clip(transformed, 0, 255)
            return transformed.astype(np.uint8).reshape(height, width, channels)
            
        except Exception as e:
            self.logger.error(f"Color matrix error: {e}")
            return frame
            
    def _apply_lut(self, frame: np.ndarray) -> np.ndarray:
        """Apply custom LUT if enabled"""
        if not self.lut_enabled or self.color_lut is None:
            return frame
            
        try:
            return cv2.LUT(frame, self.color_lut)
            
        except Exception as e:
            self.logger.error(f"LUT error: {e}")
            return frame
            
    def _apply_sharpening(self, frame: np.ndarray, strength: float = 1.0) -> np.ndarray:
        """Apply unsharp masking for detail enhancement"""
        if strength == 0.0:
            return frame
            
        try:
            # Create Gaussian blur
            blurred = cv2.GaussianBlur(frame, (0, 0), 1.0)
            
            # Calculate unsharp mask
            unsharp = cv2.addWeighted(frame, 1.0 + strength, blurred, -strength, 0)
            
            return unsharp
            
        except Exception as e:
            self.logger.error(f"Sharpening error: {e}")
            return frame
            
    def _generate_gamma_lut(self, gamma: float) -> np.ndarray:
        """Generate gamma correction lookup table"""
        inv_gamma = 1.0 / gamma
        lut = np.array([((i / 255.0) ** inv_gamma) * 255 
                       for i in np.arange(0, 256)]).astype(np.uint8)
        return lut
        
    def update_settings(self, settings: Dict[str, Any]):
        """Update processing settings"""
        try:
            if "gamma" in settings:
                self.gamma = float(settings["gamma"])
                self.gamma_lut = self._generate_gamma_lut(self.gamma)
                
            if "brightness" in settings:
                self.brightness = float(settings["brightness"])
                
            if "contrast" in settings:
                self.contrast = float(settings["contrast"])
                
            if "saturation" in settings:
                self.saturation = float(settings["saturation"])
                
            if "wb_red_gain" in settings:
                self.wb_red_gain = float(settings["wb_red_gain"])
                
            if "wb_blue_gain" in settings:
                self.wb_blue_gain = float(settings["wb_blue_gain"])
                
            if "lut_enabled" in settings:
                self.lut_enabled = bool(settings["lut_enabled"])
                
            if "lut_file" in settings and settings["lut_file"]:
                self.load_lut(settings["lut_file"])
                
            self.logger.info(f"Updated processing settings: {settings}")
            
        except Exception as e:
            self.logger.error(f"Settings update error: {e}")
            
    def load_lut(self, lut_file: str) -> bool:
        """Load custom LUT from file"""
        try:
            lut_path = Path(lut_file)
            
            if lut_path.suffix.lower() == '.cube':
                self.color_lut = self._load_cube_lut(lut_path)
            elif lut_path.suffix.lower() in ['.png', '.jpg', '.bmp']:
                self.color_lut = self._load_image_lut(lut_path)
            else:
                self.logger.error(f"Unsupported LUT format: {lut_path.suffix}")
                return False
                
            self.lut_enabled = True
            self.logger.info(f"Loaded LUT: {lut_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load LUT: {e}")
            return False
            
    def _load_cube_lut(self, lut_path: Path) -> Optional[np.ndarray]:
        """Load .cube format LUT"""
        try:
            # This is a simplified .cube loader
            # In a full implementation, you would parse the .cube format properly
            self.logger.warning("CUBE LUT loading not fully implemented")
            return None
            
        except Exception as e:
            self.logger.error(f"CUBE LUT loading error: {e}")
            return None
            
    def _load_image_lut(self, lut_path: Path) -> Optional[np.ndarray]:
        """Load LUT from image file"""
        try:
            # Load image as LUT
            lut_image = cv2.imread(str(lut_path))
            
            if lut_image is None:
                self.logger.error(f"Could not load LUT image: {lut_path}")
                return None
                
            # Convert to LUT format (simplified)
            # This assumes a specific LUT image format
            if lut_image.shape[0] == 256 and lut_image.shape[1] == 1:
                return lut_image.reshape(256, 3)
            else:
                self.logger.error(f"Invalid LUT image dimensions: {lut_image.shape}")
                return None
                
        except Exception as e:
            self.logger.error(f"Image LUT loading error: {e}")
            return None
            
    def create_medical_enhancement(self, frame: np.ndarray, enhancement_type: str) -> np.ndarray:
        """Apply medical-specific enhancements"""
        try:
            if enhancement_type == "high_contrast":
                return self._enhance_contrast(frame)
            elif enhancement_type == "detail_enhancement":
                return self._enhance_details(frame)
            elif enhancement_type == "skin_tone":
                return self._optimize_skin_tone(frame)
            elif enhancement_type == "vessel_enhancement":
                return self._enhance_vessels(frame)
            else:
                self.logger.warning(f"Unknown enhancement type: {enhancement_type}")
                return frame
                
        except Exception as e:
            self.logger.error(f"Medical enhancement error: {e}")
            return frame
            
    def _enhance_contrast(self, frame: np.ndarray) -> np.ndarray:
        """High contrast enhancement for medical imaging"""
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        enhanced = cv2.merge([l, a, b])
        return cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
        
    def _enhance_details(self, frame: np.ndarray) -> np.ndarray:
        """Detail enhancement using unsharp masking"""
        return self._apply_sharpening(frame, strength=1.5)
        
    def _optimize_skin_tone(self, frame: np.ndarray) -> np.ndarray:
        """Optimize for skin tone visibility"""
        # Adjust color temperature for better skin tone representation
        frame_float = frame.astype(np.float32)
        
        # Slight warm adjustment
        frame_float[:, :, 2] *= 1.05  # Red channel
        frame_float[:, :, 0] *= 0.95  # Blue channel
        
        return np.clip(frame_float, 0, 255).astype(np.uint8)
        
    def _enhance_vessels(self, frame: np.ndarray) -> np.ndarray:
        """Enhance blood vessel visibility"""
        # Convert to grayscale for vessel enhancement
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply morphological operations to enhance vessels
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel)
        
        # Enhance contrast
        enhanced = cv2.add(gray, blackhat)
        
        # Convert back to color
        return cv2.cvtColor(enhanced, cv2.COLOR_GRAY2BGR)
        
    def analyze_frame_quality(self, frame: np.ndarray) -> Dict[str, float]:
        """Analyze frame quality metrics"""
        try:
            # Convert to grayscale for analysis
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Calculate metrics
            metrics = {}
            
            # Sharpness (Laplacian variance)
            metrics["sharpness"] = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # Brightness (mean)
            metrics["brightness"] = np.mean(gray)
            
            # Contrast (standard deviation)
            metrics["contrast"] = np.std(gray)
            
            # Exposure (histogram analysis)
            hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
            metrics["overexposure"] = np.sum(hist[240:]) / np.sum(hist) * 100
            metrics["underexposure"] = np.sum(hist[:16]) / np.sum(hist) * 100
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Quality analysis error: {e}")
            return {}
            
    def get_recommended_settings(self, frame: np.ndarray) -> Dict[str, float]:
        """Get recommended settings based on frame analysis"""
        try:
            quality = self.analyze_frame_quality(frame)
            recommendations = {}
            
            # Brightness recommendation
            if quality.get("brightness", 128) < 80:
                recommendations["brightness"] = 20
            elif quality.get("brightness", 128) > 180:
                recommendations["brightness"] = -20
            else:
                recommendations["brightness"] = 0
                
            # Contrast recommendation
            if quality.get("contrast", 50) < 30:
                recommendations["contrast"] = 1.2
            else:
                recommendations["contrast"] = 1.0
                
            # Gamma recommendation based on histogram
            if quality.get("underexposure", 0) > 15:
                recommendations["gamma"] = 0.8
            elif quality.get("overexposure", 0) > 15:
                recommendations["gamma"] = 1.2
            else:
                recommendations["gamma"] = 1.0
                
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Recommendation error: {e}")
            return {}
            
    def save_processed_frame(self, frame: np.ndarray, output_path: str) -> bool:
        """Save processed frame to file"""
        try:
            success = cv2.imwrite(output_path, frame)
            if success:
                self.logger.info(f"Saved processed frame: {output_path}")
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to save frame: {e}")
            return False
            
    def get_processing_info(self) -> Dict[str, Any]:
        """Get current processing configuration"""
        return {
            "gamma": self.gamma,
            "brightness": self.brightness,
            "contrast": self.contrast,
            "saturation": self.saturation,
            "wb_red_gain": self.wb_red_gain,
            "wb_blue_gain": self.wb_blue_gain,
            "lut_enabled": self.lut_enabled,
            "color_matrix_enabled": self.color_matrix is not None
        }