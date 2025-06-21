#!/usr/bin/env python3
"""
pytest configuration for GERTY Simple Voice Assistant tests
Provides fixtures and mocks for testing the voice assistant functionality
Handles missing audio dependencies gracefully for CI/CD environments
"""

import pytest
import sys
import os
import tempfile
import importlib
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Check for optional dependencies
def check_audio_dependencies():
    """Check if audio dependencies are available"""
    dependencies = {
        'pyaudio': False,
        'pvporcupine': False,
        'speech_recognition': False,
        'opencv': False,
        'numpy': False
    }
    
    for dep in dependencies:
        try:
            if dep == 'opencv':
                importlib.import_module('cv2')
            else:
                importlib.import_module(dep)
            dependencies[dep] = True
        except ImportError:
            pass
    
    return dependencies

# Global dependency check
AVAILABLE_DEPS = check_audio_dependencies()

# Configure pytest
def pytest_configure(config):
    """Configure pytest settings"""
    config.addinivalue_line(
        "markers", 
        "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers",
        "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers",
        "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers",
        "audio: marks tests that require audio hardware/dependencies"
    )
    config.addinivalue_line(
        "markers",
        "porcupine: marks tests that require Porcupine API key"
    )
    config.addinivalue_line(
        "markers",
        "requires_deps: marks tests that require specific dependencies"
    )

# Project-wide fixtures
@pytest.fixture(scope="session")
def project_root():
    """Get the project root directory"""
    return Path(__file__).parent

@pytest.fixture(scope="session")
def gertycon_path(project_root):
    """Get the gertycon directory path"""
    return project_root / "gertycon"

@pytest.fixture(scope="session")
def available_dependencies():
    """Get information about available dependencies"""
    return AVAILABLE_DEPS

@pytest.fixture(scope="session")
def test_images_exist(gertycon_path):
    """Check if test images exist"""
    emotion_path = gertycon_path / "emotion"
    boot_path = gertycon_path / "boot"
    
    return {
        "emotion_images": list(emotion_path.glob("*.jpg")) if emotion_path.exists() else [],
        "boot_images": list(boot_path.glob("*.jpg")) if boot_path.exists() else [],
        "has_emotion": emotion_path.exists() and len(list(emotion_path.glob("*.jpg"))) > 0,
        "has_boot": boot_path.exists() and len(list(boot_path.glob("*.jpg"))) > 0
    }

# Mock fixtures for external dependencies
@pytest.fixture
def mock_opencv():
    """Mock OpenCV functionality"""
    if AVAILABLE_DEPS['opencv'] and AVAILABLE_DEPS['numpy']:
        # Use real OpenCV/numpy if available for better testing
        import cv2
        import numpy as np
        mock_image = np.zeros((600, 1024, 3), dtype=np.uint8)
        
        with patch('cv2.imshow') as mock_imshow, \
             patch('cv2.waitKey') as mock_waitkey, \
             patch('cv2.namedWindow') as mock_namedwindow, \
             patch('cv2.resizeWindow') as mock_resizewindow, \
             patch('cv2.destroyAllWindows') as mock_destroywindows:
            
            mock_waitkey.return_value = -1  # No key pressed
            
            yield {
                'imread': cv2.imread,  # Use real imread
                'imshow': mock_imshow,
                'waitKey': mock_waitkey,
                'namedWindow': mock_namedwindow,
                'resizeWindow': mock_resizewindow,
                'destroyAllWindows': mock_destroywindows,
                'resize': cv2.resize,  # Use real resize
                'mock_image': mock_image
            }
    else:
        # Full mock when dependencies not available
        with patch('cv2.imread') as mock_imread, \
             patch('cv2.imshow') as mock_imshow, \
             patch('cv2.waitKey') as mock_waitkey, \
             patch('cv2.namedWindow') as mock_namedwindow, \
             patch('cv2.resizeWindow') as mock_resizewindow, \
             patch('cv2.destroyAllWindows') as mock_destroywindows, \
             patch('cv2.resize') as mock_resize:
            
            # Create mock image data using Python lists (no numpy)
            mock_image = [[[0 for _ in range(3)] for _ in range(1024)] for _ in range(600)]
            mock_imread.return_value = mock_image
            mock_resize.return_value = mock_image
            mock_waitkey.return_value = -1
            
            yield {
                'imread': mock_imread,
                'imshow': mock_imshow,
                'waitKey': mock_waitkey,
                'namedWindow': mock_namedwindow,
                'resizeWindow': mock_resizewindow,
                'destroyAllWindows': mock_destroywindows,
                'resize': mock_resize,
                'mock_image': mock_image
            }

