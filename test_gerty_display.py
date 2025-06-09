#!/usr/bin/env python3
"""
Test suite for GERTY Display System
"""

import pytest
import cv2
import os
import tempfile
import numpy as np
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys

# Add the project root to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent))

from gerty_windowed import GertyDisplay


class TestGertyDisplay:
    """Test class for GERTY Display functionality"""
    
    @pytest.fixture
    def gerty_display(self):
        """Create a GertyDisplay instance for testing"""
        return GertyDisplay()
    
    @pytest.fixture
    def temp_image_dir(self):
        """Create temporary directory with test images"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create directory structure
            gertycon_dir = temp_path / "gertycon"
            boot_dir = gertycon_dir / "boot"
            emotion_dir = gertycon_dir / "emotion"
            shutdown_dir = gertycon_dir / "shutdown"
            
            boot_dir.mkdir(parents=True)
            emotion_dir.mkdir(parents=True)
            shutdown_dir.mkdir(parents=True)
            
            # Create test images (1024x600 pixels, matching GERTY specs)
            test_image = np.zeros((600, 1024, 3), dtype=np.uint8)
            test_image[:] = (50, 100, 150)  # Blue-ish color
            
            # Boot images
            cv2.imwrite(str(boot_dir / "boot1.jpg"), test_image)
            cv2.imwrite(str(boot_dir / "boot2.jpg"), test_image)
            
            # Emotion images
            for i in range(1, 9):
                cv2.imwrite(str(emotion_dir / f"g0{i}a.jpg"), test_image)
            
            # Shutdown image
            cv2.imwrite(str(shutdown_dir / "shut.jpg"), test_image)
            
            yield temp_path
    
    def test_init(self, gerty_display):
        """Test GertyDisplay initialization"""
        assert gerty_display.window_name == "GERTY"
        assert gerty_display.target_width == 1024
        assert gerty_display.target_height == 600
        assert gerty_display.display_time == 2.0
        assert isinstance(gerty_display.base_path, Path)
    
    def test_load_and_scale_image_success(self, gerty_display, temp_image_dir):
        """Test successful image loading and scaling"""
        # Update base path to temp directory
        gerty_display.base_path = temp_image_dir / "gertycon"
        
        test_image_path = temp_image_dir / "gertycon" / "boot" / "boot1.jpg"
        img = gerty_display.load_and_scale_image(test_image_path)
        
        assert img is not None
        assert img.shape == (600, 1024, 3)  # Height, Width, Channels
        assert img.dtype == np.uint8
    
    def test_load_and_scale_image_nonexistent(self, gerty_display):
        """Test loading non-existent image"""
        nonexistent_path = Path("/nonexistent/image.jpg")
        img = gerty_display.load_and_scale_image(nonexistent_path)
        assert img is None
    
    def test_get_sorted_images(self, gerty_display, temp_image_dir):
        """Test getting sorted list of images from directory"""
        boot_dir = temp_image_dir / "gertycon" / "boot"
        images = gerty_display.get_sorted_images(boot_dir)
        
        assert len(images) == 2
        assert all(str(img).endswith('.jpg') for img in images)
        assert images == sorted(images)  # Check they're sorted
    
    def test_get_sorted_images_empty_dir(self, gerty_display):
        """Test getting images from empty directory"""
        with tempfile.TemporaryDirectory() as temp_dir:
            empty_dir = Path(temp_dir)
            images = gerty_display.get_sorted_images(empty_dir)
            assert len(images) == 0
    
    @patch('cv2.imshow')
    @patch('cv2.waitKey')
    def test_display_image_success(self, mock_waitkey, mock_imshow, gerty_display, temp_image_dir):
        """Test successful image display"""
        # Setup mocks
        mock_waitkey.side_effect = [0] * 10 + [27]  # Return 0 several times, then ESC
        
        # Update base path
        gerty_display.base_path = temp_image_dir / "gertycon"
        
        test_image_path = temp_image_dir / "gertycon" / "boot" / "boot1.jpg"
        result = gerty_display.display_image(test_image_path, duration=0.1)  # Short duration for test
        
        # Should have called imshow at least once
        assert mock_imshow.called
        # Result depends on mock behavior, but should not crash
    
    @patch('cv2.imshow')
    @patch('cv2.waitKey', return_value=27)  # ESC key
    def test_display_image_esc_key(self, mock_waitkey, mock_imshow, gerty_display, temp_image_dir):
        """Test early exit with ESC key"""
        gerty_display.base_path = temp_image_dir / "gertycon"
        
        test_image_path = temp_image_dir / "gertycon" / "boot" / "boot1.jpg"
        result = gerty_display.display_image(test_image_path, duration=1.0)
        
        assert result == False  # Should return False for ESC
    
    @patch('cv2.imshow')
    @patch('cv2.waitKey', return_value=ord('q'))  # Q key
    def test_display_image_q_key(self, mock_waitkey, mock_imshow, gerty_display, temp_image_dir):
        """Test early exit with Q key"""
        gerty_display.base_path = temp_image_dir / "gertycon"
        
        test_image_path = temp_image_dir / "gertycon" / "boot" / "boot1.jpg"
        result = gerty_display.display_image(test_image_path, duration=1.0)
        
        assert result == False  # Should return False for Q
    
    @patch('cv2.namedWindow')
    @patch('cv2.resizeWindow')
    def test_setup_display(self, mock_resize, mock_named, gerty_display):
        """Test display setup"""
        gerty_display.setup_display()
        
        mock_named.assert_called_once_with("GERTY", cv2.WINDOW_NORMAL)
        mock_resize.assert_called_once_with("GERTY", 1024, 600)
    
    @patch.object(GertyDisplay, 'display_image', return_value=True)
    def test_boot_sequence(self, mock_display, gerty_display, temp_image_dir):
        """Test boot sequence execution"""
        gerty_display.base_path = temp_image_dir / "gertycon"
        
        result = gerty_display.boot_sequence()
        
        assert result == True
        assert mock_display.call_count == 2  # Two boot images
        
        # Check that images were called with correct duration
        calls = mock_display.call_args_list
        for call in calls:
            # Check positional and keyword arguments
            args, kwargs = call
            assert 'duration' in kwargs or len(args) >= 2
            if 'duration' in kwargs:
                assert kwargs['duration'] == 3.0  # Boot images should display for 3 seconds
            elif len(args) >= 2:
                assert args[1] == 3.0
    
    @patch.object(GertyDisplay, 'display_image', return_value=True)
    def test_emotion_cycle(self, mock_display, gerty_display, temp_image_dir):
        """Test emotion cycle execution"""
        gerty_display.base_path = temp_image_dir / "gertycon"
        
        result = gerty_display.emotion_cycle()
        
        assert result == True
        # Should cycle through emotions twice (2 cycles * 8 emotion images)
        assert mock_display.call_count == 16
        
        # Check duration for emotion images
        calls = mock_display.call_args_list
        for call in calls:
            args, kwargs = call
            assert 'duration' in kwargs or len(args) >= 2
            if 'duration' in kwargs:
                assert kwargs['duration'] == 1.5  # Emotion images should display for 1.5 seconds
            elif len(args) >= 2:
                assert args[1] == 1.5
    
    @patch.object(GertyDisplay, 'display_image', return_value=True)
    def test_shutdown_sequence(self, mock_display, gerty_display, temp_image_dir):
        """Test shutdown sequence execution"""
        gerty_display.base_path = temp_image_dir / "gertycon"
        
        result = gerty_display.shutdown_sequence()
        
        assert result == True
        assert mock_display.call_count == 1  # One shutdown image
        
        # Check duration for shutdown image
        call = mock_display.call_args_list[0]
        args, kwargs = call
        assert 'duration' in kwargs or len(args) >= 2
        if 'duration' in kwargs:
            assert kwargs['duration'] == 4.0  # Shutdown should display for 4 seconds
        elif len(args) >= 2:
            assert args[1] == 4.0
    
    @patch.object(GertyDisplay, 'display_image', return_value=False)  # Simulate early exit
    def test_sequences_early_exit(self, mock_display, gerty_display, temp_image_dir):
        """Test early exit from sequences"""
        gerty_display.base_path = temp_image_dir / "gertycon"
        
        # All sequences should return False if display_image returns False
        assert gerty_display.boot_sequence() == False
        assert gerty_display.emotion_cycle() == False
        assert gerty_display.shutdown_sequence() == False
    
    @patch.object(GertyDisplay, 'setup_display')
    @patch.object(GertyDisplay, 'boot_sequence', return_value=True)
    @patch.object(GertyDisplay, 'emotion_cycle', return_value=True)
    @patch.object(GertyDisplay, 'shutdown_sequence', return_value=True)
    @patch('cv2.destroyAllWindows')
    @patch('time.sleep')
    def test_run_complete_sequence(self, mock_sleep, mock_destroy, mock_shutdown, 
                                  mock_emotion, mock_boot, mock_setup, gerty_display):
        """Test complete run sequence"""
        gerty_display.run()
        
        # Verify all sequences were called
        mock_setup.assert_called_once()
        mock_boot.assert_called_once()
        mock_emotion.assert_called_once()
        mock_shutdown.assert_called_once()
        mock_destroy.assert_called_once()
    
    @patch.object(GertyDisplay, 'setup_display')
    @patch.object(GertyDisplay, 'boot_sequence', return_value=False)  # Simulate early exit
    @patch('cv2.destroyAllWindows')
    def test_run_early_exit(self, mock_destroy, mock_boot, mock_setup, gerty_display):
        """Test run method with early exit"""
        gerty_display.run()
        
        mock_setup.assert_called_once()
        mock_boot.assert_called_once()
        mock_destroy.assert_called_once()


class TestImageFiles:
    """Test the actual image files in the project"""
    
    def test_gertycon_directory_exists(self):
        """Test that gertycon directory exists"""
        gertycon_path = Path(__file__).parent / "gertycon"
        assert gertycon_path.exists(), "gertycon directory should exist"
        assert gertycon_path.is_dir(), "gertycon should be a directory"
    
    def test_boot_images_exist(self):
        """Test that boot images exist"""
        boot_path = Path(__file__).parent / "gertycon" / "boot"
        assert boot_path.exists(), "boot directory should exist"
        
        boot_images = list(boot_path.glob("*.jpg"))
        assert len(boot_images) >= 1, "Should have at least one boot image"
        
        for img_path in boot_images:
            assert img_path.stat().st_size > 0, f"Boot image {img_path.name} should not be empty"
    
    def test_emotion_images_exist(self):
        """Test that emotion images exist"""
        emotion_path = Path(__file__).parent / "gertycon" / "emotion"
        assert emotion_path.exists(), "emotion directory should exist"
        
        emotion_images = list(emotion_path.glob("*.jpg"))
        assert len(emotion_images) >= 1, "Should have at least one emotion image"
        
        for img_path in emotion_images:
            assert img_path.stat().st_size > 0, f"Emotion image {img_path.name} should not be empty"
    
    def test_shutdown_images_exist(self):
        """Test that shutdown images exist"""
        shutdown_path = Path(__file__).parent / "gertycon" / "shutdown"
        assert shutdown_path.exists(), "shutdown directory should exist"
        
        shutdown_images = list(shutdown_path.glob("*.jpg"))
        assert len(shutdown_images) >= 1, "Should have at least one shutdown image"
        
        for img_path in shutdown_images:
            assert img_path.stat().st_size > 0, f"Shutdown image {img_path.name} should not be empty"
    
    def test_image_dimensions(self):
        """Test that images have correct dimensions (1024x600)"""
        gertycon_path = Path(__file__).parent / "gertycon"
        
        # Test a few sample images
        test_images = []
        
        # Add boot images
        boot_path = gertycon_path / "boot"
        if boot_path.exists():
            test_images.extend(list(boot_path.glob("*.jpg"))[:1])  # Test first boot image
        
        # Add emotion images
        emotion_path = gertycon_path / "emotion"
        if emotion_path.exists():
            test_images.extend(list(emotion_path.glob("*.jpg"))[:2])  # Test first two emotion images
        
        # Add shutdown images
        shutdown_path = gertycon_path / "shutdown"
        if shutdown_path.exists():
            test_images.extend(list(shutdown_path.glob("*.jpg"))[:1])  # Test shutdown image
        
        for img_path in test_images:
            img = cv2.imread(str(img_path))
            assert img is not None, f"Should be able to load {img_path.name}"
            
            height, width = img.shape[:2]
            assert width == 1024, f"{img_path.name} width should be 1024, got {width}"
            assert height == 600, f"{img_path.name} height should be 600, got {height}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
