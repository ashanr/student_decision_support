# Student Migration Data Integration

This document explains how student migration data is integrated into the Student Decision Support System (DSS) API.

## Overview

The Student DSS API now includes integration with historical student migration data (`student_migration_data.csv`) to enhance university program recommendations. This data contains information about past students, their preferences, choices, and outcomes, which helps provide more personalized and accurate recommendations.

## Key Benefits

- **Enhanced recommendations** based on patterns from successful student migrations
- **Similar student matching** to show what comparable students chose
- **Popularity indicators** for universities, countries, and fields based on student satisfaction
- **Data-driven insights** into factors that lead to successful educational outcomes

## How It Works

### Data Loading and Processing

The student data is loaded from `data/student_migration_data.csv` and processed by the `StudentDataAnalyzer` class. This involves:

1. Loading the CSV data
2. Processing and normalizing features
3. Building a nearest-neighbor model to find similar students
4. Analyzing patterns in student preferences and outcomes

### Recommendation Enhancement

The recommendation process now includes these additional steps:

1. **Basic filtering and scoring** occurs as before based on user preferences
2. **Similar student matching** identifies historical students with similar profiles
3. **Recommendation boosting** enhances scores for programs that were successful for similar students
4. **Explanation generation** includes insights from historical student data

## Using the Student Data Analyzer

You can use the `StudentDataAnalyzer` class in your own applications:

```python
from student_data_analyzer import StudentDataAnalyzer

# Initialize the analyzer
analyzer = StudentDataAnalyzer()

# Load and prepare data
analyzer.load_data()
analyzer.build_recommendation_model()

# Find similar students
preferences = {
    "field_of_study": "Computer Science",
    "gpa": 3.5,
    "max_tuition": 30000
}
similar_students = analyzer.find_similar_students(preferences)

# Enhance existing recommendations
enhanced_recommendations = analyzer.enhance_recommendations(
    original_recommendations, 
    preferences
)

# Get popularity boost for a specific option
boost_score = analyzer.get_popularity_boost(
    university_name="Technical University of Munich",
    country="Germany",
    field="Computer Science"
)
```

## Analyzing Student Data Patterns

The included `analyze_student_patterns.py` script can generate insights about student migration patterns:

```bash
python analyze_student_patterns.py
```

This will generate visualizations including:
- Popular destination countries
- University tier distribution
- Factors correlated with student satisfaction
- Popular fields of study
- Budget patterns

The generated charts are saved as PNG files in the current directory.

## Technical Implementation

The integration consists of these components:

1. **StudentDataAnalyzer class** (`student_data_analyzer.py`) - Core functionality for working with student data
2. **CourseSelectionAssistant integration** - Updated to leverage student data insights
3. **API endpoints** - New endpoint for similar students and enhanced recommendation endpoint
4. **Analysis script** (`analyze_student_patterns.py`) - For data exploration and visualization

## Data Fields Used

The most important student data fields used by the system include:

- `student_id` - Unique identifier for each student
- `field_of_study` - Academic discipline the student pursued
- `current_gpa` - Student's grade point average
- `tuition_budget` - Student's budget for tuition
- `living_expense_budget` - Student's budget for living expenses
- `final_destination_country` - Country where student ultimately enrolled
- `final_university_tier` - Tier/ranking level of chosen university
- `decision_satisfaction_score` - How satisfied the student was with their decision (1-10)

## Future Enhancements

Planned improvements for the student data integration:

1. Machine learning models to better predict student satisfaction
2. Clustering algorithms to identify student archetypes
3. Time-series analysis to identify changing trends in student preferences
4. More sophisticated visualization tools for exploring student outcomes
5. Personalized advice generation based on similar student experiences