@pytest.fixture
def mock_speech_recognition():
    """Mock speech recognition functionality"""
    with patch('speech_recognition.Recognizer') as mock_recognizer_class, \
         patch('speech_recognition.Microphone') as mock_microphone_class:
        
        # Create mock instances
        mock_recognizer = Mock()
        mock_microphone = Mock()
        mock_recognizer_class.return_value = mock_recognizer
        mock_microphone_class.return_value = mock_microphone
        
        # Mock microphone context manager
        mock_microphone.__enter__ = Mock(return_value=mock_microphone)
        mock_microphone.__exit__ = Mock(return_value=None)
        
        # Mock speech recognition methods
        mock_recognizer.adjust_for_ambient_noise = Mock()
        mock_recognizer.listen = Mock()
        mock_recognizer.recognize_google = Mock(return_value="test speech")
        
        yield {
            'recognizer_class': mock_recognizer_class,
            'microphone_class': mock_microphone_class,
            'recognizer': mock_recognizer,
            'microphone': mock_microphone
        }

@pytest.fixture
def mock_porcupine():
    """Mock Porcupine wake word detection"""
    with patch('pvporcupine.create') as mock_create:
        mock_porcupine = Mock()
        mock_create.return_value = mock_porcupine
        
        # Mock Porcupine properties and methods
        mock_porcupine.sample_rate = 16000
        mock_porcupine.frame_length = 512
        mock_porcupine.process = Mock(return_value=-1)  # No wake word detected
        mock_porcupine.delete = Mock()
        
        yield {
            'create': mock_create,
            'instance': mock_porcupine
        }

@pytest.fixture
def mock_pyaudio():
    """Mock PyAudio functionality - handles missing PortAudio gracefully"""
    with patch('pyaudio.PyAudio') as mock_pyaudio_class:
        mock_pyaudio = Mock()
        mock_stream = Mock()
        
        mock_pyaudio_class.return_value = mock_pyaudio
        mock_pyaudio.open.return_value = mock_stream
        
        # Mock audio stream methods
        mock_stream.is_active.return_value = True
        mock_stream.start_stream = Mock()
        mock_stream.stop_stream = Mock()
        mock_stream.close = Mock()
        mock_stream.read = Mock(return_value=b'\x00' * 1024)  # Mock audio data
        
        mock_pyaudio.terminate = Mock()
        
        # Mock constants that might be needed
        with patch('pyaudio.paInt16', 8):
            yield {
                'pyaudio_class': mock_pyaudio_class,
                'pyaudio': mock_pyaudio,
                'stream': mock_stream
            }

@pytest.fixture
def mock_requests():
    """Mock requests for AI API calls"""
    with patch('requests.post') as mock_post:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{'message': {'content': 'Test AI response'}}]
        }
        mock_post.return_value = mock_response
        
        yield {
            'post': mock_post,
            'response': mock_response
        }

@pytest.fixture
def mock_all_external_deps(mock_opencv, mock_speech_recognition, mock_porcupine, mock_pyaudio, mock_requests):
    """Mock all external dependencies at once"""
    return {
        'opencv': mock_opencv,
        'speech_recognition': mock_speech_recognition,
        'porcupine': mock_porcupine,
        'pyaudio': mock_pyaudio,
        'requests': mock_requests
    }

# GERTY-specific fixtures
@pytest.fixture
def gerty_instance(mock_all_external_deps):
    """Create a GERTY instance with all dependencies mocked"""
    # Only import and create if we can handle missing dependencies
    try:
        from gerty_simple_voice import GERTYSimpleVoice
        
        # Patch signal handlers to avoid interference with tests
        with patch('signal.signal'):
            gerty = GERTYSimpleVoice()
            gerty.setup_display()
            gerty.setup_voice()
            return gerty
    except ImportError as e:
        pytest.skip(f"Cannot import GERTYSimpleVoice: {e}")

@pytest.fixture
def gerty_with_porcupine(gerty_instance, mock_porcupine):
    """Create a GERTY instance with Porcupine set up"""
    if gerty_instance:
        gerty_instance.setup_porcupine()
        return gerty_instance
    else:
        pytest.skip("GERTY instance not available")

