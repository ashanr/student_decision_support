#!/usr/bin/env python3
"""
Student Migration Data Generator

This script creates synthetic student migration data for use with the
Student DSS recommendation system. The data follows the structure outlined
in the student-migration-database-documentation.md file.
"""

import os
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_student_data(num_records=1000):
    """Generate synthetic student data."""
    print(f"Generating {num_records} student records...")
    
    # Set random seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    # Lists for categorical data
    countries = [
        "Pakistan", "Iran", "Nepal", "India", "Nigeria", 
        "China", "Vietnam", "Brazil", "Mexico", "South Africa",
        "Indonesia", "Bangladesh", "Egypt", "Turkey", "Ukraine",
        "Russia", "Thailand", "Malaysia", "Colombia", "Kenya"
    ]
    
    destination_countries = [
        "United States", "Germany", "Canada", "United Kingdom", 
        "Australia", "France", "Netherlands", "Singapore", 
        "Japan", "Sweden", "Switzerland", "New Zealand", 
        "South Korea", "Italy", "Spain"
    ]
    
    fields_of_study = [
        "Medicine", "Chemistry", "Psychology", "Computer Science",
        "Business", "Engineering", "Physics", "Literature", 
        "Economics", "Biology", "Mathematics", "Law",
        "Architecture", "Agriculture", "Political Science",
        "Sociology", "Anthropology", "History", "Art", "Education"
    ]
    
    education_levels = ["High School", "Diploma", "Bachelor's", "Master's"]
    institution_types = ["Public", "Private", "International"]
    funding_sources = ["Family", "Loan", "Scholarship", "Self-funded", "Employer", "Government"]
    decision_styles = [
        "Analytical", "Intuitive", "Consultative", "Directive", 
        "Conceptual", "Behavioral", "Flexible", "Systematic"
    ]
    
    university_tiers = ["Tier 1 (Top 50)", "Tier 2 (51-200)", "Tier 3 (201-500)", 
                      "Tier 4 (501-1000)", "Tier 5 (1001+)"]
    
    # Generate random data for each student
    data = {
        "student_id": range(1, num_records + 1),
        "first_name": [f"Student{i}" for i in range(1, num_records + 1)],
        "last_name": [f"Lastname{i}" for i in range(1, num_records + 1)],
        "email": [f"student{i}@example.com" for i in range(1, num_records + 1)],
        "phone": [f"+1234567{i:04d}" for i in range(1, num_records + 1)],
        "date_of_birth": [(datetime.now() - timedelta(days=random.randint(18*365, 29*365))).strftime('%Y-%m-%d') 
                         for _ in range(num_records)],
        "gender": np.random.choice(["Male", "Female", "Other"], size=num_records, p=[0.323, 0.374, 0.303]),
        "nationality": np.random.choice(countries, size=num_records),
        "home_country": [],  # Will be filled below (mostly same as nationality)
        "home_city": [f"City-{i}" for i in range(num_records)],
        "native_language": [],  # Will be filled based on country
        
        # Academic background
        "current_gpa": np.random.uniform(2.5, 4.0, size=num_records).round(2),
        "previous_education_level": np.random.choice(education_levels, size=num_records, p=[0.27, 0.27, 0.23, 0.23]),
        "field_of_study": np.random.choice(fields_of_study, size=num_records),
        "institution_type": np.random.choice(institution_types, size=num_records),
        "standardized_test_score": np.random.randint(300, 340, size=num_records),  # Simplified GRE score
        "academic_achievements": np.random.randint(0, 11, size=num_records),
        "research_experience": np.random.choice([True, False], size=num_records),
        
        # Financial profile
        "family_income_bracket": np.random.choice(
            ["<$10K", "$10K-$25K", "$25K-$50K", "$50K-$75K", "$75K-$100K", ">$100K"], 
            size=num_records
        ),
        "financial_aid_needed": np.random.choice([True, False], size=num_records, p=[0.49, 0.51]),
        "tuition_budget": np.random.randint(15000, 80001, size=num_records),
        "living_expense_budget": np.random.randint(8000, 25001, size=num_records),
        "has_scholarship": np.random.choice([True, False], size=num_records, p=[0.35, 0.65]),
        "financial_support_source": np.random.choice(funding_sources, size=num_records),
        
        # Career aspirations (using fields as a base)
        "intended_career_field": [],  # Will be filled based on field_of_study
        "career_importance_score": np.random.randint(1, 11, size=num_records),
        "job_market_priority": np.random.randint(1, 11, size=num_records),
        "entrepreneurship_interest": np.random.randint(1, 11, size=num_records),
        "research_interest": np.random.randint(1, 11, size=num_records),
        "industry_preference": np.random.choice(
            ["Academia", "Corporate", "Government", "Non-profit", "Startup", "Research"], 
            size=num_records
        ),
        
        # Migration preferences
        "preferred_destinations": [],  # Will be filled with 1-3 countries
        "language_barrier_concern": np.random.randint(1, 11, size=num_records),
        "cultural_adaptation_confidence": np.random.randint(1, 11, size=num_records),
        "visa_processing_importance": np.random.randint(1, 11, size=num_records),
        "post_study_work_priority": np.random.randint(1, 11, size=num_records),
        "permanent_residence_interest": np.random.randint(1, 11, size=num_records),
        
        # Decision factors
        "family_influence_score": np.random.randint(1, 11, size=num_records),
        "peer_influence_score": np.random.randint(1, 11, size=num_records),
        "consultant_influence_score": np.random.randint(1, 11, size=num_records),
        "university_ranking_importance": np.random.randint(1, 11, size=num_records),
        "cost_sensitivity_score": np.random.randint(1, 11, size=num_records),
        "safety_importance_score": np.random.randint(1, 11, size=num_records),
        
        # Behavioral characteristics
        "risk_tolerance_score": np.random.randint(1, 11, size=num_records),
        "decision_making_style": np.random.choice(decision_styles, size=num_records),
        "information_seeking_behavior": np.random.choice(decision_styles, size=num_records),  # Reuse styles
        "technology_comfort_level": np.random.randint(1, 11, size=num_records),
        "social_network_size": np.random.randint(1, 11, size=num_records),
        "adaptability_score": np.random.randint(1, 11, size=num_records),
        
        # Application outcomes
        "applications_submitted": np.random.randint(3, 13, size=num_records),
        "acceptances_received": [],  # Will be calculated below
        "final_destination_country": [],  # Will be filled based on acceptances
        "final_university_tier": [],  # Will be filled randomly from tiers
        "application_success_rate": [],  # Will be calculated
        "decision_satisfaction_score": [],  # Will be calculated
        
        # Engagement metrics
        "consultation_sessions": np.random.randint(1, 16, size=num_records),
        "information_search_hours": np.random.randint(10, 201, size=num_records),
        "application_preparation_time": np.random.randint(30, 366, size=num_records),
        "decision_timeline_days": np.random.randint(30, 731, size=num_records),
        "stress_level_score": np.random.randint(1, 11, size=num_records),
        "confidence_level_score": np.random.randint(1, 11, size=num_records),
    }
    
    # Fill in derived fields
    for i in range(num_records):
        # Home country (95% same as nationality)
        data["home_country"].append(data["nationality"][i] if random.random() < 0.95 else random.choice(countries))
        
        # Native language (simple placeholder based on country)
        data["native_language"].append(data["nationality"][i] + " Language")
        
        # Intended career field (80% same as field of study)
        if random.random() < 0.8:
            data["intended_career_field"].append(data["field_of_study"][i])
        else:
            data["intended_career_field"].append(random.choice(fields_of_study))
        
        # Preferred destinations (1-3 countries)
        num_destinations = random.randint(1, 3)
        data["preferred_destinations"].append(
            ", ".join(random.sample(destination_countries, num_destinations))
        )
        
        # Application outcomes
        apps = data["applications_submitted"][i]
        # Acceptances should be <= applications
        acceptances = min(random.randint(0, 8), apps)
        data["acceptances_received"].append(acceptances)
        
        # Final destination (if any acceptances)
        if acceptances > 0:
            data["final_destination_country"].append(random.choice(destination_countries))
            data["final_university_tier"].append(random.choice(university_tiers))
        else:
            data["final_destination_country"].append(None)
            data["final_university_tier"].append(None)
        
        # Success rate
        if apps > 0:
            data["application_success_rate"].append(round(acceptances / apps * 100, 1))
        else:
            data["application_success_rate"].append(0)
        
        # Satisfaction (correlated with success rate but with noise)
        if acceptances > 0:
            base_satisfaction = data["application_success_rate"][i] / 100 * 10
            noise = random.uniform(-2, 2)
            satisfaction = max(1, min(10, round(base_satisfaction + noise)))
            data["decision_satisfaction_score"].append(satisfaction)
        else:
            data["decision_satisfaction_score"].append(random.randint(1, 4))  # Lower satisfaction for no acceptances
    
    # Create DataFrame
    df = pd.DataFrame(data)
    return df

def main():
    """Main function to generate and save student data."""
    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, "student_migration_data.csv")
    
    # Generate data
    student_data = generate_student_data()
    
    # Save to CSV
    student_data.to_csv(output_file, index=False)
    print(f"Generated {len(student_data)} student records and saved to {output_file}")
    
    # Save a subset to SQLite (if needed)
    try:
        import sqlite3
        db_path = os.path.join(script_dir, "studentDSS.db")
        
        # Connect to SQLite database
        conn = sqlite3.connect(db_path)
        
        # Save a subset of columns to a students table
        subset_columns = [
            "student_id", "field_of_study", "current_gpa", "tuition_budget",
            "living_expense_budget", "final_destination_country", 
            "final_university_tier", "decision_satisfaction_score",
            "university_ranking_importance", "cost_sensitivity_score",
            "career_importance_score"
        ]
        
        subset_df = student_data[subset_columns]
        subset_df.to_sql('students', conn, if_exists='replace', index=False)
        
        print(f"Also saved data to SQLite database at {db_path}")
        conn.close()
    except Exception as e:
        print(f"Note: Could not save to SQLite: {e}")

if __name__ == "__main__":
    main()
    main()
