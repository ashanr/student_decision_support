#!/usr/bin/env python3
"""
Cleanup script for Student DSS.
Removes deprecated files and performs system cleanup.
"""

import os
import shutil
import time

def backup_file(filepath):
    """Create a backup of a file before removing it."""
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return False
        
    backup_dir = os.path.join(os.path.dirname(filepath), "backups")
    os.makedirs(backup_dir, exist_ok=True)
    
    filename = os.path.basename(filepath)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    backup_path = os.path.join(backup_dir, f"{filename}.{timestamp}.bak")
    
    try:
        shutil.copy2(filepath, backup_path)
        print(f"Created backup at: {backup_path}")
        return True
    except Exception as e:
        print(f"Error creating backup: {e}")
        return False

def remove_deprecated_files():
    """Remove files that are no longer needed."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    deprecated_files = [
        "update_course_selection_assistant.py"
    ]
    
    for filename in deprecated_files:
        filepath = os.path.join(base_dir, filename)
        if os.path.exists(filepath):
            print(f"Found deprecated file: {filename}")
            if backup_file(filepath):
                try:
                    os.remove(filepath)
                    print(f"Removed: {filename}")
                except Exception as e:
                    print(f"Error removing file: {e}")
            else:
                print(f"Skipped removal due to backup failure: {filename}")
        else:
            print(f"Deprecated file not found: {filename}")

if __name__ == "__main__":
    print("Starting system cleanup...")
    remove_deprecated_files()
    print("Cleanup complete!")
