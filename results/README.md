# Decision Support Results

This directory contains sample and generated results from the Student Decision Support System.

## Directory Contents

- **Sample Results:** Pre-generated examples of what the system produces
  - `sample_recommendations.json`: Example of JSON recommendations data
  - `decision_support_report.md`: Example of a formatted decision report

- **Generated Results:** Created when you run the system (will be created automatically)
  - `program_recommendations.png`: Visualization of program matches
  - `destination_popularity.png`: Analysis of popular destination countries
  - `university_tiers.png`: Distribution of university tiers
  - `field_popularity.png`: Analysis of popular fields of study
  - `budget_patterns.png`: Analysis of budget patterns
  - `satisfaction_correlations.png`: Heatmap of satisfaction correlations

## How to Generate Results

Run the following scripts to generate actual results:

```bash
# Generate program recommendations
python course_selection_assistant.py

# Generate data analysis visualizations
python analyze_student_patterns.py
```

The generated files will be placed in this directory, replacing any existing files with the same names.

## Using These Results

The results in this directory can be used for:

1. **Decision Making:** Review recommendations to help choose university programs
2. **Data Analysis:** Understand patterns in student migration and preferences
3. **Presentation:** Share findings with academic advisors or other stakeholders
4. **Testing:** Verify that the system is working correctly

## File Formats

- `.json`: Raw data in JSON format
- `.md`: Formatted reports in Markdown format
- `.png`: Visualization images
- `.html`: Interactive web reports (if generated with the web option)
