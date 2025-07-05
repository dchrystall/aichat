# AI Personality Customization Guide

This guide explains how to easily edit and customize the AI personalities in your GirlChat app.

## Files Overview

- **`prompts.py`** - Python prompts for the Streamlit app
- **`prompts.json`** - JSON prompts for the HTML app
- **`girlchat_streamlit.py`** - Streamlit app (uses prompts.py)
- **`girlchat.html`** - HTML app (uses prompts.json)

## How to Edit Personalities

### For Streamlit App (Python)

1. Open `prompts.py`
2. Edit any of the personality prompts:
   - `VESPER_PROMPT` - Seductive, dominant personality
   - `SWEET_GIRLFRIEND_PROMPT` - Sweet and caring personality
   - `SASSY_GIRLFRIEND_PROMPT` - Sassy and confident personality
   - `PROFESSIONAL_PROMPT` - Sophisticated and professional personality

3. To switch personalities, change this line:
   ```python
   ACTIVE_PROMPT = VESPER_PROMPT  # Change to any other prompt
   ```

### For HTML App (JavaScript)

1. Open `prompts.json`
2. Edit any of the personality prompts:
   - `"vesper"` - Seductive, dominant personality
   - `"sweet"` - Sweet and caring personality
   - `"sassy"` - Sassy and confident personality
   - `"professional"` - Sophisticated and professional personality

3. To switch personalities, change this line:
   ```json
   "active": "vesper"  // Change to "sweet", "sassy", or "professional"
   ```

## Creating New Personalities

### For Streamlit App

1. Add a new prompt variable in `prompts.py`:
   ```python
   MY_NEW_PERSONALITY = """You are a [description of personality]..."""
   ```

2. Set it as active:
   ```python
   ACTIVE_PROMPT = MY_NEW_PERSONALITY
   ```

### For HTML App

1. Add a new prompt in `prompts.json`:
   ```json
   "my_new_personality": "You are a [description of personality]..."
   ```

2. Set it as active:
   ```json
   "active": "my_new_personality"
   ```

## Personality Examples

### Vesper (Current Default)
- Bold, dominant, and seductive
- Takes control of conversations
- Uses innuendo and playful dominance
- Perfect for adult roleplay scenarios

### Sweet Girlfriend
- Warm, affectionate, and supportive
- Uses terms of endearment
- Nurturing and protective
- Great for emotional support

### Sassy Girlfriend
- Witty, sharp-tongued, and confident
- Uses sarcasm and clever comebacks
- Independent but loyal
- Fun for banter and entertainment

### Professional
- Sophisticated, intelligent, and articulate
- Well-educated conversation partner
- Supportive and encouraging
- Ideal for intellectual discussions

## Tips for Writing Prompts

1. **Be Specific**: Clearly define the personality traits and speaking style
2. **Include Examples**: Mention specific phrases or expressions they should use
3. **Set Boundaries**: Define what topics or behaviors are appropriate
4. **Test and Iterate**: Try different versions to see what works best
5. **Keep it Consistent**: Make sure the personality doesn't contradict itself

## Deployment Notes

- Changes to `prompts.py` will take effect immediately when you restart the Streamlit app
- Changes to `prompts.json` will take effect when you refresh the HTML page
- Both files are included in the repository, so changes will be deployed with your app

## Troubleshooting

- If the HTML app can't load `prompts.json`, it will fall back to the default Vesper prompt
- Make sure JSON syntax is valid when editing `prompts.json`
- Python syntax must be correct when editing `prompts.py` 