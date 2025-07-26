#!/usr/bin/env python3
"""
Student Migration Data Pattern Analyzer

This script analyzes patterns in student migration data to identify
trends and insights that can improve the recommendation system.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_student_data(file_path=None):
    """Load student migration data from CSV file."""
    if file_path is None:
        # Corrected path to reference data in the same package
        file_path = os.path.join(os.path.dirname(__file__), 
                              "data", "student_migration_data.csv")
    
    try:
        data = pd.read_csv(file_path)
        print(f"Loaded {len(data)} student records")
        return data
    except Exception as e:
        print(f"Error loading student data: {e}")
        return None

def analyze_destination_popularity(data):
    """Analyze which countries are most popular as destinations."""
    if 'final_destination_country' not in data.columns:
        print("No destination country data available")
        return
    
    # Get destination counts, excluding missing values
    destinations = data['final_destination_country'].dropna()
    destination_counts = destinations.value_counts()
    
    print("\n=== POPULAR DESTINATION COUNTRIES ===")
    print(destination_counts.head(10))
    
    # Create bar chart
    plt.figure(figsize=(12, 6))
    destination_counts.head(10).plot(kind='bar', color='skyblue')
    plt.title('Top 10 Destination Countries')
    plt.xlabel('Country')
    plt.ylabel('Number of Students')
    plt.tight_layout()
    plt.savefig('destination_popularity.png')
    print("Chart saved as 'destination_popularity.png'")

def analyze_university_tiers(data):
    """Analyze the distribution of university tiers chosen by students."""
    if 'final_university_tier' not in data.columns:
        print("No university tier data available")
        return
    
    # Get tier distribution
    tiers = data['final_university_tier'].dropna()
    tier_counts = tiers.value_counts()
    
    print("\n=== UNIVERSITY TIER DISTRIBUTION ===")
    print(tier_counts)
    
    # Create pie chart
    plt.figure(figsize=(10, 8))
    plt.pie(tier_counts, labels=tier_counts.index, autopct='%1.1f%%', 
            startangle=90, shadow=True)
    plt.title('University Tier Distribution')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    plt.tight_layout()
    plt.savefig('university_tiers.png')
    print("Chart saved as 'university_tiers.png'")

def analyze_satisfaction_factors(data):
    """Analyze factors that correlate with high decision satisfaction."""
    if 'decision_satisfaction_score' not in data.columns:
        print("No satisfaction score data available")
        return
    
    # Factors that might influence satisfaction
    potential_factors = [
        'university_ranking_importance', 'cost_sensitivity_score',
        'safety_importance_score', 'career_importance_score',
        'confidence_level_score', 'risk_tolerance_score'
    ]
    
    # Filter to factors that exist in the data
    factors = [f for f in potential_factors if f in data.columns]
    
    if not factors:
        print("No relevant satisfaction factors found in data")
        return
    
    print("\n=== SATISFACTION CORRELATION ANALYSIS ===")
    
    # Calculate correlations
    correlations = {}
    for factor in factors:
        corr = data[factor].corr(data['decision_satisfaction_score'])
        correlations[factor] = corr
        print(f"{factor}: correlation with satisfaction = {corr:.3f}")
    
    # Create correlation heatmap
    plt.figure(figsize=(10, 8))
    corr_data = data[factors + ['decision_satisfaction_score']].corr()
    sns.heatmap(corr_data, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Correlation between Factors and Decision Satisfaction')
    plt.tight_layout()
    plt.savefig('satisfaction_correlations.png')
    print("Chart saved as 'satisfaction_correlations.png'")

def analyze_field_popularity(data):
    """Analyze which fields of study are most popular."""
    if 'field_of_study' not in data.columns:
        print("No field of study data available")
        return
    
    # Get field counts
    field_counts = data['field_of_study'].value_counts()
    
    print("\n=== POPULAR FIELDS OF STUDY ===")
    print(field_counts.head(10))
    
    # Create horizontal bar chart
    plt.figure(figsize=(12, 8))
    field_counts.head(10).plot(kind='barh', color='lightgreen')
    plt.title('Top 10 Fields of Study')
    plt.xlabel('Number of Students')
    plt.ylabel('Field')
    plt.tight_layout()
    plt.savefig('field_popularity.png')
    print("Chart saved as 'field_popularity.png'")

def analyze_budget_patterns(data):
    """Analyze patterns in student budgets and their choices."""
    budget_columns = ['tuition_budget', 'living_expense_budget']
    
    # Check if budget data is available
    if not all(col in data.columns for col in budget_columns):
        print("Budget data not available")
        return
    
    print("\n=== BUDGET ANALYSIS ===")
    
    # Calculate basic statistics
    for col in budget_columns:
        print(f"\n{col} statistics:")
        print(data[col].describe())
    
    # Create scatter plot of tuition vs living budget
    plt.figure(figsize=(10, 8))
    plt.scatter(data['tuition_budget'], data['living_expense_budget'], 
                alpha=0.5, c=data['decision_satisfaction_score'] if 'decision_satisfaction_score' in data.columns else 'blue')
    
    plt.title('Tuition Budget vs Living Expense Budget')
    plt.xlabel('Tuition Budget (USD)')
    plt.ylabel('Living Expense Budget (USD)')
    plt.colorbar(label='Satisfaction Score' if 'decision_satisfaction_score' in data.columns else None)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('budget_patterns.png')
    print("Chart saved as 'budget_patterns.png'")

def main():
    """Main function to run all analyses."""
    print("=== STUDENT MIGRATION DATA ANALYSIS ===")
    
    # Load data
    data = load_student_data()
    if data is None:
        return
    
    # Perform analyses
    analyze_destination_popularity(data)
    analyze_university_tiers(data)
    analyze_satisfaction_factors(data)
    analyze_field_popularity(data)
    analyze_budget_patterns(data)
    
    print("\nAnalysis complete!")

if __name__ == "__main__":
    main()
