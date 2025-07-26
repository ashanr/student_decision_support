#!/usr/bin/env python3
"""
Database Initialization Script

This script creates the necessary database tables for the Student DSS system,
including universities, countries, cities, and programs.
"""

import os
import sqlite3
import pandas as pd
import csv
import json
from pathlib import Path

def create_database(db_path="studentDSS.db"):
    """Create and initialize the database with required tables."""
    # Make sure the directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Connect to the database (will create if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print(f"Creating database at {db_path}...")
    
    # Create countries table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS countries (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        code TEXT NOT NULL UNIQUE,
        region TEXT,
        language TEXT,
        average_living_cost REAL,
        average_tuition_cost REAL,
        safety_index INTEGER,
        quality_of_life_index INTEGER
    )
    ''')
    
    # Create cities table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cities (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        country_id INTEGER,
        population INTEGER,
        cost_of_living_index REAL,
        student_friendly_score INTEGER,
        FOREIGN KEY (country_id) REFERENCES countries(id),
        UNIQUE(name, country_id)
    )
    ''')
    
    # Create universities table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS universities (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        country_id INTEGER,
        city_id INTEGER,
        city TEXT, 
        country TEXT,
        ranking_global INTEGER,
        ranking_national INTEGER,
        student_count INTEGER,
        established_year INTEGER,
        website TEXT,
        FOREIGN KEY (country_id) REFERENCES countries(id),
        FOREIGN KEY (city_id) REFERENCES cities(id)
    )
    ''')
    
    # Create programs table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS programs (
        id INTEGER PRIMARY KEY,
        name_program TEXT NOT NULL,
        university_id INTEGER,
        field TEXT,
        level TEXT,
        language TEXT,
        duration INTEGER,
        tuition_per_year REAL,
        application_fee REAL,
        admission_requirements TEXT,
        FOREIGN KEY (university_id) REFERENCES universities(id)
    )
    ''')
    
    # Create fields_of_study reference table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS fields_of_study (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        category TEXT,
        employment_growth_rate REAL,
        average_starting_salary REAL
    )
    ''')
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    
    print("Database schema created successfully.")
    return True

def seed_sample_data(db_path="studentDSS.db"):
    """Seed the database with sample data for testing."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("Seeding database with sample data...")
    
    # Sample countries data
    countries = [
        (1, "United States", "US", "North America", "English", 1800, 35000, 70, 80),
        (2, "Germany", "DE", "Europe", "German", 1000, 1500, 80, 85),
        (3, "Canada", "CA", "North America", "English/French", 1500, 25000, 85, 90),
        (4, "United Kingdom", "UK", "Europe", "English", 1700, 30000, 75, 82),
        (5, "Australia", "AU", "Oceania", "English", 1600, 32000, 82, 88),
        (6, "France", "FR", "Europe", "French", 1200, 2000, 78, 83),
        (7, "Netherlands", "NL", "Europe", "Dutch", 1300, 12000, 83, 88),
        (8, "Singapore", "SG", "Asia", "English/Mandarin", 2000, 35000, 90, 85),
        (9, "Japan", "JP", "Asia", "Japanese", 1400, 15000, 88, 80),
        (10, "Sweden", "SE", "Europe", "Swedish", 1500, 0, 85, 90)
    ]
    
    cursor.executemany('''
    INSERT OR REPLACE INTO countries (id, name, code, region, language, average_living_cost, average_tuition_cost, safety_index, quality_of_life_index)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', countries)
    
    # Sample cities data
    cities = [
        (1, "New York", 1, 8400000, 100, 8),
        (2, "Boston", 1, 695000, 95, 9),
        (3, "Munich", 2, 1500000, 80, 9),
        (4, "Berlin", 2, 3700000, 75, 9),
        (5, "Toronto", 3, 2900000, 85, 9),
        (6, "Vancouver", 3, 675000, 90, 9),
        (7, "London", 4, 8900000, 95, 8),
        (8, "Sydney", 5, 5300000, 90, 9),
        (9, "Paris", 6, 2100000, 90, 8),
        (10, "Amsterdam", 7, 820000, 85, 9),
        (11, "Singapore", 8, 5700000, 95, 8),
        (12, "Tokyo", 9, 13900000, 85, 8),
        (13, "Stockholm", 10, 975000, 80, 9)
    ]
    
    cursor.executemany('''
    INSERT OR REPLACE INTO cities (id, name, country_id, population, cost_of_living_index, student_friendly_score)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', cities)
    
    # Sample universities data
    universities = [
        (1, "Massachusetts Institute of Technology", 1, 2, "Boston", "United States", 1, 1, 11000, 1861, "http://web.mit.edu/"),
        (2, "Harvard University", 1, 2, "Boston", "United States", 2, 2, 23000, 1636, "https://www.harvard.edu/"),
        (3, "Technical University of Munich", 2, 3, "Munich", "Germany", 50, 1, 40000, 1868, "https://www.tum.de/en/"),
        (4, "Humboldt University of Berlin", 2, 4, "Berlin", "Germany", 80, 3, 35000, 1810, "https://www.hu-berlin.de/en"),
        (5, "University of Toronto", 3, 5, "Toronto", "Canada", 25, 1, 95000, 1827, "https://www.utoronto.ca/"),
        (6, "University of British Columbia", 3, 6, "Vancouver", "Canada", 35, 2, 65000, 1908, "https://www.ubc.ca/"),
        (7, "Imperial College London", 4, 7, "London", "United Kingdom", 10, 3, 19000, 1907, "https://www.imperial.ac.uk/"),
        (8, "University of Sydney", 5, 8, "Sydney", "Australia", 40, 1, 70000, 1850, "https://www.sydney.edu.au/"),
        (9, "Sorbonne University", 6, 9, "Paris", "France", 90, 1, 55000, 1253, "https://www.sorbonne-universite.fr/en"),
        (10, "University of Amsterdam", 7, 10, "Amsterdam", "Netherlands", 65, 1, 30000, 1632, "https://www.uva.nl/en"),
        (11, "National University of Singapore", 8, 11, "Singapore", "Singapore", 15, 1, 40000, 1905, "https://www.nus.edu.sg/"),
        (12, "University of Tokyo", 9, 12, "Tokyo", "Japan", 30, 1, 28000, 1877, "https://www.u-tokyo.ac.jp/en/"),
        (13, "KTH Royal Institute of Technology", 10, 13, "Stockholm", "Sweden", 70, 1, 15000, 1827, "https://www.kth.se/en")
    ]
    
    cursor.executemany('''
    INSERT OR REPLACE INTO universities (id, name, country_id, city_id, city, country, ranking_global, ranking_national, student_count, established_year, website)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', universities)
    
    # Sample programs data
    programs = [
        (1, "Master of Computer Science", 1, "Computer Science", "Master", "English", 2, 50000, 75, "GRE, 3.5+ GPA, TOEFL"),
        (2, "MBA", 2, "Business", "Master", "English", 2, 70000, 100, "GMAT, 2+ years work experience"),
        (3, "Master of Data Science", 3, "Computer Science", "Master", "English", 2, 1500, 50, "Bachelor in CS or related field, GRE"),
        (4, "PhD in Physics", 4, "Physics", "PhD", "German/English", 4, 0, 0, "Master's degree, research proposal"),
        (5, "Master of Computer Science", 5, "Computer Science", "Master", "English", 2, 25000, 120, "GRE, B+ average"),
        (6, "Bachelor of Engineering", 6, "Engineering", "Bachelor", "English", 4, 30000, 90, "High school diploma, SAT/ACT"),
        (7, "MSc in Artificial Intelligence", 7, "Computer Science", "Master", "English", 1, 35000, 80, "Bachelor in CS or related field"),
        (8, "Bachelor of Science in Medicine", 8, "Medicine", "Bachelor", "English", 6, 40000, 150, "High school diploma with strong science"),
        (9, "Master of Arts in Literature", 9, "Literature", "Master", "French", 2, 2000, 60, "Bachelor's degree, French proficiency"),
        (10, "MSc in Sustainable Development", 10, "Environmental Sciences", "Master", "English", 2, 16000, 100, "Bachelor's degree in related field"),
        (11, "Master of Engineering", 11, "Engineering", "Master", "English", 2, 35000, 90, "Bachelor in Engineering, GRE"),
        (12, "PhD in Robotics", 12, "Engineering", "PhD", "English/Japanese", 5, 8000, 0, "Master's degree, research proposal"),
        (13, "MSc in Sustainable Technology", 13, "Environmental Engineering", "Master", "English", 2, 0, 75, "Bachelor's degree, English proficiency"),
        (14, "Bachelor of Computer Science", 1, "Computer Science", "Bachelor", "English", 4, 45000, 75, "High school diploma, SAT/ACT"),
        (15, "Master of Public Health", 5, "Health Sciences", "Master", "English", 2, 28000, 110, "Bachelor's degree, GRE"),
        (16, "MSc in Finance", 7, "Finance", "Master", "English", 1, 38000, 95, "Bachelor's degree, GMAT"),
        (17, "Master in Machine Learning", 3, "Computer Science", "Master", "English", 2, 1500, 50, "Bachelor in CS or Mathematics"),
        (18, "MSc in Biomedical Engineering", 11, "Engineering", "Master", "English", 2, 32000, 80, "Bachelor in Engineering or Life Sciences"),
        (19, "PhD in Economics", 2, "Economics", "PhD", "English", 4, 0, 0, "Master's degree, research proposal"),
        (20, "Bachelor of Business Administration", 6, "Business", "Bachelor", "English", 3, 28000, 90, "High school diploma, personal statement")
    ]
    
    cursor.executemany('''
    INSERT OR REPLACE INTO programs (id, name_program, university_id, field, level, language, duration, tuition_per_year, application_fee, admission_requirements)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', programs)
    
    # Sample fields of study
    fields = [
        (1, "Computer Science", "STEM", 24.5, 72000),
        (2, "Business", "Business", 8.2, 65000),
        (3, "Engineering", "STEM", 12.8, 70000),
        (4, "Medicine", "Health Sciences", 15.6, 85000),
        (5, "Literature", "Humanities", 4.3, 48000),
        (6, "Physics", "STEM", 9.2, 68000),
        (7, "Environmental Sciences", "STEM", 11.4, 58000),
        (8, "Economics", "Social Sciences", 7.5, 67000),
        (9, "Health Sciences", "Health Sciences", 18.2, 72000),
        (10, "Finance", "Business", 10.2, 75000)
    ]
    
    cursor.executemany('''
    INSERT OR REPLACE INTO fields_of_study (id, name, category, employment_growth_rate, average_starting_salary)
    VALUES (?, ?, ?, ?, ?)
    ''', fields)
    
    conn.commit()
    conn.close()
    
    print("Sample data seeded successfully.")
    return True

def import_csv_data(db_path="studentDSS.db"):
    """Import data from CSV files if they exist."""
    data_dir = os.path.dirname(os.path.abspath(db_path))
    
    csv_files = {
        'countries.csv': 'countries',
        'cities.csv': 'cities',
        'universities.csv': 'universities',
        'programs.csv': 'programs',
        'fields_of_study.csv': 'fields_of_study'
    }
    
    conn = sqlite3.connect(db_path)
    
    for file_name, table_name in csv_files.items():
        file_path = os.path.join(data_dir, file_name)
        if os.path.exists(file_path):
            try:
                print(f"Importing data from {file_name}...")
                df = pd.read_csv(file_path)
                df.to_sql(table_name, conn, if_exists='append', index=False)
                print(f"Successfully imported data from {file_name}")
            except Exception as e:
                print(f"Error importing data from {file_name}: {e}")
    
    conn.close()

def main():
    """Main function to initialize the database."""
    # Get the path to the data directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "studentDSS.db")
    
    print("Database Initialization")
    print("=======================")
    print(f"Database will be created at: {db_path}")
    
    # Create the database schema
    if create_database(db_path):
        # Seed with sample data
        seed_sample_data(db_path)
        
        # Import from CSV if available
        import_csv_data(db_path)
        
        print("\nDatabase initialization complete!")
        print("You can now use this database with the Student DSS application.")
    else:
        print("\nDatabase initialization failed.")

if __name__ == "__main__":
    main()
