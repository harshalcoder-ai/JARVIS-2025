"""
JARVIS Feature Module: Emotional Intelligence Engine
Add this to your existing JARVIS for emotion detection and adaptive responses

Features:
- Mood detection from voice
- Emotion detection from face
- Mood history tracking
- Adaptive response tone
- Stress/fatigue detection
"""

import asyncio
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from collections import deque
import statistics


@dataclass
class EmotionReading:
    """Single emotion reading"""
    emotion: str
    confidence: float
    source: str  # voice, face, text
    timestamp: datetime
    metadata: Dict = None


class EmotionalIntelligence:
    """
    Complete emotional intelligence system
    
    Usage:
        ei = EmotionalIntelligence()
        await ei.initialize()
        
        # Detect emotion from face
        emotion = await ei.detect_emotion_from_face()
        
        # Get adaptive response
        response = ei.get_adaptive_response("Hello", current_emotion="sad")
    """
    
    EMOTIONS = {
        'happy': {'arousal': 0.7, 'valence': 0.8},
        'sad': {'arousal': -0.5, 'valence': -0.7},
        'angry': {'arousal': 0.8, 'valence': -0.6},
        'fear': {'arousal': 0.6, 'valence': -0.5},
        'surprise': {'arousal': 0.5, 'valence': 0.3},
        'disgust': {'arousal': 0.3, 'valence': -0.6},
        'neutral': {'arousal': 0.0, 'valence': 0.0},
        'excited': {'arousal': 0.9, 'valence': 0.9},
        'stressed': {'arousal': 0.7, 'valence': -0.4},
        'calm': {'arousal': -0.3, 'valence': 0.5},
        'tired': {'arousal': -0.7, 'valence': -0.2}
    }
    
    def __init__(self, history_size: int = 100):
        self.history_size = history_size
        self.emotion_history: deque = deque(maxlen=history_size)
        self.mood_trend = "neutral"
        
        # Emotion detection models
        self.face_detector = None
        self.voice_analyzer = None
        
        # Adaptive response settings
        self.response_styles = {
            'sad': {'tone': 'supportive', 'verbosity': 'high', 'empathy': 0.9},
            'angry': {'tone': 'calm', 'verbosity': 'low', 'empathy': 0.8},
            'stressed': {'tone': 'soothing', 'verbosity': 'medium', 'empathy': 0.9},
            'happy': {'tone': 'enthusiastic', 'verbosity': 'high', 'empathy': 0.7},
            'tired': {'tone': 'gentle', 'verbosity': 'low', 'empathy': 0.8},
            'neutral': {'tone': 'professional', 'verbosity': 'medium', 'empathy': 0.6}
        }
    
    async def initialize(self):
        """Initialize emotional intelligence system"""
        print("❤️  Initializing Emotional Intelligence Engine...")
        
        # Try to load face emotion detector
        try:
            from deepface import DeepFace
            self.face_detector = DeepFace
            print("   ✅ Face emotion detection ready (DeepFace)")
        except ImportError:
            print("   ⚠️  DeepFace not installed - face emotions disabled")
            print("      Install with: pip install deepface")
        
        # Try to load voice analyzer
        try:
            import librosa
            self.voice_analyzer = librosa
            print("   ✅ Voice emotion analysis ready")
        except ImportError:
            print("   ⚠️  Librosa not installed - voice emotions disabled")
            print("      Install with: pip install librosa")
        
        print("   ✅ Emotional Intelligence ready")
    
    async def detect_emotion_from_face(self, image_path: Optional[str] = None) -> Optional[str]:
        """
        Detect emotion from face using camera or image
        
        Args:
            image_path: Path to image, or None to use camera
            
        Returns:
            Detected emotion or None
        """
        if not self.face_detector:
            return None
        
        try:
            import cv2
            
            # Get image
            if image_path:
                img = cv2.imread(image_path)
            else:
                # Use camera
                cap = cv2.VideoCapture(0)
                ret, img = cap.read()
                cap.release()
                
                if not ret:
                    return None
            
            # Analyze emotion
            result = self.face_detector.analyze(
                img, 
                actions=['emotion'],
                enforce_detection=False
            )
            
            if result and len(result) > 0:
                emotion = result[0]['dominant_emotion']
                confidence = result[0]['emotion'][emotion] / 100.0
                
                # Record emotion
                reading = EmotionReading(
                    emotion=emotion,
                    confidence=confidence,
                    source='face',
                    timestamp=datetime.now()
                )
                self.emotion_history.append(reading)
                
                # Update mood trend
                self._update_mood_trend()
                
                return emotion
                
        except Exception as e:
            print(f"   Face emotion error: {e}")
            return None
    
    async def detect_emotion_from_voice(self, audio_data: bytes) -> Optional[str]:
        """
        Detect emotion from voice
        
        Args:
            audio_data: Raw audio bytes
            
        Returns:
            Detected emotion or None
        """
        if not self.voice_analyzer:
            return None
        
        try:
            import numpy as np
            
            # Analyze voice features
            # This is a simplified version - real implementation would use
            # trained models for emotion recognition
            
            # Extract features like pitch, energy, tempo
            # For now, return based on simple heuristics
            
            # Placeholder: Random emotion (replace with actual model)
            emotions = ['neutral', 'happy', 'sad', 'angry']
            emotion = emotions[0]  # Default neutral
            
            reading = EmotionReading(
                emotion=emotion,
                confidence=0.7,
                source='voice',
                timestamp=datetime.now()
            )
            self.emotion_history.append(reading)
            
            return emotion
            
        except Exception as e:
            print(f"   Voice emotion error: {e}")
            return None
    
    def detect_emotion_from_text(self, text: str) -> str:
        """
        Detect emotion from text using keyword analysis
        
        Args:
            text: Input text
            
        Returns:
            Detected emotion
        """
        text_lower = text.lower()
        
        # Emotion keywords
        emotion_keywords = {
            'happy': ['happy', 'great', 'awesome', 'wonderful', 'excellent', 'love', 'joy'],
            'sad': ['sad', 'unhappy', 'depressed', 'down', 'miserable', 'cry'],
            'angry': ['angry', 'mad', 'furious', 'annoyed', 'irritated', 'hate'],
            'stressed': ['stress', 'worried', 'anxious', 'overwhelm', 'pressure'],
            'tired': ['tired', 'exhausted', 'sleepy', 'fatigue', 'worn out'],
            'excited': ['excited', 'thrilled', 'pumped', 'energized']
        }
        
        # Count keyword matches
        emotion_scores = {}
        for emotion, keywords in emotion_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                emotion_scores[emotion] = score
        
        # Return emotion with highest score
        if emotion_scores:
            detected = max(emotion_scores, key=emotion_scores.get)
            
            reading = EmotionReading(
                emotion=detected,
                confidence=0.6,
                source='text',
                timestamp=datetime.now()
            )
            self.emotion_history.append(reading)
            
            return detected
        
        return 'neutral'
    
    def _update_mood_trend(self):
        """Update overall mood trend based on recent emotions"""
        if len(self.emotion_history) < 3:
            return
        
        # Get recent emotions (last 10)
        recent = list(self.emotion_history)[-10:]
        
        # Calculate average valence (positive/negative)
        valences = [
            self.EMOTIONS.get(reading.emotion, {'valence': 0})['valence']
            for reading in recent
        ]
        
        avg_valence = statistics.mean(valences)
        
        # Determine trend
        if avg_valence > 0.3:
            self.mood_trend = 'positive'
        elif avg_valence < -0.3:
            self.mood_trend = 'negative'
        else:
            self.mood_trend = 'neutral'
    
    def get_current_mood(self) -> Dict:
        """
        Get current mood assessment
        
        Returns:
            Dictionary with mood information
        """
        if not self.emotion_history:
            return {
                'current_emotion': 'neutral',
                'mood_trend': 'neutral',
                'confidence': 0.5
            }
        
        # Most recent emotion
        latest = self.emotion_history[-1]
        
        return {
            'current_emotion': latest.emotion,
            'mood_trend': self.mood_trend,
            'confidence': latest.confidence,
            'timestamp': latest.timestamp.isoformat(),
            'source': latest.source
        }
    
    def get_mood_history(self, hours: int = 24) -> List[Dict]:
        """
        Get mood history for specified time period
        
        Args:
            hours: Number of hours to look back
            
        Returns:
            List of emotion readings
        """
        cutoff = datetime.now() - timedelta(hours=hours)
        
        history = [
            {
                'emotion': reading.emotion,
                'confidence': reading.confidence,
                'source': reading.source,
                'timestamp': reading.timestamp.isoformat()
            }
            for reading in self.emotion_history
            if reading.timestamp > cutoff
        ]
        
        return history
    
    def detect_stress(self) -> Dict:
        """
        Detect if user is stressed based on emotion patterns
        
        Returns:
            Stress assessment
        """
        if len(self.emotion_history) < 5:
            return {'stressed': False, 'level': 0.0}
        
        recent = list(self.emotion_history)[-10:]
        
        # Count stress indicators
        stress_emotions = ['stressed', 'angry', 'anxious', 'worried']
        stress_count = sum(
            1 for reading in recent 
            if reading.emotion in stress_emotions
        )
        
        stress_level = stress_count / len(recent)
        
        return {
            'stressed': stress_level > 0.4,
            'level': stress_level,
            'recommendation': self._get_stress_recommendation(stress_level)
        }
    
    def _get_stress_recommendation(self, stress_level: float) -> str:
        """Get recommendation based on stress level"""
        if stress_level > 0.7:
            return "Consider taking a break. You seem quite stressed."
        elif stress_level > 0.4:
            return "You might be feeling stressed. Would you like to take a short break?"
        else:
            return "You're doing well. Keep it up!"
    
    def get_adaptive_response(self, base_response: str, 
                            current_emotion: Optional[str] = None) -> str:
        """
        Adapt response based on user's emotion
        
        Args:
            base_response: Original response
            current_emotion: Current user emotion (or auto-detect)
            
        Returns:
            Adapted response
        """
        # Get current emotion
        if not current_emotion and self.emotion_history:
            current_emotion = self.emotion_history[-1].emotion
        
        if not current_emotion:
            return base_response
        
        # Get response style for emotion
        style = self.response_styles.get(
            current_emotion,
            self.response_styles['neutral']
        )
        
        # Adapt response based on style
        adapted = base_response
        
        # Add empathetic prefix for negative emotions
        if current_emotion in ['sad', 'stressed', 'angry', 'tired']:
            empathy_prefixes = {
                'sad': "I understand you're feeling down. ",
                'stressed': "I can see you're stressed. ",
                'angry': "I understand your frustration. ",
                'tired': "You seem tired. "
            }
            adapted = empathy_prefixes.get(current_emotion, "") + adapted
        
        # Add enthusiasm for positive emotions
        elif current_emotion in ['happy', 'excited']:
            if not adapted.endswith('!'):
                adapted = adapted.rstrip('.') + '!'
        
        return adapted
    
    def get_emotion_stats(self) -> Dict:
        """Get emotion statistics"""
        if not self.emotion_history:
            return {}
        
        # Count emotions
        emotion_counts = {}
        for reading in self.emotion_history:
            emotion_counts[reading.emotion] = emotion_counts.get(reading.emotion, 0) + 1
        
        # Calculate percentages
        total = len(self.emotion_history)
        emotion_percentages = {
            emotion: (count / total) * 100
            for emotion, count in emotion_counts.items()
        }
        
        return {
            'total_readings': total,
            'emotion_distribution': emotion_percentages,
            'most_common': max(emotion_counts, key=emotion_counts.get),
            'mood_trend': self.mood_trend
        }


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

