# This file is no longer needed - all updates have been applied to the main files
# Consider removing this file entirely
Script to update the course_selection_assistant.py file to use the new database structure.
This is a utility script that demonstrates how to modify the existing code.
"""

import os
import fileinput
import sys
import re
from pathlib import Path

def check_required_files():
    """Check if all required files exist."""
    required_files = [
        "course_selection_assistant.py",
        "student_data_analyzer.py",
        "app.py",
        "__init__.py"  # Add the new file to check
    ]
    
    base_dir = os.path.dirname(__file__)
    missing_files = []
    
    for filename in required_files:
        file_path = os.path.join(base_dir, filename)
        if not os.path.exists(file_path):
            missing_files.append(filename)
    
    if missing_files:
        print(f"Error: The following required files are missing: {', '.join(missing_files)}")
        print("Please ensure all required files are present before updating.")
        return False
    
    return True

def update_course_selection_assistant():
    """Update the course_selection_assistant.py file to use the new database structure."""
    # First check if all required files exist
    if not check_required_files():
        return False
        
    file_path = os.path.join(os.path.dirname(__file__), "course_selection_assistant.py")
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return False
    
    # Make a backup of the original file
    backup_path = file_path + ".bak"
    try:
        with open(file_path, 'r') as source_file:
            source_content = source_file.read()
            
        with open(backup_path, 'w') as backup_file:
            backup_file.write(source_content)
            
        print(f"Created backup of original file at {backup_path}")
    except Exception as e:
        print(f"Error creating backup: {e}")
        return False
    
    # Modifications to make
    modifications = [
        {
            "pattern": r"self\.db_path = os\.path\.join\(os\.path\.dirname\(os\.path\.dirname\(os\.path\.dirname\(__file__\)\)\),\s*\"data\", \"studentDSS\.db\"\)",
            "replacement": "self.db_path = os.path.join(os.path.dirname(__file__), \"data\", \"studentDSS.db\")"
        },
        {
            "pattern": r"self\.load_data\(\)",
            "replacement": "self.load_data()\n        # Initialize student data analyzer\n        self.student_analyzer.load_data()\n        self.student_analyzer.build_recommendation_model()"
        },
        {
            "pattern": r"top_programs = self\.display_recommendations\(scored_programs\)",
            "replacement": "# Enhance recommendations using student data\n        print(f\"\\n{Fore.CYAN}Enhancing recommendations with student migration data...{Style.RESET_ALL}\")\n        enhanced_programs = self.student_analyzer.enhance_recommendations(scored_programs, self.user_preferences)\n        \n        top_programs = self.display_recommendations(enhanced_programs)"
        },
        {
            "pattern": r"self\.visualize_results\(scored_programs\)",
            "replacement": "self.visualize_results(enhanced_programs)"
        }
    ]
    
    try:
        # Apply modifications
        with open(file_path, 'r') as file:
            content = file.read()
        
        for mod in modifications:
            content = re.sub(mod["pattern"], mod["replacement"], content)
        
        with open(file_path, 'w') as file:
            file.write(content)
        
        print(f"Successfully updated {file_path}")
        return True
    except Exception as e:
        print(f"Error updating file: {e}")
        # Restore from backup
        try:
            with open(backup_path, 'r') as backup_file:
                original_content = backup_file.read()
                
            with open(file_path, 'w') as source_file:
                source_file.write(original_content)
                
            print(f"Restored original file from backup")
        except Exception as restore_err:
            print(f"Error restoring from backup: {restore_err}")
        
        return False

def main():
    """Main function."""
    print("Updating course_selection_assistant.py to use new database structure...")
    if update_course_selection_assistant():
        print("Update successful!")
        print("\nTo complete the setup:")
        print("1. Run 'python data/initialize_database.py' to create and populate the database")
        print("2. Make sure student_data_analyzer.py is in place and importable")
        print("3. Run 'python check_dependencies.py' to verify all dependencies")
        print("4. Run the updated course_selection_assistant.py")
    else:
        print("Update failed. Please update the file manually.")

if __name__ == "__main__":
    main()
