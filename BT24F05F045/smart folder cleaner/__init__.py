"""
Smart Folder Cleaner Package
=============================
A professional, modular tkinter desktop application for folder organization.
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__description__ = "Smart Folder Cleaner - Organize and deduplicate your folders with ease"

from gui import SmartCleanerApp
from core import scan_folder, execute_cleaning, get_file_category

__all__ = ["SmartCleanerApp", "scan_folder", "execute_cleaning", "get_file_category"]
