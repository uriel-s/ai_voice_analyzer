@echo off
echo Starting AI Voice Analyzer...
cd /d "%~dp0"

echo Checking dependencies...
pip install -r requirements.txt --quiet

echo Launching application...
python -m streamlit run src/streamlit_voice_analyzer.py
pause