async def example_usage():
    """Example of how to use Emotional Intelligence"""
    
    # Initialize
    ei = EmotionalIntelligence()
    await ei.initialize()
    
    # Simulate emotion detection from text
    print("\n🔍 Detecting emotions from text:")
    
    texts = [
        "I'm so happy today!",
        "I'm feeling really stressed about this deadline",
        "This is frustrating and making me angry",
        "I'm tired and need to rest"
    ]
    
    for text in texts:
        emotion = ei.detect_emotion_from_text(text)
        print(f"   Text: '{text}'")
        print(f"   Detected emotion: {emotion}\n")
    
    # Get current mood
    mood = ei.get_current_mood()
    print(f"📊 Current Mood: {mood}")
    
    # Check stress level
    stress = ei.detect_stress()
    print(f"\n😰 Stress Assessment:")
    print(f"   Stressed: {stress['stressed']}")
    print(f"   Level: {stress['level']:.2%}")
    print(f"   Recommendation: {stress['recommendation']}")
    
    # Test adaptive responses
    print(f"\n💬 Adaptive Responses:")
    
    base_response = "Here's the information you requested."
    
    for emotion in ['sad', 'happy', 'stressed', 'neutral']:
        adapted = ei.get_adaptive_response(base_response, emotion)
        print(f"   [{emotion.upper()}] {adapted}")
    
    # Get emotion statistics
    stats = ei.get_emotion_stats()
    print(f"\n📈 Emotion Statistics:")
    print(f"   Total readings: {stats['total_readings']}")
    print(f"   Most common: {stats['most_common']}")
    print(f"   Mood trend: {stats['mood_trend']}")


if __name__ == "__main__":
    asyncio.run(example_usage())
