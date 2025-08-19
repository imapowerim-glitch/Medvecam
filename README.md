# MedVeCam Ultra 2.0 - Advanced Medical Camera System

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Overview

MedVeCam Ultra 2.0 is an advanced medical camera application designed for high-quality video recording and real-time imaging in medical environments. The system is optimized for both Raspberry Pi and desktop platforms, providing professional-grade features for medical documentation and procedures.

## ✨ New Features in Version 2.0

### 🎥 Enhanced Video Quality
- **2K Recording Support**: Native 2560x1440 recording resolution
- **High Bitrate**: Up to 25 Mbps for exceptional detail preservation
- **Optimized H264 Encoding**: Advanced codec settings for medical imaging
- **Multiple Resolution Options**: 2K, Full HD, HD, and VGA support

### ⚡ Performance Improvements
- **Optimized Preview**: Reduced buffering for real-time viewing
- **Multithreading**: Smooth operation with concurrent preview and recording
- **Memory Optimization**: Efficient resource usage for Raspberry Pi
- **Reduced Latency**: Minimized delays and stuttering

### 🏥 Medical Presets
- **10 Specialized Presets**: Surgery, Dermatology, Ophthalmology, Endoscopy, Microscopy, Radiology, Wound Assessment, Dental, Low Light, and General
- **Automatic Optimization**: Settings tuned for specific medical scenarios
- **Custom Presets**: Create and save your own configurations
- **Import/Export**: Share presets between systems

### 🎨 Advanced Color Correction
- **Gamma Correction**: Precise exposure adjustment
- **White Balance Fine-tuning**: Red and blue gain controls
- **Brightness/Contrast**: Real-time adjustments
- **Saturation Control**: Color intensity optimization
- **LUT Support**: Custom lookup tables for color grading

### 🖥️ Enhanced User Interface
- **Modern GUI**: Intuitive control panels and layout
- **Real-time Preview**: Live camera feed with optimized performance
- **Status Indicators**: Recording status, quality metrics, and performance monitoring
- **Control Panels**: Organized settings for quick access
- **Medical Enhancements**: Specialized processing for medical imaging

### 🔧 Technical Features
- **Automatic Camera Detection**: Supports both Raspberry Pi camera and USB webcams
- **Error Handling**: Robust camera error detection and recovery
- **Performance Monitoring**: FPS tracking and frame drop detection
- **Logging System**: Comprehensive logging for debugging
- **Configuration Management**: Persistent settings storage

## 🚀 Installation

### System Requirements
- Python 3.7 or higher
- OpenCV 4.8.0+
- 4GB RAM minimum (8GB recommended)
- For Raspberry Pi: Raspberry Pi 4 recommended

### Quick Start

1. **Clone the repository:**
```bash
git clone https://github.com/imapowerim-glitch/Medvecam.git
cd Medvecam
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **For Raspberry Pi, also install:**
```bash
pip install picamera2
```

4. **Run the application:**
```bash
python medvecam_ultra.py
```

## 📖 Usage

### Basic Operation

1. **Start the Application**: Run `python medvecam_ultra.py`
2. **Initialize Camera**: The system will auto-detect your camera
3. **Start Preview**: Click "Start Preview" to see live feed
4. **Select Preset**: Choose a medical preset appropriate for your use case
5. **Record Video**: Click "Start Recording" to begin capture
6. **Adjust Settings**: Use the control panels to fine-tune image quality

### Medical Presets Guide

| Preset | Best For | Key Features |
|--------|----------|--------------|
| **Surgery** | Operating room procedures | High detail, accurate colors, OR lighting |
| **Dermatology** | Skin examination | Enhanced skin tone, detail enhancement |
| **Ophthalmology** | Eye examination | High contrast, vessel enhancement |
| **Endoscopy** | Internal examination | Low-light optimization, brightness boost |
| **Microscopy** | Microscopic imaging | Maximum detail, high contrast |
| **Radiology** | X-ray display | Grayscale optimization, edge enhancement |
| **Wound Assessment** | Wound documentation | Color accuracy, texture detail |
| **Dental** | Oral examination | Fluorescent lighting, contrast enhancement |
| **Low Light** | Dark environments | Noise reduction, brightness optimization |
| **General** | Standard medical imaging | Balanced settings for general use |

### Advanced Features

#### Color Correction
- **Gamma**: Adjust overall brightness curve (0.5-3.0)
- **Brightness**: Linear brightness adjustment (-100 to +100)
- **Contrast**: Contrast enhancement (0.5-3.0)
- **Saturation**: Color intensity (0.0-3.0)
- **White Balance**: Fine-tune color temperature

#### Custom LUT Support
Load custom lookup tables for specialized color grading:
1. Prepare LUT file (.cube or image format)
2. Go to Settings → Advanced Settings
3. Load LUT file and enable LUT processing

#### Performance Optimization
- **Raspberry Pi Mode**: Automatically optimizes for limited resources
- **Desktop Mode**: Utilizes full system capabilities
- **Threading Control**: Adjust CPU core usage
- **Memory Management**: Configure buffer sizes

## 🏗️ Architecture

### Core Components

- **`medvecam_ultra.py`**: Main application and GUI
- **`config.py`**: Configuration management and settings
- **`camera_handler.py`**: Camera initialization and control
- **`video_processor.py`**: Advanced video processing and effects
- **`medical_presets.py`**: Medical imaging presets and optimizations

### Key Features

- **Modular Design**: Easily extensible architecture
- **Cross-Platform**: Supports Raspberry Pi and desktop systems
- **Error Recovery**: Robust error handling and logging
- **Real-time Processing**: Live preview with minimal latency

## 🔧 Configuration

### Camera Settings
```python
# Example camera configuration
camera_settings = {
    "resolution": (2560, 1440),
    "framerate": 30,
    "bitrate": 25000000,
    "brightness": 0.0,
    "contrast": 1.0,
    "saturation": 1.0
}
```

### Performance Tuning
```python
# Raspberry Pi optimization
config.optimize_for_raspberry_pi()

# Desktop optimization
config.optimize_for_desktop()
```

## 📊 Performance Metrics

### Video Quality
- **2K Resolution**: 2560x1440 @ 30fps
- **Bitrate**: Up to 25 Mbps
- **Codec**: H264 with medical-grade settings
- **Color Depth**: 8-bit RGB with enhanced processing

### System Performance
- **CPU Usage**: Optimized for Raspberry Pi 4
- **Memory Usage**: <512MB on Raspberry Pi
- **Latency**: <100ms preview delay
- **Frame Rate**: Stable 30fps recording

## 🛠️ Troubleshooting

### Common Issues

**Camera Not Detected**
- Ensure camera is properly connected
- Check camera permissions
- Try different USB ports (for webcams)

**Poor Performance**
- Use Raspberry Pi optimization mode
- Reduce preview resolution
- Close other applications

**Recording Fails**
- Check available disk space
- Verify write permissions
- Ensure stable power supply

### Debug Mode
Enable detailed logging by setting log level to DEBUG in configuration.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Install development dependencies
4. Make your changes
5. Run tests and ensure code quality
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/imapowerim-glitch/Medvecam/issues)
- **Documentation**: [Wiki](https://github.com/imapowerim-glitch/Medvecam/wiki)
- **Email**: support@medvecam.com

## 🙏 Acknowledgments

- OpenCV community for excellent computer vision tools
- Raspberry Pi Foundation for the picamera2 library
- Medical professionals who provided feedback and requirements

---

**MedVeCam Ultra 2.0** - Professional medical imaging for everyone.