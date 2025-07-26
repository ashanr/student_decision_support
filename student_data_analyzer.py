"""
Student Migration Data Analyzer

This module provides functionality to analyze student migration data
and enhance university program recommendations based on historical patterns.
"""

import os
import pandas as pd
import numpy as np

# Remove unused sklearn import handling - use simple try/except
try:
    from sklearn.neighbors import NearestNeighbors
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

class StudentDataAnalyzer:
    """Class for analyzing student migration data and enhancing recommendations."""
    
    def __init__(self, data_path=None):
        """Initialize the StudentDataAnalyzer with data path."""
        if data_path is None:
            self.data_path = os.path.join(os.path.dirname(__file__), "data", "student_migration_data.csv")
        else:
            self.data_path = data_path
            
        self.student_data = None
        self.model = None
        self.feature_columns = None
        self.normalized_features = None
        
    def load_data(self):
        """Load student migration data from CSV."""
        try:
            # Check if file exists
            if not os.path.exists(self.data_path):
                print(f"Warning: Student migration data not found at {self.data_path}")
                return False
                
            # Load the data
            self.student_data = pd.read_csv(self.data_path)
            print(f"Loaded student migration data: {len(self.student_data)} records")
            return True
        except Exception as e:
            print(f"Error loading student data: {e}")
            return False
            
    def build_recommendation_model(self):
        """Build a nearest neighbor model for finding similar students."""
        if self.student_data is None or len(self.student_data) == 0:
            print("No student data available for building model")
            return False
            
        if not SKLEARN_AVAILABLE:
            print("Warning: scikit-learn not available, similarity matching will be limited")
            return False
            
        try:
            # Select features for similarity matching
            self.feature_columns = [
                'current_gpa', 
                'tuition_budget', 
                'living_expense_budget',
                'university_ranking_importance',
                'cost_sensitivity_score',
                'career_importance_score'
            ]
            
            # Filter to features that exist in the data
            self.feature_columns = [col for col in self.feature_columns if col in self.student_data.columns]
            
            if not self.feature_columns:
                print("No usable feature columns found in data")
                return False
                
            # Extract features
            features = self.student_data[self.feature_columns].copy()
            
            # Handle missing values
            features = features.fillna(features.mean())
            
            # Normalize features
            self.normalized_features = (features - features.mean()) / features.std()
            
            # Build nearest neighbors model
            self.model = NearestNeighbors(n_neighbors=min(10, len(self.normalized_features)), 
                                         metric='euclidean')
            self.model.fit(self.normalized_features)
            
            print("Successfully built recommendation model")
            return True
        except Exception as e:
            print(f"Error building recommendation model: {e}")
            return False
            
    def find_similar_students(self, preferences, n=5):
        """Find similar students based on provided preferences."""
        if self.model is None or self.normalized_features is None:
            return None
            
        try:
            # Extract and normalize query features
            query_features = []
            for col in self.feature_columns:
                # Handle mapping from preferences to feature columns
                if col == 'current_gpa' and 'gpa' in preferences:
                    val = preferences['gpa']
                elif col == 'university_ranking_importance' and 'ranking_importance' in preferences:
                    val = preferences['ranking_importance']
                elif col == 'cost_sensitivity_score' and 'cost_sensitivity' in preferences:
                    val = preferences['cost_sensitivity']
                else:
                    val = preferences.get(col, None)
                    
                # Use mean if value not provided
                if val is None:
                    val = self.student_data[col].mean()
                    
                query_features.append(val)
                
            # Normalize query using same parameters as training data
            means = self.normalized_features.mean()
            stds = self.normalized_features.std()
            normalized_query = [(query_features[i] - means[i]) / stds[i] for i in range(len(query_features))]
            
            # Find nearest neighbors
            distances, indices = self.model.kneighbors([normalized_query], n_neighbors=min(n, len(self.normalized_features)))
            
            # Get similar student records
            similar_students = self.student_data.iloc[indices[0]]
            
            return similar_students
        except Exception as e:
            print(f"Error finding similar students: {e}")
            return None
            
    def enhance_recommendations(self, recommendations, preferences):
        """Enhance recommendations with insights from student data."""
        if recommendations is None or len(recommendations) == 0:
            return recommendations
            
        if self.student_data is None or len(self.student_data) == 0:
            return recommendations
            
        try:
            # Find similar students
            similar_students = self.find_similar_students(preferences, n=10)
            
            if similar_students is None or len(similar_students) == 0:
                return recommendations
                
            # Create a copy of recommendations to avoid modifying original
            enhanced = recommendations.copy()
            
            # Calculate destination popularity among similar students
            destination_counts = similar_students['final_destination_country'].value_counts()
            total_destinations = sum(destination_counts)
            
            # Boost scores based on destination popularity
            for idx, row in enhanced.iterrows():
                country = row['country']
                
                # Calculate popularity boost (0-0.05 range)
                popularity = destination_counts.get(country, 0) / max(1, total_destinations)
                popularity_boost = popularity * 0.05
                
                # Apply the boost to the final score
                if 'final_score' in row:
                    rec_idx = idx  # Get the index of the current recommendation
                    enhanced.at[rec_idx, 'student_data_boost'] = popularity_boost
                    enhanced.at[rec_idx, 'final_score'] += popularity_boost
                    
                    # Update match percentage
                    if 'match_percentage' in row:
                        enhanced.at[rec_idx, 'match_percentage'] = min(100, (enhanced.at[rec_idx, 'final_score'] * 100).round(1))
            
            # Sort by the enhanced final score
            if 'final_score' in enhanced.columns:
                enhanced = enhanced.sort_values(by='final_score', ascending=False)
            
            # Generate explanations for student data influence
            self._add_student_data_explanations(enhanced, similar_students)
            
            return enhanced
        except Exception as e:
            print(f"Error enhancing recommendations: {e}")
            return recommendations
    
    def get_popularity_boost(self, university_name=None, country=None, field=None):
        """Get a boost score based on the popularity of a university/country/field."""
        if self.student_data is None:
            return 0.0
            
        try:
            boost = 0.0
            
            # Country popularity (0-0.03)
            if country and 'final_destination_country' in self.student_data.columns:
                country_counts = self.student_data['final_destination_country'].value_counts()
                total_countries = sum(country_counts)
                country_popularity = country_counts.get(country, 0) / max(1, total_countries)
                boost += country_popularity * 0.03
                
            # Field popularity (0-0.02)
            if field and 'field_of_study' in self.student_data.columns:
                field_counts = self.student_data['field_of_study'].value_counts()
                total_fields = sum(field_counts)
                field_popularity = field_counts.get(field, 0) / max(1, total_fields)
                boost += field_popularity * 0.02
                
            return boost
        except Exception as e:
            print(f"Error calculating popularity boost: {e}")
            return 0.0
    
    def _add_student_data_explanations(self, recommendations, similar_students):
        """Add explanations about similar students to recommendations."""
        if len(similar_students) == 0 or recommendations is None:
            return
            
        try:
            for idx, rec in recommendations.iterrows():
                country = rec['country'] if 'country' in rec else None
                field = rec['field'] if 'field' in rec else None
                boost = rec['student_data_boost'] if 'student_data_boost' in rec else 0
                
                # Skip if no boost or no explanation field
                if boost <= 0 or 'explanation' not in recommendations.columns:
                    continue
                
                # Find matching students for this recommendation
                matches = similar_students[
                    (similar_students['final_destination_country'] == country) &
                    (similar_students['decision_satisfaction_score'] >= 7)  # Only high satisfaction
                ]
                
                # Add explanation about similar students if there are matches
                if len(matches) > 0:
                    # Get current explanation or empty string
                    current_explanation = recommendations.at[idx, 'explanation'] or ""
                    
                    # Add student data insight
                    student_insight = (f" Similar students to your profile have been "
                                     f"satisfied with programs in {country}.")
                    
                    # Append to existing explanation
                    if current_explanation.endswith("."):
                        recommendations.at[idx, 'explanation'] = current_explanation + student_insight
                    else:
                        recommendations.at[idx, 'explanation'] = current_explanation + "." + student_insight
        except Exception as e:
            print(f"Error adding student data explanations: {e}")

    def analyze_satisfaction_factors(self):
        """Analyze which factors correlate with student satisfaction."""
        if self.student_data is None or len(self.student_data) == 0:
            return {}
            
        try:
            # Potential factors that might influence satisfaction
            potential_factors = [
                'university_ranking_importance', 'cost_sensitivity_score',
                'safety_importance_score', 'career_importance_score',
                'confidence_level_score', 'risk_tolerance_score'
            ]
            
            # Filter to factors that exist in the data
            factors = [f for f in potential_factors if f in self.student_data.columns]
            
            if not factors or 'decision_satisfaction_score' not in self.student_data.columns:
                return {}
            
            # Calculate correlations
            correlations = {}
            for factor in factors:
                corr = self.student_data[factor].corr(self.student_data['decision_satisfaction_score'])
                correlations[factor] = corr
                
            return correlations
        except Exception as e:
            print(f"Error analyzing satisfaction factors: {e}")
            return {}
                                     f"satisfied with programs in {country}.")
                    
                    # Append to existing explanation
                    if current_explanation.endswith("."):
                        recommendations.at[idx, 'explanation'] = current_explanation + student_insight
                    else:
                        recommendations.at[idx, 'explanation'] = current_explanation + "." + student_insight
        except Exception as e:
            print(f"Error adding student data explanations: {e}")
            print(f"Error adding student data explanations: {e}")

    def analyze_satisfaction_factors(self):
        """Analyze which factors correlate with student satisfaction."""
        if self.student_data is None or len(self.student_data) == 0:
            return {}
            
        try:
            # Potential factors that might influence satisfaction
            potential_factors = [
                'university_ranking_importance', 'cost_sensitivity_score',
                'safety_importance_score', 'career_importance_score',
                'confidence_level_score', 'risk_tolerance_score'
            ]
            
            # Filter to factors that exist in the data
            factors = [f for f in potential_factors if f in self.student_data.columns]
            
            if not factors or 'decision_satisfaction_score' not in self.student_data.columns:
                return {}
            
            # Calculate correlations
            correlations = {}
            for factor in factors:
                corr = self.student_data[factor].corr(self.student_data['decision_satisfaction_score'])
                correlations[factor] = corr
                
            return correlations
        except Exception as e:
            print(f"Error analyzing satisfaction factors: {e}")
            return {}
