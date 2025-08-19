"""
MedVeCam Ultra 2.0 Medical Presets
Specialized presets for different medical imaging scenarios
"""

import logging
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class MedicalPreset:
    """Medical imaging preset configuration"""
    name: str
    description: str
    camera_settings: Dict[str, Any]
    processing_settings: Dict[str, Any]
    recording_settings: Dict[str, Any]

class MedicalPresets:
    """Medical presets manager for specialized imaging"""
    
    def __init__(self):
        """Initialize medical presets"""
        self.logger = logging.getLogger(__name__)
        self.presets = {}
        self._initialize_default_presets()
        
    def _initialize_default_presets(self):
        """Initialize default medical presets"""
        
        # General medical imaging
        self.presets["General"] = MedicalPreset(
            name="General",
            description="General purpose medical imaging with balanced settings",
            camera_settings={
                "brightness": 0.0,
                "contrast": 1.0,
                "saturation": 1.0,
                "sharpness": 1.0,
                "exposure_time": 33000,
                "analogue_gain": 1.0,
                "awb_mode": "auto"
            },
            processing_settings={
                "gamma": 1.0,
                "brightness": 0,
                "contrast": 1.0,
                "saturation": 1.0,
                "wb_red_gain": 1.0,
                "wb_blue_gain": 1.0
            },
            recording_settings={
                "bitrate": 25000000,
                "quality": 23
            }
        )
        
        # Surgical procedures
        self.presets["Surgery"] = MedicalPreset(
            name="Surgery",
            description="Optimized for surgical procedures with high detail and accurate colors",
            camera_settings={
                "brightness": 10.0,
                "contrast": 1.2,
                "saturation": 1.1,
                "sharpness": 1.3,
                "exposure_time": 25000,
                "analogue_gain": 1.0,
                "awb_mode": "tungsten"  # For OR lighting
            },
            processing_settings={
                "gamma": 0.9,
                "brightness": 5,
                "contrast": 1.2,
                "saturation": 1.1,
                "wb_red_gain": 1.05,
                "wb_blue_gain": 0.95
            },
            recording_settings={
                "bitrate": 30000000,  # Higher bitrate for detail
                "quality": 20
            }
        )
        
        # Dermatology
        self.presets["Dermatology"] = MedicalPreset(
            name="Dermatology",
            description="Skin examination with enhanced detail and accurate skin tone reproduction",
            camera_settings={
                "brightness": 5.0,
                "contrast": 1.15,
                "saturation": 1.2,
                "sharpness": 1.4,
                "exposure_time": 30000,
                "analogue_gain": 1.0,
                "awb_mode": "daylight"
            },
            processing_settings={
                "gamma": 0.95,
                "brightness": 3,
                "contrast": 1.15,
                "saturation": 1.2,
                "wb_red_gain": 1.1,
                "wb_blue_gain": 0.9
            },
            recording_settings={
                "bitrate": 25000000,
                "quality": 22
            }
        )
        
        # Ophthalmology
        self.presets["Ophthalmology"] = MedicalPreset(
            name="Ophthalmology",
            description="Eye examination with optimized contrast and detail enhancement",
            camera_settings={
                "brightness": -5.0,
                "contrast": 1.3,
                "saturation": 0.9,
                "sharpness": 1.5,
                "exposure_time": 20000,
                "analogue_gain": 1.2,
                "awb_mode": "auto"
            },
            processing_settings={
                "gamma": 0.85,
                "brightness": -10,
                "contrast": 1.3,
                "saturation": 0.9,
                "wb_red_gain": 1.0,
                "wb_blue_gain": 1.0
            },
            recording_settings={
                "bitrate": 25000000,
                "quality": 21
            }
        )
        
        # Endoscopy
        self.presets["Endoscopy"] = MedicalPreset(
            name="Endoscopy",
            description="Internal examination with enhanced visibility in low-light conditions",
            camera_settings={
                "brightness": 15.0,
                "contrast": 1.4,
                "saturation": 1.3,
                "sharpness": 1.2,
                "exposure_time": 40000,
                "analogue_gain": 1.5,
                "awb_mode": "auto"
            },
            processing_settings={
                "gamma": 0.8,
                "brightness": 15,
                "contrast": 1.4,
                "saturation": 1.3,
                "wb_red_gain": 1.0,
                "wb_blue_gain": 1.0
            },
            recording_settings={
                "bitrate": 25000000,
                "quality": 23
            }
        )
        
        # Microscopy
        self.presets["Microscopy"] = MedicalPreset(
            name="Microscopy",
            description="Microscopic imaging with maximum detail and contrast",
            camera_settings={
                "brightness": 0.0,
                "contrast": 1.5,
                "saturation": 0.8,
                "sharpness": 2.0,
                "exposure_time": 15000,
                "analogue_gain": 1.0,
                "awb_mode": "daylight"
            },
            processing_settings={
                "gamma": 1.1,
                "brightness": 0,
                "contrast": 1.5,
                "saturation": 0.8,
                "wb_red_gain": 1.0,
                "wb_blue_gain": 1.0
            },
            recording_settings={
                "bitrate": 35000000,  # Very high bitrate for microscopy
                "quality": 18
            }
        )
        
        # Radiology
        self.presets["Radiology"] = MedicalPreset(
            name="Radiology",
            description="X-ray and imaging display with high contrast and grayscale optimization",
            camera_settings={
                "brightness": 0.0,
                "contrast": 1.6,
                "saturation": 0.5,
                "sharpness": 1.3,
                "exposure_time": 25000,
                "analogue_gain": 1.0,
                "awb_mode": "auto"
            },
            processing_settings={
                "gamma": 1.2,
                "brightness": 0,
                "contrast": 1.6,
                "saturation": 0.5,
                "wb_red_gain": 1.0,
                "wb_blue_gain": 1.0
            },
            recording_settings={
                "bitrate": 20000000,
                "quality": 25
            }
        )
        
        # Wound Assessment
        self.presets["Wound_Assessment"] = MedicalPreset(
            name="Wound Assessment",
            description="Wound documentation with accurate color representation and detail",
            camera_settings={
                "brightness": 8.0,
                "contrast": 1.25,
                "saturation": 1.15,
                "sharpness": 1.3,
                "exposure_time": 28000,
                "analogue_gain": 1.0,
                "awb_mode": "daylight"
            },
            processing_settings={
                "gamma": 0.95,
                "brightness": 5,
                "contrast": 1.25,
                "saturation": 1.15,
                "wb_red_gain": 1.05,
                "wb_blue_gain": 0.95
            },
            recording_settings={
                "bitrate": 25000000,
                "quality": 22
            }
        )
        
        # Dental
        self.presets["Dental"] = MedicalPreset(
            name="Dental",
            description="Oral examination with enhanced contrast and detail for dental structures",
            camera_settings={
                "brightness": 12.0,
                "contrast": 1.3,
                "saturation": 0.9,
                "sharpness": 1.4,
                "exposure_time": 22000,
                "analogue_gain": 1.1,
                "awb_mode": "fluorescent"
            },
            processing_settings={
                "gamma": 0.9,
                "brightness": 8,
                "contrast": 1.3,
                "saturation": 0.9,
                "wb_red_gain": 1.0,
                "wb_blue_gain": 1.05
            },
            recording_settings={
                "bitrate": 25000000,
                "quality": 21
            }
        )
        
        # Low Light
        self.presets["Low_Light"] = MedicalPreset(
            name="Low Light",
            description="Optimized for low-light medical environments",
            camera_settings={
                "brightness": 20.0,
                "contrast": 1.2,
                "saturation": 1.1,
                "sharpness": 1.1,
                "exposure_time": 50000,
                "analogue_gain": 2.0,
                "awb_mode": "auto"
            },
            processing_settings={
                "gamma": 0.8,
                "brightness": 20,
                "contrast": 1.2,
                "saturation": 1.1,
                "wb_red_gain": 1.0,
                "wb_blue_gain": 1.0
            },
            recording_settings={
                "bitrate": 25000000,
                "quality": 23
            }
        )
        
        self.logger.info(f"Initialized {len(self.presets)} medical presets")
        
    def get_preset(self, name: str) -> MedicalPreset:
        """Get a medical preset by name"""
        return self.presets.get(name)
        
    def get_preset_names(self) -> List[str]:
        """Get list of available preset names"""
        return list(self.presets.keys())
        
    def get_preset_descriptions(self) -> Dict[str, str]:
        """Get preset names and descriptions"""
        return {name: preset.description for name, preset in self.presets.items()}
        
    def add_custom_preset(self, preset: MedicalPreset):
        """Add a custom medical preset"""
        self.presets[preset.name] = preset
        self.logger.info(f"Added custom preset: {preset.name}")
        
    def remove_preset(self, name: str) -> bool:
        """Remove a preset"""
        if name in self.presets:
            del self.presets[name]
            self.logger.info(f"Removed preset: {name}")
            return True
        return False
        
    def get_preset_for_scenario(self, scenario: str) -> MedicalPreset:
        """Get recommended preset for a medical scenario"""
        scenario_mapping = {
            "surgery": "Surgery",
            "skin": "Dermatology",
            "eye": "Ophthalmology",
            "internal": "Endoscopy",
            "microscope": "Microscopy",
            "xray": "Radiology",
            "wound": "Wound_Assessment",
            "dental": "Dental",
            "dark": "Low_Light"
        }
        
        preset_name = scenario_mapping.get(scenario.lower(), "General")
        return self.presets.get(preset_name)
        
    def get_specialized_enhancements(self, preset_name: str) -> Dict[str, Any]:
        """Get specialized enhancement settings for a preset"""
        enhancements = {
            "Surgery": {
                "enhancement_type": "detail_enhancement",
                "noise_reduction": True,
                "color_accuracy": "high"
            },
            "Dermatology": {
                "enhancement_type": "skin_tone",
                "color_accuracy": "very_high",
                "texture_enhancement": True
            },
            "Ophthalmology": {
                "enhancement_type": "high_contrast",
                "vessel_enhancement": True,
                "detail_enhancement": True
            },
            "Endoscopy": {
                "enhancement_type": "vessel_enhancement",
                "low_light_optimization": True,
                "noise_reduction": True
            },
            "Microscopy": {
                "enhancement_type": "detail_enhancement",
                "sharpening": "maximum",
                "contrast_optimization": True
            },
            "Radiology": {
                "enhancement_type": "high_contrast",
                "grayscale_optimization": True,
                "edge_enhancement": True
            },
            "Wound_Assessment": {
                "enhancement_type": "skin_tone",
                "color_accuracy": "very_high",
                "detail_enhancement": True
            },
            "Dental": {
                "enhancement_type": "high_contrast",
                "detail_enhancement": True,
                "fluorescence_optimization": True
            },
            "Low_Light": {
                "enhancement_type": "low_light",
                "noise_reduction": True,
                "brightness_optimization": True
            }
        }
        
        return enhancements.get(preset_name, {})
        
    def optimize_for_camera_type(self, preset_name: str, camera_type: str) -> MedicalPreset:
        """Optimize preset for specific camera type"""
        preset = self.get_preset(preset_name)
        if not preset:
            return None
            
        # Create a copy for modification
        optimized_preset = MedicalPreset(
            name=f"{preset.name}_{camera_type}",
            description=f"{preset.description} (optimized for {camera_type})",
            camera_settings=preset.camera_settings.copy(),
            processing_settings=preset.processing_settings.copy(),
            recording_settings=preset.recording_settings.copy()
        )
        
        if camera_type == "picamera2":
            # Raspberry Pi optimizations
            optimized_preset.recording_settings["bitrate"] = min(
                optimized_preset.recording_settings["bitrate"], 20000000
            )
            optimized_preset.camera_settings["analogue_gain"] = min(
                optimized_preset.camera_settings.get("analogue_gain", 1.0), 2.0
            )
            
        elif camera_type == "opencv":
            # USB camera optimizations
            optimized_preset.camera_settings["exposure_time"] = min(
                optimized_preset.camera_settings.get("exposure_time", 33000), 40000
            )
            
        return optimized_preset
        
    def validate_preset(self, preset: MedicalPreset) -> List[str]:
        """Validate preset settings"""
        errors = []
        
        # Validate camera settings
        camera_settings = preset.camera_settings
        if camera_settings.get("brightness", 0) < -100 or camera_settings.get("brightness", 0) > 100:
            errors.append("Brightness out of range (-100 to 100)")
            
        if camera_settings.get("contrast", 1.0) < 0.1 or camera_settings.get("contrast", 1.0) > 3.0:
            errors.append("Contrast out of range (0.1 to 3.0)")
            
        if camera_settings.get("saturation", 1.0) < 0.0 or camera_settings.get("saturation", 1.0) > 3.0:
            errors.append("Saturation out of range (0.0 to 3.0)")
            
        # Validate processing settings
        processing_settings = preset.processing_settings
        if processing_settings.get("gamma", 1.0) < 0.1 or processing_settings.get("gamma", 1.0) > 5.0:
            errors.append("Gamma out of range (0.1 to 5.0)")
            
        # Validate recording settings
        recording_settings = preset.recording_settings
        if recording_settings.get("bitrate", 25000000) < 1000000 or recording_settings.get("bitrate", 25000000) > 100000000:
            errors.append("Bitrate out of range (1-100 Mbps)")
            
        return errors
        
    def export_preset(self, preset_name: str, file_path: str) -> bool:
        """Export preset to JSON file"""
        try:
            import json
            from dataclasses import asdict
            
            preset = self.get_preset(preset_name)
            if not preset:
                return False
                
            preset_data = asdict(preset)
            
            with open(file_path, 'w') as f:
                json.dump(preset_data, f, indent=4)
                
            self.logger.info(f"Exported preset {preset_name} to {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to export preset: {e}")
            return False
            
    def import_preset(self, file_path: str) -> bool:
        """Import preset from JSON file"""
        try:
            import json
            
            with open(file_path, 'r') as f:
                preset_data = json.load(f)
                
            preset = MedicalPreset(**preset_data)
            
            # Validate before adding
            errors = self.validate_preset(preset)
            if errors:
                self.logger.error(f"Invalid preset: {errors}")
                return False
                
            self.add_custom_preset(preset)
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to import preset: {e}")
            return False
            
    def get_preset_recommendations(self, image_analysis: Dict[str, float]) -> List[str]:
        """Get preset recommendations based on image analysis"""
        recommendations = []
        
        brightness = image_analysis.get("brightness", 128)
        contrast = image_analysis.get("contrast", 50)
        sharpness = image_analysis.get("sharpness", 100)
        
        # Low light detection
        if brightness < 80:
            recommendations.append("Low_Light")
            
        # High detail requirement
        if sharpness > 200:
            recommendations.extend(["Microscopy", "Surgery"])
            
        # Skin imaging
        if 100 < brightness < 150 and contrast > 40:
            recommendations.extend(["Dermatology", "Wound_Assessment"])
            
        # Default recommendation
        if not recommendations:
            recommendations.append("General")
            
        return recommendations[:3]  # Return top 3 recommendations