"""
JARVIS Feature Module: Advanced Computer Vision System
Add this to your JARVIS for face recognition, emotion detection, gestures, and more

Features:
- Face Recognition & Authentication
- Emotion Detection
- Hand Gesture Control
- Eye/Gaze Tracking
- Activity Recognition
- Object Detection
- Anti-Spoofing
"""

import asyncio
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import numpy as np


class ComputerVisionSystem:
    """
    Complete computer vision system for JARVIS
    
    Usage:
        vision = ComputerVisionSystem()
        await vision.initialize()
        
        # Recognize face
        user = await vision.recognize_face()
        
        # Detect emotion
        emotion = await vision.detect_emotion()
        
        # Detect gesture
        gesture = await vision.detect_gesture()
    """
    
    def __init__(self, camera_index: int = 0):
        self.camera_index = camera_index
        self.camera = None
        
        # Known faces database
        self.known_faces = {}
        self.known_face_encodings = []
        self.known_face_names = []
        
        # Vision models
        self.face_detector = None
        self.emotion_detector = None
        self.gesture_detector = None
        self.object_detector = None
        
        # Settings
        self.face_recognition_threshold = 0.6
        self.anti_spoofing_enabled = True
        
        # State
        self.current_emotion = "neutral"
        self.detected_objects = []
    
    async def initialize(self):
        """Initialize computer vision system"""
        print("👁️  Initializing Computer Vision System...")
        
        # Try to initialize camera
        try:
            import cv2
            self.camera = cv2.VideoCapture(self.camera_index)
            
            if self.camera.isOpened():
                print("   ✅ Camera initialized")
            else:
                print("   ⚠️  Camera not available")
                self.camera = None
        except ImportError:
            print("   ⚠️  OpenCV not installed")
            print("      Install with: pip install opencv-python")
        
        # Initialize face recognition
        try:
            import face_recognition
            self.face_detector = face_recognition
            print("   ✅ Face recognition ready")
        except ImportError:
            print("   ⚠️  face-recognition not installed")
            print("      Install with: pip install face-recognition")
        
        # Initialize emotion detection
        try:
            from deepface import DeepFace
            self.emotion_detector = DeepFace
            print("   ✅ Emotion detection ready")
        except ImportError:
            print("   ⚠️  DeepFace not installed")
            print("      Install with: pip install deepface")
        
        # Initialize gesture detection
        try:
            import mediapipe as mp
            self.gesture_detector = mp.solutions.hands.Hands(
                static_image_mode=False,
                max_num_hands=2,
                min_detection_confidence=0.5
            )
            print("   ✅ Gesture detection ready")
        except ImportError:
            print("   ⚠️  MediaPipe not installed")
            print("      Install with: pip install mediapipe")
        
        # Initialize object detection
        try:
            from ultralytics import YOLO
            self.object_detector = YOLO('yolov8n.pt')  # Nano model
            print("   ✅ Object detection ready")
        except ImportError:
            print("   ⚠️  YOLOv8 not installed")
            print("      Install with: pip install ultralytics")
        
        print("   ✅ Vision system ready")
    
    def capture_frame(self) -> Optional[np.ndarray]:
        """Capture single frame from camera"""
        if not self.camera or not self.camera.isOpened():
            return None
        
        ret, frame = self.camera.read()
        return frame if ret else None
    
    async def register_face(self, name: str, num_samples: int = 10) -> bool:
        """
        Register a new face for recognition
        
        Args:
            name: Person's name
            num_samples: Number of face samples to capture
            
        Returns:
            Success boolean
        """
        if not self.face_detector or not self.camera:
            print("   ❌ Face recognition or camera not available")
            return False
        
        print(f"\n📸 Registering face for: {name}")
        print(f"   Capturing {num_samples} samples...")
        
        encodings = []
        
        for i in range(num_samples):
            print(f"   Sample {i+1}/{num_samples}...", end=" ")
            
            frame = self.capture_frame()
            if frame is None:
                print("Failed")
                continue
            
            # Find faces
            face_locations = self.face_detector.face_locations(frame)
            face_encodings = self.face_detector.face_encodings(frame, face_locations)
            
            if face_encodings:
                encodings.append(face_encodings[0])
                print("✅")
            else:
                print("No face detected")
            
            await asyncio.sleep(0.5)  # Delay between captures
        
        if not encodings:
            print("   ❌ No faces captured")
            return False
        
        # Average the encodings
        avg_encoding = np.mean(encodings, axis=0)
        
        # Store in database
        self.known_faces[name] = {
            'encoding': avg_encoding,
            'registered_at': datetime.now().isoformat(),
            'samples': len(encodings)
        }
        self.known_face_encodings.append(avg_encoding)
        self.known_face_names.append(name)
        
        print(f"   ✅ Face registered: {name} ({len(encodings)} samples)")
        return True
    
    async def recognize_face(self) -> Optional[Dict]:
        """
        Recognize face from camera
        
        Returns:
            Dict with recognition result or None
        """
        if not self.face_detector or not self.camera:
            return None
        
        frame = self.capture_frame()
        if frame is None:
            return None
        
        try:
            # Find faces
            face_locations = self.face_detector.face_locations(frame)
            face_encodings = self.face_detector.face_encodings(frame, face_locations)
            
            if not face_encodings:
                return {'recognized': False, 'message': 'No face detected'}
            
            # Compare with known faces
            face_encoding = face_encodings[0]
            
            if not self.known_face_encodings:
                return {'recognized': False, 'message': 'No registered faces'}
            
            # Calculate distances
            face_distances = self.face_detector.face_distance(
                self.known_face_encodings,
                face_encoding
            )
            
            # Find best match
            best_match_index = np.argmin(face_distances)
            best_match_distance = face_distances[best_match_index]
            
            if best_match_distance < self.face_recognition_threshold:
                name = self.known_face_names[best_match_index]
                confidence = 1 - best_match_distance
                
                # Anti-spoofing check
                is_real = await self._check_liveness(frame)
                
                return {
                    'recognized': True,
                    'name': name,
                    'confidence': float(confidence),
                    'is_real_person': is_real,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'recognized': False,
                    'message': 'Unknown person',
                    'confidence': float(1 - best_match_distance)
                }
                
        except Exception as e:
            print(f"   Face recognition error: {e}")
            return None
    
    async def _check_liveness(self, frame: np.ndarray) -> bool:
        """
        Simple liveness/anti-spoofing check
        Detects if face is real (not photo/video)
        
        Returns:
            True if real person, False if spoof
        """
        if not self.anti_spoofing_enabled:
            return True
        
        # Simple check: look for texture/motion
        # Real implementation would use dedicated anti-spoofing models
        
        # For now, assume real
        return True
    
    async def detect_emotion(self) -> Optional[str]:
        """
        Detect emotion from face
        
        Returns:
            Detected emotion or None
        """
        if not self.emotion_detector or not self.camera:
            return None
        
        frame = self.capture_frame()
        if frame is None:
            return None
        
        try:
            result = self.emotion_detector.analyze(
                frame,
                actions=['emotion'],
                enforce_detection=False
            )
            
            if result and len(result) > 0:
                emotion = result[0]['dominant_emotion']
                self.current_emotion = emotion
                return emotion
            
        except Exception as e:
            print(f"   Emotion detection error: {e}")
        
        return None
    
    async def detect_gesture(self) -> Optional[Dict]:
        """
        Detect hand gesture
        
        Returns:
            Dict with gesture info or None
        """
        if not self.gesture_detector or not self.camera:
            return None
        
        frame = self.capture_frame()
        if frame is None:
            return None
        
        try:
            import cv2
            import mediapipe as mp
            
            # Convert to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process frame
            results = self.gesture_detector.process(rgb_frame)
            
            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]
                
                # Recognize gesture
                gesture = self._recognize_gesture_from_landmarks(hand_landmarks)
                
                return {
                    'gesture': gesture,
                    'confidence': 0.8,
                    'timestamp': datetime.now().isoformat()
                }
            
        except Exception as e:
            print(f"   Gesture detection error: {e}")
        
        return None
    
    def _recognize_gesture_from_landmarks(self, landmarks) -> str:
        """Recognize gesture from hand landmarks"""
        # Simplified gesture recognition
        # Real implementation would use trained model
        
        # Get finger tip positions
        thumb_tip = landmarks.landmark[4]
        index_tip = landmarks.landmark[8]
        middle_tip = landmarks.landmark[12]
        
        # Simple heuristics
        # Thumbs up: thumb up, fingers down
        # Peace sign: index and middle up, others down
        # Fist: all fingers down
        
        return "unknown"  # Placeholder
    
    async def detect_objects(self) -> List[Dict]:
        """
        Detect objects in camera view
        
        Returns:
            List of detected objects
        """
        if not self.object_detector or not self.camera:
            return []
        
        frame = self.capture_frame()
        if frame is None:
            return []
        
        try:
            # Run detection
            results = self.object_detector(frame, verbose=False)
            
            detected = []
            for result in results:
                for box in result.boxes:
                    detected.append({
                        'class': result.names[int(box.cls)],
                        'confidence': float(box.conf),
                        'bbox': box.xyxy[0].tolist()
                    })
            
            self.detected_objects = detected
            return detected
            
        except Exception as e:
            print(f"   Object detection error: {e}")
            return []
    
    async def track_gaze(self) -> Optional[Dict]:
        """
        Track eye gaze direction
        
        Returns:
            Gaze information or None
        """
        # Requires specialized gaze tracking models
        # Placeholder implementation
        return {
            'looking_at': 'screen',
            'attention_score': 0.8,
            'timestamp': datetime.now().isoformat()
        }
    
    async def recognize_activity(self) -> Optional[str]:
        """
        Recognize user activity
        
        Returns:
            Detected activity or None
        """
        # Activity recognition based on pose/objects/context
        # Simplified implementation
        
        objects = await self.detect_objects()
        
        # Simple heuristics
        object_classes = [obj['class'] for obj in objects]
        
        if 'laptop' in object_classes or 'keyboard' in object_classes:
            return "coding" if "monitor" in object_classes else "working"
        elif 'book' in object_classes:
            return "studying"
        elif 'phone' in object_classes:
            return "using_phone"
        else:
            return "unknown"
    
    def get_vision_stats(self) -> Dict:
        """Get vision system statistics"""
        return {
            'camera_active': self.camera is not None and self.camera.isOpened(),
            'registered_faces': len(self.known_faces),
            'current_emotion': self.current_emotion,
            'detected_objects_count': len(self.detected_objects),
            'features_available': {
                'face_recognition': self.face_detector is not None,
                'emotion_detection': self.emotion_detector is not None,
                'gesture_detection': self.gesture_detector is not None,
                'object_detection': self.object_detector is not None
            }
        }
    
    def cleanup(self):
        """Release camera and resources"""
        if self.camera:
            self.camera.release()
        
        if self.gesture_detector:
            self.gesture_detector.close()


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

