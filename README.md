# AI Voice Test Analyzer

A Streamlit web application for analyzing HTML test reports with voice feedback. Upload test reports and get audio announcements of results, faults, and required component replacements.

## Features

- 🔊 **Voice Output** - Natural text-to-speech with multiple voice options
- 📄 **HTML Report Analysis** - Parses test reports and extracts key information
- 🎛️ **Customizable Settings** - Choose voice type and speech speed
- 🚀 **Web Interface** - Easy-to-use Streamlit dashboard
- 🔒 **Safe Operation** - Prevents multiple simultaneous voice operations

## Quick Start

1. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python -m streamlit run src/streamlit_voice_analyzer.py
   ```
   
   Or simply double-click `start.bat`

3. **Open your browser** and go to the displayed URL (usually `http://localhost:8501`)

## How to Use

1. **Configure Voice Settings** - Choose your preferred voice and speed in the sidebar
2. **Test Your Settings** - Click "Test Current Settings" to hear your voice configuration
3. **Upload Test Report** - Select an HTML test report file to analyze
4. **View Results** - Review the test status, faults, and components to replace
5. **Listen to Results** - Use "Quick Result" for status only or "Full Summary" for complete details

## Project Structure

```
ai_voice_analyzer/
├── src/                             # Source code
│   ├── streamlit_voice_analyzer.py  # Main Streamlit application
│   ├── voice_output_simple.py       # Text-to-speech functions
│   ├── report_parser.py             # HTML report parsing logic
│   └── __init__.py                  # Package initialization
├── data/                            # Sample data and reports
│   ├── test_report_pass.html
│   ├── test_report_fail.html
│   └── test_report_complex_fail.html
├── tests/                           # Test files
│   └── test_basic.py
├── scripts/                         # Utility scripts
├── requirements.txt                 # Project dependencies
├── start.bat                        # Quick start script
├── README.md                        # This file
└── .gitignore                       # Git ignore rules
```

## Sample Data

The `data/` folder contains example HTML test reports you can use to test the application:

- `test_report_pass.html` - Example of a passing test
- `test_report_fail.html` - Example of a failing test  
- `test_report_complex_fail.html` - Complex failure scenario

## Voice Options

- **David (Male Voice)** - Clear male voice
- **Zira (Female Voice)** - Clear female voice
- **Additional voices** - System-dependent options

## Requirements

- Python 3.7+
- Streamlit
- pyttsx3 (Text-to-speech)
- BeautifulSoup4 (HTML parsing)

## Troubleshooting

- **No voice output**: Check your system's audio settings
- **Buttons stuck**: Use the "Emergency Reset" button in the sidebar
- **File upload issues**: Ensure your HTML file is properly formatted

## License

This project is for educational and internal use.

---

## Developer Documentation

### API Reference

#### voice_output_simple.py
**Text-to-Speech functionality**

Functions:
- `speak(text, rate=100)` - Auto voice selection
- `speak_with_voice_number(text, voice_number, rate=100)` - Specific voice
- `get_current_voice_info()` - Voice information

Parameters:
- `text`: String to speak
- `voice_number`: 1=David, 2=Zira, 3+=additional voices  
- `rate`: Speech speed (80-150 WPM recommended)

#### report_parser.py
**HTML report analysis**

Functions:
- `parse_html_report(html_path)` - Parse HTML test report

Returns:
```python
{
    'status': 'pass'|'fail'|'unknown',
    'faults': ['fault1', 'fault2', ...],
    'replace': ['component1', 'component2', ...]
}
```

#### Usage Examples

**Voice Output:**
```python
from voice_output_simple import speak_with_voice_number

# Speak with David's voice at normal speed
speak_with_voice_number("Test passed", 1, rate=100)

# Speak with Zira's voice at faster speed
speak_with_voice_number("Analysis complete", 2, rate=130)
```

**Report Parsing:**
```python
from report_parser import parse_html_report

result = parse_html_report("test_report.html")
print(f"Status: {result['status']}")
print(f"Faults found: {len(result['faults'])}")
```
