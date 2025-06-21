#!/usr/bin/env python3
"""
GERTY Simple Voice Assistant with Porcupine Wake Word Detection
Uses custom "Hey GERTY" wake word model with always-on microphone
"""

import cv2
import os
import time
import glob
import sys
import requests
import speech_recognition as sr
import pvporcupine
import pyaudio
import struct
import threading
import signal
from pathlib import Path
from typing import Optional


class GERTYSimpleVoice:
    def __init__(self):
        self.base_path = Path(__file__).parent / "gertycon"
        self.window_name = "GERTY"
        self.display_time = 2.0
        
        # Screen resolution for GERTY (1024x600)
        self.target_width = 1024
        self.target_height = 600
        
        # Voice components
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # AI API configuration
        self.ai_api_url = "https://ai.hackclub.com/chat/completions"
        self.ai_headers = {"Content-Type": "application/json"}
        
        # Porcupine wake word detection
        self.porcupine = None
        self.pa = None
        self.audio_stream = None
        self.wake_word_detected = False
        self.wake_word_thread = None
        self.listening_for_wake_word = False
        
        # Current state
        self.is_processing = False
        
        # Setup signal handler for clean shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
    def _signal_handler(self, signum, frame):
        """Handle signals for clean shutdown"""
        print(f"\n[STOP] Received signal {signum}, cleaning up...")
        self.cleanup_porcupine()
        cv2.destroyAllWindows()
        sys.exit(0)
        
    def setup_display(self):
        """Initialize the display window"""
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window_name, self.target_width, self.target_height)
        
    def setup_voice(self):
        """Initialize voice components"""
        print("<MIC> Setting up voice recognition...")
        
        # Adjust for ambient noise
        try:
            with self.microphone as source:
                print("   Calibrating microphone for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("   <OK> Voice recognition ready")
        except Exception as e:
            print(f"   <WARNING> Voice setup error: {e}")
    
    def setup_porcupine(self):
        """Initialize Porcupine wake word detection"""
        try:
            print("<PORCUPINE> Setting up Porcupine wake word detection...")
            
            # Clean up any existing instances first
            if self.porcupine:
                self.cleanup_porcupine()
            
            # Use your actual access key with custom "Hey GERTY" model
            keyword_path = str(Path(__file__).parent / "Hey-Goodie_en_mac_v3_0_0.ppn")
            print(f"   <FILE> Using custom keyword model: {keyword_path}")
            
            self.porcupine = pvporcupine.create(
                access_key="fill in with your access key :)",
                keyword_paths=[keyword_path]
            )
            
            # Initialize PyAudio with error handling
            try:
                self.pa = pyaudio.PyAudio()
            except Exception as e:
                print(f"   <ERROR> PyAudio initialization failed: {e}")
                return False
            
            # Create audio stream with error handling
            try:
                self.audio_stream = self.pa.open(
                    rate=self.porcupine.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=self.porcupine.frame_length,
                    input_device_index=None,  # Use default input device
                    stream_callback=None,
                    start=False  # Don't start immediately
                )
                # Start the stream after creation
                self.audio_stream.start_stream()
            except Exception as e:
                print(f"   <ERROR> Audio stream creation failed: {e}")
                if self.pa:
                    self.pa.terminate()
                return False
            
            print("   <OK> Porcupine wake word detection ready!")
            print("   <SPEAK> Say 'Hey GERTY' to activate voice assistant")
            print(f"   <INFO> Sample rate: {self.porcupine.sample_rate} Hz")
            print(f"   <INFO> Frame length: {self.porcupine.frame_length}")
            return True
            
        except Exception as e:
            print(f"   <ERROR> Porcupine setup failed: {e}")
            return False
    
    def _try_porcupine_setup(self):
        """Try to setup Porcupine (will likely fail without access key)"""
        try:
            print("� Attempting Porcupine wake word detection...")
            
            # Use your actual access key
            self.porcupine = pvporcupine.create(
                access_key="UCYx0gb2QXm8bIoLa5JmCaSRiBwvL6UHUyArrY3EFJ4C1xyb8Mo8SA==",
                keywords=['Hey GERTY']
            )
            
            self.pa = pyaudio.PyAudio()
            self.audio_stream = self.pa.open(
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.porcupine.frame_length
            )
            
            print("   ✅ Porcupine wake word detection ready!")
            print("   📢 Say 'Picovoice' to activate GERTY")
            return True
            
        except Exception as e:
            print(f"   ⚠️  Porcupine setup failed: {str(e)[:100]}...")
            return False
    
    def wake_word_listener(self):
        """Background thread for wake word detection"""
        print("<LISTEN> Wake word listener started...")
        
        while self.listening_for_wake_word:
            try:
                if self.audio_stream:
                    # Ensure stream is active before reading
                    if not self.audio_stream.is_active():
                        try:
                            self.audio_stream.start_stream()
                            print("<STREAM> Audio stream restarted")
                        except Exception as start_error:
                            print(f"<WARNING> Failed to restart audio stream: {start_error}")
                            time.sleep(0.5)
                            continue
                    
                    # Read audio frame with proper error handling
                    try:
                        pcm = self.audio_stream.read(
                            self.porcupine.frame_length, 
                            exception_on_overflow=False
                        )
                        pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
                        
                        # Process audio frame
                        keyword_index = self.porcupine.process(pcm)
                        
                        if keyword_index >= 0 and not self.is_processing:
                            print("<WAKE> Wake word detected!")
                            self.wake_word_detected = True
                    except Exception as stream_error:
                        if self.listening_for_wake_word:
                            print(f"<WARNING> Audio stream read error: {stream_error}")
                        time.sleep(0.1)
                else:
                    # Stream not available, wait a bit
                    time.sleep(0.1)
                        
            except Exception as e:
                if self.listening_for_wake_word:  # Only print if we're still supposed to be listening
                    print(f"<WARNING> Wake word detection error: {e}")
                time.sleep(0.1)
                
        print("<LISTEN> Wake word listener stopped")
    
    def start_wake_word_detection(self):
        """Start the Porcupine wake word detection in a background thread"""
        if self.porcupine and self.audio_stream:
            # Don't start if already listening
            if self.listening_for_wake_word:
                print("<INFO> Wake word detection already active")
                return True
                
            self.listening_for_wake_word = True
            self.wake_word_thread = threading.Thread(target=self.wake_word_listener, daemon=True)
            self.wake_word_thread.start()
            return True
        return False
    
    def stop_wake_word_detection(self):
        """Stop wake word detection"""
        self.listening_for_wake_word = False
        if self.wake_word_thread:
            self.wake_word_thread.join(timeout=1)
    
    def cleanup_porcupine(self):
        """Clean up Porcupine resources safely"""
        try:
            print("<CLEANUP> Cleaning up Porcupine resources...")
            
            # Stop wake word detection first
            self.stop_wake_word_detection()
            
            # Stop and close audio stream
            if hasattr(self, 'audio_stream') and self.audio_stream:
                try:
                    if self.audio_stream.is_active():
                        self.audio_stream.stop_stream()
                        print("   <OK> Audio stream stopped")
                    self.audio_stream.close()
                    print("   <OK> Audio stream closed")
                except Exception as e:
                    print(f"   <WARNING> Audio stream close error: {e}")
                finally:
                    self.audio_stream = None
                
            # Terminate PyAudio
            if hasattr(self, 'pa') and self.pa:
                try:
                    self.pa.terminate()
                    print("   <OK> PyAudio terminated")
                except Exception as e:
                    print(f"   <WARNING> PyAudio terminate error: {e}")
                finally:
                    self.pa = None
                
            # Delete Porcupine instance
            if hasattr(self, 'porcupine') and self.porcupine:
                try:
                    self.porcupine.delete()
                    print("   <OK> Porcupine instance deleted")
                except Exception as e:
                    print(f"   <WARNING> Porcupine delete error: {e}")
                finally:
                    self.porcupine = None
                
            # Small delay to ensure cleanup completes
            time.sleep(0.1)
                
        except Exception as e:
            print(f"<WARNING> Cleanup error: {e}")
            
    def load_and_scale_image(self, image_path):
        """Load image and scale it to fit the target resolution"""
        img = cv2.imread(str(image_path))
        if img is None:
            print(f"Error loading image: {image_path}")
            return None
            
        if img.shape[:2] != (self.target_height, self.target_width):
            img_scaled = cv2.resize(img, (self.target_width, self.target_height), interpolation=cv2.INTER_LANCZOS4)
        else:
            img_scaled = img
            
        return img_scaled
        
    def display_image(self, image_path, duration=None, show_text=None, check_wake_word=False):
        """Display a single image for specified duration with optional text overlay"""
        if duration is None:
            duration = self.display_time
            
        img = self.load_and_scale_image(image_path)
        if img is None:
            return False
        
        # Add text overlay if provided
        if show_text:
            # Create a copy to avoid modifying the original
            img_with_text = img.copy()
            
            # Add semi-transparent black background for text
            overlay = img_with_text.copy()
            cv2.rectangle(overlay, (50, self.target_height - 150), 
                         (self.target_width - 50, self.target_height - 50), 
                         (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.7, img_with_text, 0.3, 0, img_with_text)
            
            # Add text
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.8
            color = (255, 255, 255)  # White text
            thickness = 2
            
            # Split long text into multiple lines
            words = show_text.split(' ')
            lines = []
            current_line = ""
            max_chars = 50  # Approximate characters per line
            
            for word in words:
                if len(current_line + word) < max_chars:
                    current_line += word + " "
                else:
                    if current_line:
                        lines.append(current_line.strip())
                    current_line = word + " "
            if current_line:
                lines.append(current_line.strip())
            
            # Draw each line
            y_start = self.target_height - 120
            line_height = 30
            for i, line in enumerate(lines[:3]):  # Max 3 lines
                y_pos = y_start + (i * line_height)
                cv2.putText(img_with_text, line, (70, y_pos), font, font_scale, color, thickness)
            
            img = img_with_text
        
        cv2.imshow(self.window_name, img)
        cv2.waitKey(1)
        
        start_time = time.time()
        while time.time() - start_time < duration:
            key = cv2.waitKey(50) & 0xFF
            if key == 27 or key == ord('q'):  # ESC or Q
                return False
            elif key == ord(' '):  # Space bar for manual activation (backup)
                return "activate"
            
            # Check for wake word detection
            if check_wake_word and self.wake_word_detected:
                self.wake_word_detected = False  # Reset flag
                return "wake_word"
                
        return True
        
    def display_emotion(self, emotion_type="neutral", duration=2.0, text=None, check_wake_word=False):
        """Display a specific emotion"""
        emotion_path = self.base_path / "emotion"
        emotion_images = sorted(glob.glob(str(emotion_path / "*.jpg")))
        
        if emotion_images:
            # Map emotions to different images
            emotion_map = {
                "neutral": 0,
                "happy": min(1, len(emotion_images)-1),
                "thinking": min(2, len(emotion_images)-1),
                "listening": min(3, len(emotion_images)-1),
                "sad": min(4, len(emotion_images)-1),
                "confused": min(5, len(emotion_images)-1)
            }
            
            image_index = emotion_map.get(emotion_type, 0)
            image_path = emotion_images[image_index]
            return self.display_image(image_path, duration, text, check_wake_word)
        return True
        
    def listen_for_speech(self, timeout=5):
        """Listen for speech and convert to text"""
        try:
            print("<MIC> Listening for your question...")
            
            # Temporarily pause Porcupine audio stream to avoid microphone conflicts on macOS
            audio_was_paused = False
            if self.listening_for_wake_word and self.audio_stream:
                print("<PAUSE> Temporarily pausing audio stream for speech recognition...")
                if self.pause_audio_stream():
                    audio_was_paused = True
                    time.sleep(0.3)  # Brief delay to ensure audio stream is fully released
            
            # Use a completely separate microphone instance for speech recognition
            temp_recognizer = sr.Recognizer()
            temp_microphone = sr.Microphone()
            
            with temp_microphone as source:
                # Adjust for ambient noise quickly
                temp_recognizer.adjust_for_ambient_noise(source, duration=0.5)
                # Listen for audio with timeout
                audio = temp_recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
                
            print("<PROCESS> Processing speech...")
            
            # Use Google's speech recognition
            text = temp_recognizer.recognize_google(audio)
            print(f"<TEXT> You said: '{text}'")
            
            # Resume Porcupine audio stream if it was paused
            if audio_was_paused:
                print("<RESUME> Resuming audio stream...")
                time.sleep(0.2)  # Brief delay before resuming
                self.resume_audio_stream()
            
            return text
            
        except sr.WaitTimeoutError:
            print("<TIMEOUT> No speech detected within timeout")
            # Resume audio stream if it was paused
            if audio_was_paused:
                print("<RESUME> Resuming audio stream after timeout...")
                time.sleep(0.2)
                self.resume_audio_stream()
            return None
        except sr.UnknownValueError:
            print("<UNKNOWN> Could not understand the audio")
            # Resume audio stream if it was paused
            if audio_was_paused:
                print("<RESUME> Resuming audio stream after unknown audio...")
                time.sleep(0.2)
                self.resume_audio_stream()
            return None
        except sr.RequestError as e:
            print(f"<ERROR> Speech recognition error: {e}")
            # Resume audio stream if it was paused
            if audio_was_paused:
                print("<RESUME> Resuming audio stream after error...")
                time.sleep(0.2)
                self.resume_audio_stream()
            return None
            
    def ask_ai(self, question: str) -> Optional[str]:
        """Send question to AI and get response"""
        try:
            print(f"<AI> Asking AI: {question}")
            
            payload = {
                "messages": [{"role": "user", "content": "you are in an embedded machine named GERTY from the movie moon. Please respond concisely, and act like how a human would speak. Imagine that you are talking to Sam Bell. " + question}]
            }
            
            response = requests.post(
                self.ai_api_url,
                headers=self.ai_headers,
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data.get('choices', [{}])[0].get('message', {}).get('content', '')
                print(f"<AI> AI response: {ai_response}")
                return ai_response
            else:
                print(f"<ERROR> AI API error: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"<ERROR> Error communicating with AI: {e}")
            return None
            
    def boot_sequence(self):
        """Display boot sequence"""
        print("<SYSTEM> GERTY boot sequence initiated...")
        boot_path = self.base_path / "boot"
        boot_images = sorted(glob.glob(str(boot_path / "*.jpg")))
        
        for image_path in boot_images:
            filename = os.path.basename(image_path)
            print(f"   -> {filename}")
            if not self.display_image(image_path, 3.0):
                return False
        return True
        
    def voice_interaction_loop(self):
        """Main voice interaction loop with wake word detection"""
        print("<MIC> Voice interaction ready with Porcupine wake word detection!")
        print("   Say 'Hey GERTY' to activate voice assistant")
        print("   Press SPACE for manual activation, ESC or Q to exit")
        
        # Start wake word detection - keep it running continuously
        if not self.start_wake_word_detection():
            print("<ERROR> Failed to start wake word detection, falling back to keyboard activation")
            return self.keyboard_interaction_loop()
        
        while True:
            # Display idle state - always listening for wake word
            result = self.display_emotion("neutral", 0.5, "Listening for 'Hey GERTY'...", check_wake_word=True)
            
            if result == "wake_word" or result == "activate":
                print("<WAKE> GERTY activated!")
                
                # DON'T pause wake word detection - keep microphone always on
                # Just set a flag to prevent multiple activations
                self.is_processing = True
                
                # Voice interaction activated
                self.display_emotion("listening", 1.0, "Listening...")
                
                # Listen for user's question
                question = self.listen_for_speech()
                
                if question:
                    # Show thinking state
                    self.display_emotion("thinking", 2.0, "Let me think about that...")
                    
                    # Get AI response
                    ai_response = self.ask_ai(question)
                    
                    if ai_response:
                        # Display the response
                        print(f"<SPEAK> GERTY says: {ai_response}")
                        self.display_emotion("happy", 5.0, ai_response)
                    else:
                        self.display_emotion("sad", 3.0, "Sorry, I couldn't get a response")
                else:
                    self.display_emotion("confused", 3.0, "Sorry, I didn't hear anything")
                
                # Reset processing flag - wake word detection continues automatically
                self.is_processing = False
                print("<LISTEN> Ready for next wake word...")
                
                # Small delay to ensure speech recognition resources are properly released
                time.sleep(0.3)
                    
            elif result == False:  # ESC or Q pressed
                break
    
    def keyboard_interaction_loop(self):
        """Fallback interaction loop using keyboard activation"""
        print("<MIC> Voice interaction ready (keyboard mode)!")
        print("   Press SPACE to activate voice assistant")
        print("   Press ESC or Q to exit")
        
        while True:
            # Display idle state with instructions
            result = self.display_emotion("neutral", 0.5, "Press SPACE to talk to me!")
            
            if result == "activate":
                # Voice interaction activated
                self.display_emotion("listening", 1.0, "Listening...")
                
                # Listen for user's question
                question = self.listen_for_speech()
                
                if question:
                    # Show thinking state
                    self.display_emotion("thinking", 2.0, "Let me think about that...")
                    
                    # Get AI response
                    ai_response = self.ask_ai(question)
                    
                    if ai_response:
                        # Display the response
                        print(f"<SPEAK> GERTY says: {ai_response}")
                        self.display_emotion("happy", 5.0, ai_response)
                    else:
                        self.display_emotion("sad", 3.0, "Sorry, I couldn't get a response")
                else:
                    self.display_emotion("confused", 3.0, "Sorry, I didn't hear anything")
                    
            elif result == False:  # ESC or Q pressed
                break
                
    def pause_audio_stream(self):
        """Temporarily pause the audio stream without cleaning up Porcupine"""
        try:
            if hasattr(self, 'audio_stream') and self.audio_stream:
                if self.audio_stream.is_active():
                    self.audio_stream.stop_stream()
                    print("   <PAUSE> Audio stream paused")
                    return True
        except Exception as e:
            print(f"   <WARNING> Audio stream pause error: {e}")
        return False
    
    def resume_audio_stream(self):
        """Resume the paused audio stream"""
        try:
            if hasattr(self, 'audio_stream') and self.audio_stream:
                if not self.audio_stream.is_active():
                    self.audio_stream.start_stream()
                    print("   <RESUME> Audio stream resumed")
                    return True
        except Exception as e:
            print(f"   <WARNING> Audio stream resume error: {e}")
        return False

    def run(self):
        """Main execution"""
        print("=" * 60)
        print("<SYSTEM> GERTY Simple Voice Assistant with Wake Word Detection")
        print("   Wake word activation + SPACE backup, ESC/Q to exit")
        print("=" * 60)
        
        try:
            self.setup_display()
            self.setup_voice()
            
            # Setup Porcupine wake word detection
            porcupine_success = self.setup_porcupine()
            
            # Boot sequence
            if not self.boot_sequence():
                return
                
            time.sleep(1)
            
            # Test AI connection
            print("<TEST> Testing AI connection...")
            test_response = self.ask_ai("Hello! Just testing the connection.")
            if test_response:
                print("<OK> AI connection successful!")
            else:
                print("<WARNING> AI connection failed - continuing anyway")
                
            # Main interaction loop
            self.voice_interaction_loop()
            
        except KeyboardInterrupt:
            print("\n<WARNING> Interrupted by user")
        except Exception as e:
            print(f"<ERROR> Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Clean up resources
            self.cleanup_porcupine()
            cv2.destroyAllWindows()
            print("<OFFLINE> GERTY Simple Voice Assistant Offline")


def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print("GERTY Simple Voice Assistant with Porcupine Wake Word Detection")
        print("Usage: python gerty_simple_voice.py")
        print("Controls:")
        print("  Wake Word - Say 'Hey GERTY' to activate voice assistant")
        print("  SPACE - Manual activation (backup)")
        print("  ESC or Q - Exit")
        print("\nFeatures:")
        print("  - Always-on microphone listening for wake word")
        print("  - Continuous wake word detection (never pauses)")
        print("  - Clean Porcupine implementation")
        return
        
    gerty = GERTYSimpleVoice()
    gerty.run()


if __name__ == "__main__":
    main()