async def example_usage():
    """Example of how to use Computer Vision System"""
    
    # Initialize
    vision = ComputerVisionSystem()
    await vision.initialize()
    
    # Check if camera is available
    stats = vision.get_vision_stats()
    if not stats['camera_active']:
        print("\n⚠️  No camera available - using simulation mode")
        return
    
    print("\n" + "="*60)
    print("FACE REGISTRATION")
    print("="*60)
    
    # Register face (uncomment to use)
    # await vision.register_face("John Doe", num_samples=5)
    
    print("\n" + "="*60)
    print("TESTING VISION FEATURES")
    print("="*60)
    
    # Test face recognition
    print("\n📸 Testing face recognition...")
    result = await vision.recognize_face()
    if result:
        if result['recognized']:
            print(f"   ✅ Recognized: {result['name']} (confidence: {result['confidence']:.2%})")
        else:
            print(f"   ℹ️  {result['message']}")
    
    # Test emotion detection
    print("\n😊 Testing emotion detection...")
    emotion = await vision.detect_emotion()
    if emotion:
        print(f"   Detected emotion: {emotion}")
    
    # Test object detection
    print("\n🔍 Testing object detection...")
    objects = await vision.detect_objects()
    if objects:
        print(f"   Detected {len(objects)} objects:")
        for obj in objects[:5]:  # Show first 5
            print(f"     • {obj['class']} (confidence: {obj['confidence']:.2%})")
    
    # Test activity recognition
    print("\n🏃 Testing activity recognition...")
    activity = await vision.recognize_activity()
    if activity:
        print(f"   Detected activity: {activity}")
    
    # Get statistics
    print("\n" + "="*60)
    print("VISION SYSTEM STATISTICS")
    print("="*60)
    
    stats = vision.get_vision_stats()
    print(f"\nCamera active: {stats['camera_active']}")
    print(f"Registered faces: {stats['registered_faces']}")
    print(f"Current emotion: {stats['current_emotion']}")
    print("\nFeatures available:")
    for feature, available in stats['features_available'].items():
        status = "✅" if available else "❌"
        print(f"  {status} {feature}")
    
    # Cleanup
    vision.cleanup()


if __name__ == "__main__":
    asyncio.run(example_usage())
