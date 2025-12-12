"""
Streamlit Cloud Entry Point
===========================
Standalone entry point for Streamlit Cloud deployment.
"""

import streamlit as st
import sys
import os

# Ensure src is in path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Now import with error handling
try:
    from src.gui import main
    main()
except ImportError as e:
    st.error(f"Import Error: {e}")
    st.info("Checking file structure...")
    
    # Debug info
    st.write("**Current directory:**", os.getcwd())
    st.write("**Root dir:**", ROOT_DIR)
    st.write("**Files in root:**", os.listdir(ROOT_DIR))
    
    if os.path.exists(os.path.join(ROOT_DIR, 'src')):
        st.write("**Files in src/:**", os.listdir(os.path.join(ROOT_DIR, 'src')))
    else:
        st.error("❌ 'src' folder not found!")
        st.info("Make sure 'src' folder is uploaded to GitHub.")