@pytest.fixture
def temp_image_file():
    """Create a temporary image file for testing"""
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
        if AVAILABLE_DEPS['opencv'] and AVAILABLE_DEPS['numpy']:
            # Create a real test image if OpenCV is available
            import cv2
            import numpy as np
            test_image = np.zeros((600, 1024, 3), dtype=np.uint8)
            cv2.imwrite(f.name, test_image)
        else:
            # Create a fake image file
            f.write(b'fake image data')
        yield f.name
    
    # Clean up
    try:
        os.unlink(f.name)
    except FileNotFoundError:
        pass

@pytest.fixture
def mock_wake_word_detection():
    """Mock wake word detection for testing"""
    def trigger_wake_word(gerty_instance):
        """Helper function to trigger wake word detection"""
        if gerty_instance:
            gerty_instance.wake_word_detected = True
            return True
        return False
    
    return trigger_wake_word

@pytest.fixture
def audio_test_data():
    """Generate test audio data"""
    if AVAILABLE_DEPS['numpy']:
        import numpy as np
        # Generate some test PCM data (16-bit signed integers)
        sample_rate = 16000
        duration = 1.0  # 1 second
        frequency = 440  # A4 note
        
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio_data = np.sin(2 * np.pi * frequency * t) * 32767
        audio_data = audio_data.astype(np.int16)
        
        return {
            'pcm_data': audio_data,
            'sample_rate': sample_rate,
            'duration': duration,
            'frequency': frequency
        }
    else:
        # Fallback without numpy
        return {
            'pcm_data': [0] * 16000,  # 1 second of silence
            'sample_rate': 16000,
            'duration': 1.0,
            'frequency': 440
        }

# Test environment setup
@pytest.fixture(autouse=True)
def setup_test_environment():
    """Set up test environment variables"""
    # Disable display for headless testing
    if 'DISPLAY' not in os.environ:
        os.environ['DISPLAY'] = ':99'  # Use virtual display
    
    # Set environment variable to indicate we're in test mode
    os.environ['GERTY_TEST_MODE'] = '1'
    
    yield
    
    # Cleanup
    if 'GERTY_TEST_MODE' in os.environ:
        del os.environ['GERTY_TEST_MODE']

# Dependency check fixtures
@pytest.fixture
def skip_if_no_audio():
    """Skip test if audio dependencies are not available"""
    if not (AVAILABLE_DEPS['pyaudio'] and AVAILABLE_DEPS['speech_recognition']):
        pytest.skip("Audio dependencies (PyAudio, SpeechRecognition) not available")

@pytest.fixture  
def skip_if_no_porcupine():
    """Skip test if Porcupine is not available"""
    if not AVAILABLE_DEPS['pvporcupine']:
        pytest.skip("Porcupine dependency not available")

@pytest.fixture
def skip_if_no_opencv():
    """Skip test if OpenCV is not available"""
    if not AVAILABLE_DEPS['opencv']:
        pytest.skip("OpenCV dependency not available")

# Helper functions for tests
def create_mock_image(width=1024, height=600, channels=3):
    """Create a mock image for testing"""
    if AVAILABLE_DEPS['numpy']:
        import numpy as np
        return np.zeros((height, width, channels), dtype=np.uint8)
    else:
        # Fallback without numpy
        return [[[0 for _ in range(channels)] for _ in range(width)] for _ in range(height)]

def create_mock_audio_frame(frame_length=512):
    """Create mock audio frame data"""
    return [0] * frame_length  # Silent audio frame

# Custom pytest markers for dependency management
def pytest_collection_modifyitems(config, items):
    """Automatically mark tests based on dependencies"""
    for item in items:
        # Mark tests that use audio features
        if any(fixture in item.fixturenames for fixture in ['mock_pyaudio', 'mock_speech_recognition', 'skip_if_no_audio']):
            item.add_marker(pytest.mark.audio)
        
        # Mark tests that use Porcupine
        if any(fixture in item.fixturenames for fixture in ['mock_porcupine', 'skip_if_no_porcupine']):
            item.add_marker(pytest.mark.porcupine)
        
        # Mark tests that use OpenCV
        if any(fixture in item.fixturenames for fixture in ['mock_opencv', 'skip_if_no_opencv']):
            item.add_marker(pytest.mark.requires_deps)
