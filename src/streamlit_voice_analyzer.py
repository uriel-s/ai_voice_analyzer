import streamlit as st
from report_parser import parse_html_report
from voice_output_simple import speak_with_voice_number
import tempfile
import pyttsx3

# Initialize session state
if 'is_speaking' not in st.session_state:
    st.session_state.is_speaking = False
if 'pending_voice_action' not in st.session_state:
    st.session_state.pending_voice_action = None
if 'voice_operation_count' not in st.session_state:
    st.session_state.voice_operation_count = 0
if 'uploaded_report' not in st.session_state:
    st.session_state.uploaded_report = None
if 'report_results' not in st.session_state:
    st.session_state.report_results = None

# Page configuration
st.set_page_config(
    page_title="AI Voice Test Analyzer", 
    page_icon="🔊", 
    layout="centered"
)

st.title("🔊 AI Voice Test Analyzer")
st.write("Upload a test report (HTML) to analyze and get voice feedback.")

# Sidebar for voice settings
st.sidebar.header("🎤 Voice Settings")

# Get available voices
engine = pyttsx3.init()
voices = engine.getProperty('voices')

# Voice selection mapping
voice_options = ["David (Male Voice)", "Zira (Female Voice)"]
if len(voices) > 2:
    for i in range(2, min(len(voices), 6)):  # Show up to 6 voices
        voice_options.append(f"Voice {i+1}")

selected_voice = st.sidebar.selectbox(
    "Choose Voice:",
    voice_options,
    help="Select your preferred voice"
)

# Map voice selection to voice number
voice_mapping = {
    "David (Male Voice)": 1,
    "Zira (Female Voice)": 2,
    "Voice 3": 3,
    "Voice 4": 4,
    "Voice 5": 5,
    "Voice 6": 6
}
voice_number = voice_mapping.get(selected_voice, 1)

# Speech speed setting
speech_speed = st.sidebar.slider(
    "Speech Speed:",
    min_value=80,
    max_value=150,
    value=100,
    step=10,
    help="Adjust how fast the voice speaks (words per minute)"
)

# Test button for current settings
test_disabled = st.session_state.is_speaking
if st.sidebar.button("🎵 Test Current Settings", disabled=test_disabled, key="test_voice_btn"):
    st.session_state.voice_operation_count += 1
    st.session_state.is_speaking = True
    st.session_state.pending_voice_action = {
        "type": "test",
        "voice_number": voice_number,
        "speed": speech_speed
    }
    st.rerun()

# Show speaking status in sidebar
if st.session_state.is_speaking:
    st.sidebar.warning("🔊 Speaking - All buttons disabled")
    # Emergency reset button
    if st.sidebar.button("🚨 Emergency Reset", key="emergency_reset_btn"):
        st.session_state.is_speaking = False
        st.session_state.pending_voice_action = None
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.info(f"Selected: {selected_voice}\nSpeed: {speech_speed} WPM")

# Show operation count
if st.session_state.voice_operation_count > 0:
    st.sidebar.caption(f"Voice operations: {st.session_state.voice_operation_count}")

# Main content area
uploaded_file = st.file_uploader("Choose a test report (HTML)", type=["html"])

# Handle file upload and store in session state
if uploaded_file:
    # Only process if it's a new file or first time
    if (st.session_state.uploaded_report is None or 
        st.session_state.uploaded_report.name != uploaded_file.name):
        
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name
        
        # Parse the HTML report and store results
        try:
            result = parse_html_report(tmp_path)
            st.session_state.uploaded_report = uploaded_file
            st.session_state.report_results = result
        except Exception as e:
            st.error(f"Error parsing HTML report: {str(e)}")
            st.session_state.uploaded_report = None
            st.session_state.report_results = None

