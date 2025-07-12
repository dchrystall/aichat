import json
import os
import time
from datetime import datetime
from typing import Dict, List, Optional
import hashlib
import re

class MemoryManager:
    """Advanced memory management system for GirlChat"""
    
    def __init__(self, user_id: str = "default"):
        self.user_id = user_id
        self.memory_file = f"memory_{user_id}.json"
        self.memory_data = self.load_memory()
    
    def load_memory(self) -> Dict:
        """Load memory from file"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading memory: {e}")
                return self.get_default_memory()
        return self.get_default_memory()
    
    def save_memory(self):
        """Save memory to file"""
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.memory_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving memory: {e}")
    
    def get_default_memory(self) -> Dict:
        """Get default memory structure"""
        return {
            "user_profile": {
                "name": None,
                "age": None,
                "location": None,
                "interests": [],
                "preferences": {},
                "relationship_status": None,
                "communication_style": "casual"
            },
            "conversation_history": {
                "total_conversations": 0,
                "first_conversation": None,
                "last_conversation": None,
                "conversation_count": 0,
                "average_message_length": 0,
                "favorite_topics": [],
                "disliked_topics": []
            },
            "emotional_context": {
                "current_mood": "neutral",
                "mood_history": [],
                "stress_level": "low",
                "engagement_level": "medium",
                "emotional_triggers": []
            },
            "relationship_memory": {
                "important_dates": {},
                "shared_jokes": [],
                "inside_references": [],
                "relationship_milestones": [],
                "future_plans": [],
                "conversation_highlights": []
            },
            "behavioral_patterns": {
                "active_hours": [],
                "response_patterns": {},
                "conversation_depth": "casual",
                "photo_sharing_frequency": 0,
                "topic_preferences": {}
            },
            "personal_details": {
                "work_info": {},
                "family_info": {},
                "hobbies": [],
                "goals": [],
                "concerns": [],
                "achievements": []
            }
        }
    
    def update_conversation(self, user_input: str, ai_response: str, timestamp: float = None):
        """Update memory with new conversation"""
        if timestamp is None:
            timestamp = time.time()
        
        # Update conversation stats
        self.memory_data["conversation_history"]["conversation_count"] += 1
        self.memory_data["conversation_history"]["total_conversations"] += 1
        
        if not self.memory_data["conversation_history"]["first_conversation"]:
            self.memory_data["conversation_history"]["first_conversation"] = timestamp
        
        self.memory_data["conversation_history"]["last_conversation"] = timestamp
        
        # Update average message length
        current_avg = self.memory_data["conversation_history"]["average_message_length"]
        count = self.memory_data["conversation_history"]["conversation_count"]
        new_avg = ((current_avg * (count - 1)) + len(user_input)) / count
        self.memory_data["conversation_history"]["average_message_length"] = new_avg
        
        # Extract and store information
        self.extract_personal_info(user_input, ai_response)
        self.update_emotional_context(user_input, ai_response)
        self.extract_topics(user_input, ai_response)
        self.update_behavioral_patterns(user_input, timestamp)
        
        # Save memory
        self.save_memory()
    
    def extract_personal_info(self, user_input: str, ai_response: str):
        """Extract personal information from conversation"""
        text = user_input.lower()
        
        # Extract name
        if not self.memory_data["user_profile"]["name"]:
            name_patterns = [
                r"my name is (\w+)",
                r"i'm (\w+)",
                r"call me (\w+)",
                r"i am (\w+)"
            ]
            for pattern in name_patterns:
                match = re.search(pattern, text)
                if match:
                    self.memory_data["user_profile"]["name"] = match.group(1).title()
                    break
        
        # Extract age
        if not self.memory_data["user_profile"]["age"]:
            age_match = re.search(r'i am (\d+)', text) or re.search(r"i'm (\d+)", text) or re.search(r'age (\d+)', text)
            if age_match:
                self.memory_data["user_profile"]["age"] = int(age_match.group(1))
        
        # Extract location
        if not self.memory_data["user_profile"]["location"]:
            location_keywords = ["live in", "from", "city", "state", "country"]
            for keyword in location_keywords:
                if keyword in text:
                    words = text.split()
                    try:
                        keyword_index = words.index(keyword)
                        if keyword_index + 1 < len(words):
                            location = words[keyword_index + 1]
                            self.memory_data["user_profile"]["location"] = location.title()
                            break
                    except ValueError:
                        continue
        
        # Extract interests
        interest_keywords = ["like", "love", "enjoy", "interested in", "passionate about", "hobby"]
        for keyword in interest_keywords:
            if keyword in text:
                words = text.split()
                try:
                    keyword_index = words.index(keyword)
                    if keyword_index + 1 < len(words):
                        interest = words[keyword_index + 1]
                        if interest not in self.memory_data["user_profile"]["interests"]:
                            self.memory_data["user_profile"]["interests"].append(interest)
                        break
                except ValueError:
                    continue
    
    def update_emotional_context(self, user_input: str, ai_response: str):
        """Update emotional context based on conversation"""
        text = f"{user_input} {ai_response}".lower()
        
        # Mood detection
        mood_indicators = {
            "happy": ["happy", "excited", "great", "awesome", "wonderful", "amazing", "😊", "😄", "🎉", "joy", "pleased"],
            "sad": ["sad", "depressed", "down", "upset", "disappointed", "😢", "😭", "😔", "miserable", "unhappy"],
            "angry": ["angry", "mad", "furious", "annoyed", "frustrated", "😠", "😡", "🤬", "irritated"],
            "stressed": ["stressed", "anxious", "worried", "nervous", "overwhelmed", "😰", "😨", "tense"],
            "calm": ["calm", "relaxed", "peaceful", "chill", "😌", "🧘", "serene"],
            "excited": ["excited", "thrilled", "pumped", "energized", "🔥", "⚡"]
        }
        
        detected_mood = "neutral"
        for mood, indicators in mood_indicators.items():
            if any(indicator in text for indicator in indicators):
                detected_mood = mood
                break
        
        self.memory_data["emotional_context"]["current_mood"] = detected_mood
        
        # Add to mood history
        mood_entry = {
            "mood": detected_mood,
            "timestamp": time.time(),
            "trigger": user_input[:100]  # First 100 chars as context
        }
        self.memory_data["emotional_context"]["mood_history"].append(mood_entry)
        
        # Keep only last 50 mood entries
        if len(self.memory_data["emotional_context"]["mood_history"]) > 50:
            self.memory_data["emotional_context"]["mood_history"] = self.memory_data["emotional_context"]["mood_history"][-50:]
        
        # Update engagement level
        message_length = len(user_input)
        if message_length > 100:
            self.memory_data["emotional_context"]["engagement_level"] = "high"
        elif message_length > 50:
            self.memory_data["emotional_context"]["engagement_level"] = "medium"
        else:
            self.memory_data["emotional_context"]["engagement_level"] = "low"
    
    def extract_topics(self, user_input: str, ai_response: str):
        """Extract and categorize conversation topics"""
        combined_text = f"{user_input} {ai_response}".lower()
        
        topic_categories = {
            "work": ["work", "job", "office", "career", "boss", "colleague", "meeting", "project"],
            "family": ["family", "mom", "dad", "sister", "brother", "parents", "kids", "children"],
            "hobbies": ["hobby", "interest", "sport", "music", "reading", "gaming", "art", "cooking"],
            "relationships": ["relationship", "dating", "partner", "boyfriend", "girlfriend", "marriage"],
            "health": ["health", "exercise", "diet", "fitness", "wellness", "doctor", "medical"],
            "travel": ["travel", "vacation", "trip", "destination", "adventure", "flight"],
            "food": ["food", "cooking", "restaurant", "meal", "cuisine", "recipe"],
            "entertainment": ["movie", "show", "book", "game", "entertainment", "tv", "film"],
            "technology": ["tech", "computer", "phone", "app", "software", "internet"],
            "emotions": ["happy", "sad", "angry", "excited", "worried", "stressed", "feelings"]
        }
        
        detected_topics = []
        for category, keywords in topic_categories.items():
            if any(keyword in combined_text for keyword in keywords):
                detected_topics.append(category)
        
        # Update favorite topics
        for topic in detected_topics:
            if topic not in self.memory_data["conversation_history"]["favorite_topics"]:
                self.memory_data["conversation_history"]["favorite_topics"].append(topic)
    
    def update_behavioral_patterns(self, user_input: str, timestamp: float):
        """Update behavioral patterns"""
        # Track active hours
        hour = datetime.fromtimestamp(timestamp).hour
        if hour not in self.memory_data["behavioral_patterns"]["active_hours"]:
            self.memory_data["behavioral_patterns"]["active_hours"].append(hour)
            self.memory_data["behavioral_patterns"]["active_hours"].sort()
        
        # Track conversation depth
        if len(user_input) > 200:
            self.memory_data["behavioral_patterns"]["conversation_depth"] = "deep"
        elif len(user_input) > 100:
            self.memory_data["behavioral_patterns"]["conversation_depth"] = "moderate"
        else:
            self.memory_data["behavioral_patterns"]["conversation_depth"] = "casual"
    
    def get_memory_summary(self) -> str:
        """Generate a summary of user memory for AI context"""
        summary_parts = []
        
        # Basic profile
        profile = self.memory_data["user_profile"]
        if profile["name"]:
            summary_parts.append(f"User's name: {profile['name']}")
        if profile["age"]:
            summary_parts.append(f"User's age: {profile['age']}")
        if profile["location"]:
            summary_parts.append(f"User's location: {profile['location']}")
        
        # Conversation stats
        conv_history = self.memory_data["conversation_history"]
        summary_parts.append(f"Total conversations: {conv_history['conversation_count']}")
        
        # Current mood and engagement
        emotional = self.memory_data["emotional_context"]
        summary_parts.append(f"Current mood: {emotional['current_mood']}")
        summary_parts.append(f"Engagement level: {emotional['engagement_level']}")
        
        # Interests and topics
        if profile["interests"]:
            summary_parts.append(f"Interests: {', '.join(profile['interests'])}")
        if conv_history["favorite_topics"]:
            summary_parts.append(f"Favorite topics: {', '.join(conv_history['favorite_topics'])}")
        
        # Behavioral patterns
        behavioral = self.memory_data["behavioral_patterns"]
        summary_parts.append(f"Conversation depth: {behavioral['conversation_depth']}")
        
        return " | ".join(summary_parts) if summary_parts else "No memory data available"
    
    def add_relationship_milestone(self, milestone: str, date: str = None):
        """Add a relationship milestone"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        milestone_entry = {
            "description": milestone,
            "date": date,
            "timestamp": time.time()
        }
        self.memory_data["relationship_memory"]["relationship_milestones"].append(milestone_entry)
        self.save_memory()
    
    def add_inside_joke(self, joke: str):
        """Add an inside joke or reference"""
        if joke not in self.memory_data["relationship_memory"]["shared_jokes"]:
            self.memory_data["relationship_memory"]["shared_jokes"].append(joke)
            self.save_memory()
    
    def clear_memory(self):
        """Clear all memory data"""
        self.memory_data = self.get_default_memory()
        self.save_memory()
    
    def export_memory(self) -> Dict:
        """Export memory data for backup"""
        return self.memory_data.copy()
    
    def import_memory(self, memory_data: Dict):
        """Import memory data from backup"""
        self.memory_data = memory_data
        self.save_memory() 