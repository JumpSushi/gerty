#!/usr/bin/env python3
"""
GERTY Display - Windowed version for better macOS compatibility
"""

import cv2
import os
import time
import glob
import sys
from pathlib import Path


class GertyDisplay:
    def __init__(self):
        self.base_path = Path(__file__).parent / "gertycon"
        self.window_name = "GERTY"
        self.display_time = 2.0  # seconds per image
        
        # Screen resolution for GERTY (1024x600)
        self.target_width = 1024
        self.target_height = 600
        
    def setup_display(self):
        """Initialize the display window"""
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        # Set window size to match GERTY screen
        cv2.resizeWindow(self.window_name, self.target_width, self.target_height)
        
    def load_and_scale_image(self, image_path):
        """Load image and scale it to fit the target resolution"""
        img = cv2.imread(str(image_path))
        if img is None:
            print(f"Error loading image: {image_path}")
            return None
            
        # The images are already 1024x600, but let's ensure they're exactly right
        if img.shape[:2] != (self.target_height, self.target_width):
            img_scaled = cv2.resize(img, (self.target_width, self.target_height), interpolation=cv2.INTER_LANCZOS4)
        else:
            img_scaled = img
            
        return img_scaled
        
    def display_image(self, image_path, duration=None):
        """Display a single image for specified duration"""
        if duration is None:
            duration = self.display_time
            
        img = self.load_and_scale_image(image_path)
        if img is None:
            return False
        
        # Display the image
        cv2.imshow(self.window_name, img)
        cv2.waitKey(1)  # Force window refresh
        
        # Wait for duration with periodic checks for key presses
        start_time = time.time()
        while time.time() - start_time < duration:
            key = cv2.waitKey(50) & 0xFF  # Check every 50ms
            if key == 27:  # ESC key
                return False
            elif key == ord('q'):  # Q key
                return False
        return True
        
    def get_sorted_images(self, folder_path):
        """Get sorted list of images from a folder"""
        image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp']
        images = []
        
        for ext in image_extensions:
            images.extend(glob.glob(str(folder_path / ext)))
            
        return sorted(images)
        
    def boot_sequence(self):
        """Display boot sequence"""
        print("🤖 GERTY boot sequence initiated...")
        boot_path = self.base_path / "boot"
        boot_images = self.get_sorted_images(boot_path)
        
        for image_path in boot_images:
            filename = os.path.basename(image_path)
            print(f"   → {filename}")
            if not self.display_image(image_path, 3.0):  # Longer display for boot
                return False
        return True
        
    def emotion_cycle(self):
        """Cycle through emotion images"""
        print("😊 GERTY emotional display cycle...")
        emotion_path = self.base_path / "emotion"
        emotion_images = self.get_sorted_images(emotion_path)
        
        # Cycle through emotions
        cycles = 2
        for cycle in range(cycles):
            print(f"   Cycle {cycle + 1}/{cycles}")
            for image_path in emotion_images:
                filename = os.path.basename(image_path)
                print(f"   → {filename}")
                if not self.display_image(image_path, 1.5):  # Slightly faster emotions
                    return False
        return True
        
    def shutdown_sequence(self):
        """Display shutdown sequence"""
        print("🔌 GERTY shutdown sequence...")
        shutdown_path = self.base_path / "shutdown"
        shutdown_images = self.get_sorted_images(shutdown_path)
        
        for image_path in shutdown_images:
            filename = os.path.basename(image_path)
            print(f"   → {filename}")
            if not self.display_image(image_path, 4.0):  # Longer display for shutdown
                return False
        return True
        
    def run(self):
        """Main execution loop"""
        print("=" * 50)
        print("🤖 GERTY Display System v1.0")
        print("   Initializing emotional display interface...")
        print("   Press ESC or Q at any time to exit")
        print("=" * 50)
        
        try:
            self.setup_display()
            
            # Boot sequence
            if not self.boot_sequence():
                return
                
            time.sleep(1)  # Brief pause between sequences
                
            # Emotion cycle
            if not self.emotion_cycle():
                return
                
            time.sleep(1)  # Brief pause before shutdown
                
            # Shutdown sequence
            if not self.shutdown_sequence():
                return
                
            print("✅ Sequence complete. GERTY going offline...")
            time.sleep(2)  # Show final image a bit longer
            
        except KeyboardInterrupt:
            print("\n⚠️  Interrupted by user - Emergency shutdown")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            cv2.destroyAllWindows()
            print("🔌 GERTY Display System Offline")


def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print("GERTY Display System")
        print("Usage: python gerty_windowed.py")
        print("Controls:")
        print("  ESC or Q - Exit early")
        print("  Window can be resized/moved as needed")
        return
        
    gerty = GertyDisplay()
    gerty.run()


if __name__ == "__main__":
    main()
