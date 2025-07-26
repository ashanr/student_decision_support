from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import sqlite3
import pandas as pd
from datetime import datetime

# Simplified import
try:
    from course_selection_assistant import CourseSelectionAssistant
    from student_data_analyzer import StudentDataAnalyzer
except ImportError:
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from course_selection_assistant import CourseSelectionAssistant
    from student_data_analyzer import StudentDataAnalyzer

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the student data analyzer
student_analyzer = StudentDataAnalyzer()

# Load student data on startup - replace deprecated before_first_request
def initialize_data():
    """Load student data on server startup"""
    try:
        student_analyzer.load_data()
        student_analyzer.build_recommendation_model()
    except Exception as e:
        app.logger.error(f"Error initializing student data: {e}")

# Call initialization function
with app.app_context():
    initialize_data()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for the Python API."""
    try:
        # Simplified database path
        db_path = os.path.join(os.path.dirname(__file__), "data", "studentDSS.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT 1')
        cursor.fetchone()
        conn.close()
        
        return jsonify({
            "status": "ok",
            "timestamp": datetime.now().isoformat(),
            "service": "python-api",
            "database": "connected"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "timestamp": datetime.now().isoformat(),
            "service": "python-api",
            "error": str(e)
        }), 500

@app.route('/api/python/recommendations', methods=['POST'])
def get_recommendations():
    """Generate course recommendations based on user preferences."""
    try:
        # Get user preferences from request
        preferences = request.json
        
        # Add preference validation and normalization
        if not validate_preferences(preferences):
            return jsonify({
                "success": False,
                "error": "Invalid preference format"
            }), 400
            
        # Add preference enrichment with defaults for missing values
        preferences = enrich_preferences(preferences)
        
        # Initialize the course selection assistant
        assistant = CourseSelectionAssistant()
        
        # Connect to database
        if not assistant.connect_to_database():
            return jsonify({
                "success": False,
                "error": "Failed to connect to database"
            }), 500
            
        # Load data
        if not assistant.load_data():
            return jsonify({
                "success": False,
                "error": "Failed to load data"
            }), 500
            
        # Set user preferences
        assistant.user_preferences = preferences
        
        # Filter programs based on preferences
        filtered_programs = assistant.filter_programs()
        
        # Score and rank programs
        scored_programs = assistant.score_programs(filtered_programs)
        
        # Apply diversity boosting to ensure varied recommendations
        scored_programs = assistant.apply_diversity_boosting(scored_programs)
        
        # Enhance recommendations with student data insights
        enhanced_programs = student_analyzer.enhance_recommendations(scored_programs, preferences)
        
        # Add explanation generation for recommendations
        explanations = assistant.generate_explanations(enhanced_programs.head(10))
        
        # Convert DataFrame to dict for JSON serialization
        if enhanced_programs is not None:
            top_programs = enhanced_programs.head(10)
            result = []
            for i, (_, program) in enumerate(top_programs.iterrows()):
                program_dict = program.to_dict()
                # Clean up any non-serializable objects
                for key, value in program_dict.items():
                    if not isinstance(value, (str, int, float, bool, list, dict, type(None))):
                        program_dict[key] = str(value)
                
                # Add explanation for this recommendation
                program_dict['explanation'] = explanations[i] if i < len(explanations) else ""
                result.append(program_dict)
        else:
            result = []
            
        # Track recommendation performance for future improvement
        log_recommendation_event(preferences, result)
            
        return jsonify({
            "success": True,
            "recommendations": result
        })
        
    except Exception as e:
        app.logger.error(f"Error generating recommendations: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/python/countries', methods=['GET'])
def get_countries():
    """Get all countries from the database."""
    try:
        # Connect to database
        db_path = os.path.join(os.path.dirname(__file__), "data", "studentDSS.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # This enables column access by name
        cursor = conn.cursor()
        
        # Query all countries
        cursor.execute('SELECT * FROM countries')
        countries = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify(countries)
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/python/universities', methods=['GET'])
def get_universities():
    """Get all universities with optional filtering."""
    try:
        # Get query parameters
        country = request.args.get('country')
        limit = int(request.args.get('limit', 100))
        offset = int(request.args.get('offset', 0))
        
        # Simplified database path
        db_path = os.path.join(os.path.dirname(__file__), "data", "studentDSS.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Build query
        query = "SELECT * FROM universities WHERE 1=1"
        params = []
        
        if country:
            query += " AND country = ?"
            params.append(country)
            
        query += " LIMIT ? OFFSET ?"
        params.append(limit)
        params.append(offset)
        
        # Execute query
        cursor.execute(query, params)
        universities = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify({
            "success": True,
            "count": len(universities),
            "universities": universities
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# New helper functions to improve accuracy
def validate_preferences(preferences):
    """Validate that preferences contain required fields and proper value types"""
    required_fields = ['field_of_study', 'degree_level']
    for field in required_fields:
        if field not in preferences:
            return False
    return True

def enrich_preferences(preferences):
    """Add default values for missing preferences to improve matching accuracy"""
    enriched = preferences.copy()
    
    # Add defaults for common missing fields
    if 'max_tuition' not in enriched:
        enriched['max_tuition'] = 50000
    if 'preferred_countries' not in enriched or not enriched['preferred_countries']:
        enriched['preferred_countries'] = []
    if 'language_preference' not in enriched:
        enriched['language_preference'] = 'Any language with English programs'
        
    return enriched

def log_recommendation_event(preferences, results):
    """Log recommendation data for future analysis and algorithm improvement"""
    try:
        timestamp = datetime.now().isoformat()
        log_entry = {
            'timestamp': timestamp,
            'preferences': preferences,
            'results_count': len(results),
            'top_match_score': results[0]['match_percentage'] if results else None
        }
        
        # In a production system, this would write to a database or log file
        print(f"Recommendation log: {json.dumps(log_entry)}")
    except Exception as e:
        print(f"Error logging recommendation: {e}")

# Add a new endpoint for getting similar student profiles
@app.route('/api/python/similar-students', methods=['POST'])
def get_similar_students():
    """Find similar students based on provided preferences."""
    try:
        preferences = request.json
        
        if not student_analyzer.student_data is not None:
            # Load data if not already loaded
            student_analyzer.load_data()
            student_analyzer.build_recommendation_model()
        
        similar_students = student_analyzer.find_similar_students(preferences)
        
        if similar_students is None:
            return jsonify({
                "success": False,
                "error": "Could not find similar students"
            }), 404
            
        # Clean the data for JSON serialization
        result = []
        for _, student in similar_students.iterrows():
            student_dict = {
                "id": int(student["student_id"]),
                "field_of_study": student["field_of_study"],
                "gpa": float(student["current_gpa"]),
                "final_destination": student["final_destination_country"] 
                    if "final_destination_country" in student and pd.notna(student["final_destination_country"]) else None,
                "satisfaction_score": int(student["decision_satisfaction_score"]) 
                    if "decision_satisfaction_score" in student and pd.notna(student["decision_satisfaction_score"]) else None
            }
            result.append(student_dict)
            
        return jsonify({
            "success": True,
            "similar_students": result
        })
        
    except Exception as e:
        app.logger.error(f"Error finding similar students: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Fix duplicate app.run() by keeping only one instance
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
