# Simple Text-to-Speech with voice and speed selection

import pyttsx3

def speak(text, rate=100):
    """
    Speak text with auto-selected best voice and custom rate
    """
    engine = pyttsx3.init()
    
    # Set speed and volume
    engine.setProperty('rate', rate)
    engine.setProperty('volume', 0.65)
    
    # Get available voices and select the best one
    voices = engine.getProperty('voices')
    
    # Use second voice if available (usually better quality)
    if len(voices) >= 2:
        engine.setProperty('voice', voices[1].id)
    elif len(voices) == 1:
        engine.setProperty('voice', voices[0].id)
    
    # Speak
    engine.say(text)
    engine.runAndWait()

def speak_with_voice_number(text, voice_number, rate=100):
    """
    Speak with specific voice number (1 or 2) and custom rate
    """
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    # Check if requested voice exists
    if voice_number and 1 <= voice_number <= len(voices):
        selected_voice = voices[voice_number - 1]
        engine.setProperty('voice', selected_voice.id)
    else:
        # Fallback to auto selection
        speak(text, rate)
        return
    
    # Set properties
    engine.setProperty('rate', rate)
    engine.setProperty('volume', 0.65)
    
    # Speak
    engine.say(text)
    engine.runAndWait()

def get_current_voice_info():
    """
    Returns info about auto-selected voice
    """
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    if len(voices) >= 2:
        return f"Auto: {voices[1].name}"
    elif len(voices) == 1:
        return f"Auto: {voices[0].name}"
    else:
        return "No voices available"
