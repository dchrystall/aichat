# GirlChat Memory System

## Overview

The GirlChat app now includes a sophisticated memory system that allows the AI to remember details about users across conversations and sessions. This creates a more personalized and engaging experience.

## Memory Features

### 1. **User Profile Memory**
- **Name**: Automatically detected and remembered
- **Age**: Extracted from conversations
- **Location**: Detected when mentioned
- **Interests**: Tracked from user preferences and conversations
- **Communication Style**: Adapts based on user behavior

### 2. **Conversation History**
- **Total Conversations**: Tracks number of interactions
- **First/Last Conversation**: Timestamps for relationship tracking
- **Average Message Length**: Understanding user communication style
- **Favorite Topics**: Automatically categorized from conversations
- **Topic Categories**: Work, Family, Hobbies, Relationships, Health, Travel, Food, Entertainment, Technology, Emotions

### 3. **Emotional Context**
- **Current Mood**: Real-time mood detection (happy, sad, angry, stressed, calm, excited)
- **Mood History**: Tracks mood changes over time
- **Engagement Level**: Monitors user participation (low, medium, high)
- **Emotional Triggers**: Identifies what affects user mood

### 4. **Behavioral Patterns**
- **Active Hours**: Tracks when user is most active
- **Conversation Depth**: Casual, moderate, or deep conversations
- **Photo Sharing Frequency**: Tracks image analysis usage
- **Response Patterns**: Understanding user communication preferences

### 5. **Relationship Memory**
- **Important Dates**: Birthdays, anniversaries, special occasions
- **Shared Jokes**: Inside jokes and references
- **Relationship Milestones**: Significant moments in the relationship
- **Future Plans**: Plans and goals discussed
- **Conversation Highlights**: Memorable moments

### 6. **Personal Details**
- **Work Information**: Job details, career goals
- **Family Information**: Family members, relationships
- **Hobbies**: Activities and interests
- **Goals**: Personal and professional aspirations
- **Concerns**: Issues and worries shared
- **Achievements**: Successes and accomplishments

## How It Works

### Automatic Information Extraction
The system automatically extracts information from conversations using:
- **Pattern Matching**: Recognizes common phrases and structures
- **Keyword Detection**: Identifies topics and categories
- **Context Analysis**: Understands conversation flow and meaning

### Memory Persistence
- **File-Based Storage**: Memory is saved to JSON files
- **Session Persistence**: Data survives browser refreshes
- **Cross-Session Memory**: Information remembered across app restarts
- **Export/Import**: Users can backup and restore their memory data

### AI Integration
- **Context Injection**: Memory summary is included in AI prompts
- **Personalized Responses**: AI uses memory to tailor responses
- **Relationship Continuity**: Maintains conversation context and history
- **Adaptive Behavior**: AI adjusts based on user preferences and patterns

## Usage Examples

### Name Detection
```
User: "My name is John"
AI: "Nice to meet you, John! 💕 I'll remember that."
```

### Interest Tracking
```
User: "I love playing guitar"
AI: "That's awesome! I'll remember you're into music. What kind of guitar do you play?"
```

### Mood Awareness
```
User: "I'm feeling really stressed about work"
AI: "I can see you're stressed, sweetheart. Let's talk about what's going on at work."
```

### Topic Memory
```
User: "Remember when we talked about that movie?"
AI: "Of course! We discussed that thriller you watched last week. Did you end up watching the sequel?"
```

## Memory Management

### Sidebar Features
- **Memory Display**: Shows current memory data
- **Clear Memory**: Reset all stored information
- **Export Memory**: Download memory as JSON file
- **Real-time Updates**: Memory updates as you chat

### Privacy & Control
- **Local Storage**: Memory stored locally on your device
- **User Control**: Clear memory anytime
- **Data Export**: Backup your conversation history
- **Selective Memory**: Choose what to remember

## Technical Implementation

### Files
- `memory_manager.py`: Core memory management system
- `girlchat_streamlit.py`: Updated main app with memory integration
- `memory_*.json`: Persistent memory storage files

### Key Functions
- `MemoryManager.update_conversation()`: Updates memory with new data
- `MemoryManager.get_memory_summary()`: Generates AI context
- `MemoryManager.extract_personal_info()`: Extracts user details
- `MemoryManager.update_emotional_context()`: Tracks mood and emotions

### Memory Structure
```json
{
  "user_profile": { ... },
  "conversation_history": { ... },
  "emotional_context": { ... },
  "relationship_memory": { ... },
  "behavioral_patterns": { ... },
  "personal_details": { ... }
}
```

## Benefits

1. **Personalized Experience**: AI remembers your preferences and history
2. **Relationship Building**: Creates continuity across conversations
3. **Emotional Intelligence**: AI adapts to your mood and needs
4. **Context Awareness**: Maintains conversation flow and references
5. **User Control**: Full control over what's remembered
6. **Privacy**: Local storage keeps your data secure

## Future Enhancements

- **Vector Database**: Semantic search through conversation history
- **Multi-User Support**: Separate memory for different users
- **Advanced NLP**: Better information extraction and understanding
- **Memory Analytics**: Insights into conversation patterns
- **Cloud Sync**: Optional cloud storage for cross-device access
- **Memory Sharing**: Share memories between different AI personalities 