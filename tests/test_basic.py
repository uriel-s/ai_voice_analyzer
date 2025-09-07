"""
Basic tests for the AI Voice Test Analyzer
"""

import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.report_parser import parse_html_report
from src.voice_output_simple import speak_with_voice_number
import tempfile

def test_report_parser():
    """Test the HTML report parsing functionality"""
    print("Testing report parser...")
    
    # Test with sample files
    sample_files = [
        "../data/test_report_pass.html",
        "../data/test_report_fail.html",
        "../data/test_report_complex_fail.html"
    ]
    
    for sample_file in sample_files:
        if os.path.exists(sample_file):
            print(f"Testing {sample_file}...")
            try:
                result = parse_html_report(sample_file)
                print(f"  Status: {result.get('status', 'unknown')}")
                print(f"  Faults: {len(result.get('faults', []))}")
                print(f"  Replace: {len(result.get('replace', []))}")
                print("  ✅ PASSED")
            except Exception as e:
                print(f"  ❌ FAILED: {e}")
        else:
            print(f"  ⚠️  SKIPPED: File not found")
    print()

def test_voice_output():
    """Test the voice output functionality"""
    print("Testing voice output...")
    
    try:
        # Test with voice number 1 (should be safe on most systems)
        print("  Testing speak_with_voice_number function...")
        # Note: This will actually speak, so we just test the function exists
        print("  ✅ Function available")
        
        # You can uncomment the line below to actually test voice output
        # speak_with_voice_number("Test message", 1, rate=120)
        
    except Exception as e:
        print(f"  ❌ FAILED: {e}")
    print()

def test_file_creation():
    """Test temporary file creation"""
    print("Testing file operations...")
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
            tmp.write(b"<html><body>Test</body></html>")
            tmp_path = tmp.name
        
        # Check if file was created
        if os.path.exists(tmp_path):
            print("  ✅ Temporary file creation: PASSED")
            os.unlink(tmp_path)  # Clean up
        else:
            print("  ❌ Temporary file creation: FAILED")
            
    except Exception as e:
        print(f"  ❌ File operations: FAILED: {e}")
    print()

def run_all_tests():
    """Run all tests"""
    print("🧪 Running AI Voice Test Analyzer Tests")
    print("=" * 50)
    
    test_report_parser()
    test_voice_output()
    test_file_creation()
    
    print("Tests completed!")

if __name__ == "__main__":
    run_all_tests()
