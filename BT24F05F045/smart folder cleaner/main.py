"""
Smart Folder Cleaner — Main Entry Point
========================================
A professional GUI application built entirely with Python's built-in
tkinter library. No Flask, no web browser, no external packages needed.

Run with:   python main.py
Requires:   Python 3.8+  (tkinter is included with Python)
"""
import tkinter as tk
import config
from gui import SmartCleanerApp


def setup_high_dpi():
    """On Windows, prevent blurry text on high-DPI screens."""
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass


def main():
    """Initialize and run the application."""
    root = tk.Tk()
    root.title(config.WINDOW_TITLE)
    
    setup_high_dpi()
    app = SmartCleanerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
