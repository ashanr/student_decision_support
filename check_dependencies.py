#!/usr/bin/env python3
"""
Dependency checker for Student DSS
Verifies all required files are present and accessible
"""

import os
import sys
import importlib

def check_file(filepath, required=True):
    """Check if a file exists and report status"""
    exists = os.path.exists(filepath)
    filename = os.path.basename(filepath)
    
    if exists:
        print(f"✓ Found {filename}")
    else:
        message = f"✗ Missing {filename}"
        if required:
            print(f"ERROR: {message}")
        else:
            print(f"WARNING: {message}")
    
    return exists

def check_import(module_name):
    """Check if a module can be imported"""
    try:
        importlib.import_module(module_name)
        print(f"✓ Successfully imported {module_name}")
        return True
    except ImportError as e:
        print(f"✗ Failed to import {module_name}: {e}")
        return False

def main():
    """Main function to check dependencies"""
    print("Checking Student DSS dependencies...\n")
    
    # Check essential files
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    files_to_check = [
        os.path.join(base_dir, "app.py"),
        os.path.join(base_dir, "course_selection_assistant.py"),
        os.path.join(base_dir, "student_data_analyzer.py"),
    ]
    
    data_dir = os.path.join(base_dir, "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Created missing data directory at {data_dir}")
    
    # Check each file
    missing_files = 0
    for file_path in files_to_check:
        if not check_file(file_path):
            missing_files += 1
    
    # Check Python imports
    print("\nChecking Python imports:")
    modules_to_check = ["pandas", "numpy", "sklearn", "flask", "tabulate", "colorama", "matplotlib"]
    missing_modules = 0
    
    for module in modules_to_check:
        if not check_import(module):
            missing_modules += 1
    
    # Try to import our own module
    try:
        sys.path.insert(0, base_dir)
        from student_data_analyzer import StudentDataAnalyzer
        print("✓ Successfully imported StudentDataAnalyzer class")
    except Exception as e:
        print(f"✗ Failed to import StudentDataAnalyzer: {e}")
        missing_modules += 1
    
    # Report results
    print("\nDependency check summary:")
    if missing_files == 0 and missing_modules == 0:
        print("All dependencies satisfied!")
    else:
        print(f"Found {missing_files} missing files and {missing_modules} import issues")
        print("Please resolve these issues before running the application")
        
        # Provide installation instructions
        if missing_modules > 0:
            print("\nTo install missing Python packages, run:")
            print("pip install -r requirements.txt")
            
            # Check if requirements.txt exists
            req_path = os.path.join(base_dir, "requirements.txt")
            if not os.path.exists(req_path):
                print("\nWARNING: requirements.txt not found!")
                print("You can install individual packages with:")
                for module in modules_to_check:
                    print(f"pip install {module}")

if __name__ == "__main__":
    main()
