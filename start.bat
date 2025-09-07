@echo off
cd /d "%~dp0"
python -m streamlit run src/streamlit_voice_analyzer.py
pause