# Display results if we have them
if st.session_state.report_results:
    result = st.session_state.report_results
    
    # Display results
    st.subheader("📊 Test Results:")
    
    # Status display
    status = result.get('status', 'unknown')
    if status == 'pass':
        st.success("✅ Test Passed")
    elif status == 'fail':
        st.error("❌ Test Failed")
    else:
        st.warning("⚠️ Unknown Status")
    
    # Faults section
    st.subheader("🔍 Detected Faults:")
    faults = result.get('faults', [])
    if faults:
        for fault in faults:
            st.write(f"• {fault}")
    else:
        st.write("No faults detected.")
    
    # Components to replace section
    st.subheader("🔧 Components to Replace:")
    replace_components = result.get('replace', [])
    if replace_components:
        for component in replace_components:
            st.write(f"🔧 {component}")
    else:
        st.write("No components need replacement.")
    
    # Voice announcement section
    st.subheader("🔊 Voice Announcements:")
    
    # Show current speaking status
    if st.session_state.is_speaking:
        st.warning("🎵 Speaking... All voice buttons are disabled until complete.")
    else:
        st.info("💡 Click a button below to hear the results")
    
    # Voice buttons (disabled during speaking)
    buttons_disabled = st.session_state.is_speaking
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📢 Quick Result", disabled=buttons_disabled, key="quick_result_btn"):
            st.session_state.voice_operation_count += 1
            st.session_state.is_speaking = True
            st.session_state.pending_voice_action = {
                "type": "quick",
                "status": status,
                "voice_number": voice_number,
                "speed": speech_speed
            }
            st.rerun()
    
    with col2:
        if st.button("🔊 Full Summary", disabled=buttons_disabled, key="full_summary_btn"):
            st.session_state.voice_operation_count += 1
            st.session_state.is_speaking = True
            st.session_state.pending_voice_action = {
                "type": "full",
                "status": status,
                "faults": faults,
                "replace": replace_components,
                "voice_number": voice_number,
                "speed": speech_speed
            }
            st.rerun()

# Process pending voice actions (executes after UI is rendered)
if st.session_state.pending_voice_action and st.session_state.is_speaking:
    action = st.session_state.pending_voice_action
    st.session_state.pending_voice_action = None
    
    try:
        if action["type"] == "test":
            # Test voice settings
            test_text = "This is a test of your current voice and speed settings"
            st.info("🎵 Testing voice settings...")
            speak_with_voice_number(test_text, action["voice_number"], rate=action["speed"])
            
        elif action["type"] == "quick":
            # Quick result announcement
            quick_msg = f"Test {'Passed' if action['status'] == 'pass' else 'Failed'}"
            st.info("🎵 Announcing quick result...")
            speak_with_voice_number(quick_msg, action["voice_number"], rate=action["speed"])
            
        elif action["type"] == "full":
            # Full summary announcement
            summary_parts = []
            summary_parts.append(f"Test {'Passed' if action['status'] == 'pass' else 'Failed'}")
            
            if action["faults"]:
                faults_text = "Faults detected: " + ", ".join(action["faults"][:3])
                if len(action["faults"]) > 3:
                    faults_text += f" and {len(action['faults']) - 3} more"
                summary_parts.append(faults_text)
            
            if action["replace"]:
                replace_text = "Components to replace: " + ", ".join(action["replace"][:3])
                if len(action["replace"]) > 3:
                    replace_text += f" and {len(action['replace']) - 3} more"
                summary_parts.append(replace_text)
            
            summary = ". ".join(summary_parts) + "."
            st.info("🎵 Announcing full summary...")
            speak_with_voice_number(summary, action["voice_number"], rate=action["speed"])
    
    except Exception as e:
        st.error(f"Voice operation failed: {str(e)}")
    
    finally:
        # Always clear speaking state
        st.session_state.is_speaking = False
        st.rerun()

# Instructions
with st.expander("ℹ️ How to Use"):
    st.write("""
    1. **Configure Voice Settings** - Choose your preferred voice and speed in the sidebar
    2. **Test Your Settings** - Click "Test Current Settings" to hear your voice configuration
    3. **Upload Test Report** - Select an HTML test report file to analyze
    4. **View Results** - Review the test status, faults, and components to replace
    5. **Listen to Results** - Use "Quick Result" for status only or "Full Summary" for complete details
    
    **Note:** Only one voice operation can run at a time. All buttons are disabled during voice playback.
    """)
