# Student DSS API Documentation

This document provides comprehensive documentation for the Student Decision Support System (DSS) API.

## Overview

The Student DSS API is a REST API that helps students find suitable university programs based on their preferences, budget constraints, and academic goals. The API uses a sophisticated scoring algorithm to match student preferences with program data.

## Base URL

All API endpoints are relative to:

```
http://localhost:5000
```

For production deployments, replace with your domain.

## API Endpoints

### Health Check

Verify if the API service is running and can connect to the database.

#### Endpoint

```
GET /health
```

#### Response

- **Status**: 200 OK
- **Content-Type**: application/json

```json
{
  "status": "ok",
  "timestamp": "2024-01-28T15:30:45.123456",
  "service": "python-api",
  "database": "connected"
}
```

#### Error Response

- **Status**: 500 Internal Server Error
- **Content-Type**: application/json

```json
{
  "status": "error",
  "timestamp": "2024-01-28T15:30:45.123456",
  "service": "python-api",
  "error": "Error message details"
}
```

### Get Recommendations

Generates course recommendations based on user preferences using the advanced recommendation engine.

#### Endpoint

```
POST /api/python/recommendations
```

#### Request Headers

- **Content-Type**: application/json

#### Request Body

```json
{
  "field_of_study": "Computer Science",
  "degree_level": "Master",
  "max_tuition": 30000,
  "max_living_expenses": 1500,
  "preferred_countries": ["Germany", "Canada", "Netherlands"],
  "language_preference": "Any language with English programs"
}
```

##### Required Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| field_of_study | string | Field or discipline the student is interested in |
| degree_level | string | Academic level (Bachelor, Master, PhD) |

##### Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| max_tuition | number | Maximum annual tuition in USD | 50000 |
| max_living_expenses | number | Maximum monthly living expenses in USD | No limit |
| preferred_countries | array | List of preferred countries | [] |
| language_preference | string | One of: "English only", "Any language with English programs", "Open to learning a new language" | "Any language with English programs" |

#### Response

- **Status**: 200 OK
- **Content-Type**: application/json

```json
{
  "success": true,
  "recommendations": [
    {
      "id": 245,
      "name_program": "Master of Computer Science",
      "name_university": "Technical University of Munich",
      "country": "Germany",
      "city": "Munich",
      "tuition_per_year": 1500,
      "language": "English",
      "duration": 2,
      "field": "Computer Science",
      "level": "Master",
      "ranking_global": 50,
      "match_percentage": 95.2,
      "explanation": "Recommended because: Strong match with your academic interests; Fits well within your budget at $1,500/year; Well-ranked institution (#50 globally); Located in your preferred country (Germany)."
    },
    {
      "id": 189,
      "name_program": "MSc Computer Science",
      "name_university": "University of Toronto",
      "country": "Canada",
      "city": "Toronto",
      "tuition_per_year": 25000,
      "language": "English",
      "duration": 2,
      "field": "Computer Science",
      "level": "Master",
      "ranking_global": 25,
      "match_percentage": 92.8,
      "explanation": "Recommended because: Strong match with your academic interests; Well-ranked institution (#25 globally); Matches your language preferences; Located in your preferred country (Canada)."
    }
    // Additional recommendations...
  ]
}
```

#### Error Response

- **Status**: 400 Bad Request, 500 Internal Server Error
- **Content-Type**: application/json

```json
{
  "success": false,
  "error": "Error message details"
}
```

### Get Countries

Retrieves a list of all countries in the database.

#### Endpoint

```
GET /api/python/countries
```

#### Response

- **Status**: 200 OK
- **Content-Type**: application/json

```json
[
  {
    "id": 1,
    "name": "United States",
    "code": "US",
    "region": "North America",
    "average_living_cost": 1800,
    "average_tuition_cost": 35000,
    "language": "English",
    "safety_index": 70,
    "quality_of_life_index": 80
  },
  {
    "id": 2,
    "name": "Germany",
    "code": "DE",
    "region": "Europe",
    "average_living_cost": 1000,
    "average_tuition_cost": 1500,
    "language": "German",
    "safety_index": 80,
    "quality_of_life_index": 85
  }
  // Additional countries...
]
```

#### Error Response

- **Status**: 500 Internal Server Error
- **Content-Type**: application/json

```json
{
  "success": false,
  "error": "Error message details"
}
```

### Get Universities

Retrieves a list of universities with optional filtering.

#### Endpoint

```
GET /api/python/universities
```

#### Query Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| country | string | Filter by country name | None |
| limit | integer | Maximum number of results | 100 |
| offset | integer | Result offset for pagination | 0 |

#### Response

- **Status**: 200 OK
- **Content-Type**: application/json

```json
{
  "success": true,
  "count": 5,
  "universities": [
    {
      "id": 45,
      "name": "Technical University of Munich",
      "country": "Germany",
      "city": "Munich",
      "ranking_global": 50,
      "ranking_national": 2,
      "student_count": 40000,
      "established_year": 1868,
      "website": "https://www.tum.de/en/"
    },
    {
      "id": 46,
      "name": "Ludwig Maximilian University of Munich",
      "country": "Germany",
      "city": "Munich",
      "ranking_global": 32,
      "ranking_national": 1,
      "student_count": 50000,
      "established_year": 1472,
      "website": "https://www.lmu.de/en/"
    }
    // Additional universities...
  ]
}
```

#### Error Response

- **Status**: 500 Internal Server Error
- **Content-Type**: application/json

```json
{
  "success": false,
  "error": "Error message details"
}
```

## Student Data Integration

The API now includes integration with student migration data to enhance recommendations based on historical patterns and similar student preferences.

### Get Similar Students

Finds students with similar profiles and preferences to help inform decision making.

#### Endpoint

```
POST /api/python/similar-students
```

#### Request Headers

- **Content-Type**: application/json

#### Request Body

```json
{
  "field_of_study": "Computer Science",
  "gpa": 3.5,
  "max_tuition": 30000,
  "university_ranking_importance": 8,
  "cost_sensitivity": 7
}
```

#### Response

- **Status**: 200 OK
- **Content-Type**: application/json

```json
{
  "success": true,
  "similar_students": [
    {
      "id": 42,
      "field_of_study": "Computer Science",
      "gpa": 3.7,
      "final_destination": "Germany",
      "satisfaction_score": 9
    },
    {
      "id": 157,
      "field_of_study": "Data Science",
      "gpa": 3.4,
      "final_destination": "Netherlands",
      "satisfaction_score": 8
    }
    // Additional similar students...
  ]
}
```

#### Error Response

- **Status**: 404 Not Found, 500 Internal Server Error
- **Content-Type**: application/json

```json
{
  "success": false,
  "error": "Error message details"
}
```

### Enhanced Recommendations

The `/api/python/recommendations` endpoint now includes enhancements from student migration data analysis. The recommendations are improved by:

1. Finding similar student profiles from historical data
2. Identifying patterns in successful student migrations
3. Boosting recommendations based on destination popularity among similar students
4. Considering satisfaction scores of past students

No changes are needed to the API request format, but responses now include enhanced matching scores and additional context in the explanations.

## Error Codes and Troubleshooting

The API uses standard HTTP status codes:

- **200 OK**: Request succeeded
- **400 Bad Request**: Invalid input parameters
- **500 Internal Server Error**: Server-side error

Common issues and solutions:

1. **Database connection errors**: Ensure the database file is in the correct location (`data/studentDSS.db`).
2. **Invalid preferences**: Make sure to include all required parameters in the recommendations request.
3. **No recommendations**: If your search criteria are too restrictive, try relaxing some parameters.

## Database Connection Troubleshooting

If you encounter errors related to database connectivity (such as "failed to connect to database"), follow these steps:

1. **Verify database file exists**:
   - Check that the database file exists at `data/studentDSS.db` relative to the API root directory
   - If using a custom path, verify it matches the path specified in the API configuration

2. **Check file permissions**:
   - Ensure the user running the API service has read and write permissions to the database file
   - On Linux/macOS: `chmod 644 data/studentDSS.db`
   - On Windows: Right-click > Properties > Security > Edit > Add appropriate permissions

3. **Verify database structure**:
   - If you've created a new database, ensure it has the correct schema
   - You can initialize a new database using the setup script: `python scripts/init_db.py`

4. **Check for concurrent access issues**:
   - SQLite databases may have locking issues if multiple processes try to write simultaneously
   - Ensure no other process has an exclusive lock on the database file

5. **Database path configuration**:
   - If you've moved the database file, update the configuration in `config.py` or set the environment variable:
   ```bash
   # Linux/macOS
   export DB_PATH=/path/to/studentDSS.db
   
   # Windows
   set DB_PATH=C:\path\to\studentDSS.db
   ```

6. **Restart API service**:
   - After making any changes, restart the API service to ensure they take effect

If the error persists after trying these steps, check the API logs for more detailed error messages or contact support.

## Rate Limiting

The API currently does not implement rate limiting. In production environments, consider adding appropriate rate limiting to prevent abuse.

## Versioning

This documentation describes API v1. Future versions will be made available under different endpoints.

## Examples

### cURL Examples

#### Health Check
```bash
curl -X GET http://localhost:5000/health
```

#### Get Recommendations
```bash
curl -X POST \
  http://localhost:5000/api/python/recommendations \
  -H 'Content-Type: application/json' \
  -d '{
    "field_of_study": "Computer Science",
    "degree_level": "Master",
    "max_tuition": 30000,
    "preferred_countries": ["Germany", "Canada"],
    "language_preference": "Any language with English programs"
  }'
```

#### Get Countries
```bash
curl -X GET http://localhost:5000/api/python/countries
```

#### Get Universities
```bash
curl -X GET 'http://localhost:5000/api/python/universities?country=Germany&limit=5'
```

#### Get Similar Students
```bash
curl -X POST \
  http://localhost:5000/api/python/similar-students \
  -H 'Content-Type: application/json' \
  -d '{
    "field_of_study": "Computer Science",
    "gpa": 3.5,
    "max_tuition": 30000
  }'
```

## Postman Usage Guide

### Importing cURL Requests to Postman

You can easily import any of the cURL commands below into Postman:

1. Copy the cURL command
2. In Postman, click "Import" > "Raw text" 
3. Paste the cURL command
4. Click "Import"

### Ready-to-Use cURL Commands for Postman

#### Health Check
```bash
curl --location --request GET 'http://localhost:5000/health'
```

#### Get All Countries
```bash
curl --location --request GET 'http://localhost:5000/api/python/countries'
```

#### Get Universities (All)
```bash
curl --location --request GET 'http://localhost:5000/api/python/universities'
```

#### Get Universities (Filtered by Country)
```bash
curl --location --request GET 'http://localhost:5000/api/python/universities?country=Germany&limit=10&offset=0'
```

#### Get University Programs Recommendations
```bash
curl --location --request POST 'http://localhost:5000/api/python/recommendations' \
--header 'Content-Type: application/json' \
--data-raw '{
    "field_of_study": "Computer Science",
    "degree_level": "Master",
    "max_tuition": 30000,
    "max_living_expenses": 1500,
    "preferred_countries": ["Germany", "Canada", "Netherlands"],
    "language_preference": "Any language with English programs"
}'
```

#### Get Recommendations (Business Field)
```bash
curl --location --request POST 'http://localhost:5000/api/python/recommendations' \
--header 'Content-Type: application/json' \
--data-raw '{
    "field_of_study": "Business Administration",
    "degree_level": "Bachelor",
    "max_tuition": 25000,
    "preferred_countries": ["United States", "United Kingdom", "Australia"],
    "language_preference": "English only"
}'
```

#### Get Recommendations (Engineering Field)
```bash
curl --location --request POST 'http://localhost:5000/api/python/recommendations' \
--header 'Content-Type: application/json' \
--data-raw '{
    "field_of_study": "Mechanical Engineering",
    "degree_level": "Master",
    "max_tuition": 35000,
    "max_living_expenses": 1200,
    "preferred_countries": ["Germany", "Sweden", "Switzerland"],
    "language_preference": "Any language with English programs"
}'
```

#### Get Similar Students
```bash
curl --location --request POST 'http://localhost:5000/api/python/similar-students' \
--header 'Content-Type: application/json' \
--data-raw '{
    "field_of_study": "Computer Science",
    "gpa": 3.5,
    "max_tuition": 30000
}'
```

### Postman Collection

You can also download a complete Postman Collection file containing all these requests from the repository at: 
`examples/student_dss_api.postman_collection.json`

### Python Example

```python
import requests
import json

# Define the API endpoint
url = "http://localhost:5000/api/python/recommendations"

# Prepare the request payload
payload = {
    "field_of_study": "Computer Science",
    "degree_level": "Master",
    "max_tuition": 30000,
    "preferred_countries": ["Germany", "Canada"],
    "language_preference": "Any language with English programs"
}

# Send the POST request
response = requests.post(url, json=payload)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    
    # Print the recommendations
    for i, recommendation in enumerate(data['recommendations'], 1):
        print(f"{i}. {recommendation['name_program']} at {recommendation['name_university']}")
        print(f"   Match: {recommendation['match_percentage']}%")
        print(f"   {recommendation['explanation']}")
        print()
else:
    print(f"Error: {response.status_code}")
    print(response.text)

# Get similar students
url = "http://localhost:5000/api/python/similar-students"
payload = {
    "field_of_study": "Computer Science",
    "gpa": 3.5,
    "max_tuition": 30000
}
response = requests.post(url, json=payload)
similar_students = response.json()

print("Similar students from historical data:")
for student in similar_students['similar_students']:
    print(f"- {student['field_of_study']} student with GPA {student['gpa']} chose {student['final_destination']}")
    print(f"  Satisfaction score: {student['satisfaction_score']}/10")

# Get enhanced recommendations
response = requests.post(url, json=payload)
recommendations = response.json()

print("\nEnhanced program recommendations:")
for rec in recommendations['recommendations'][:3]:
    print(f"- {rec['name_program']} at {rec['name_university']} ({rec['match_percentage']}% match)")
    print(f"  {rec['explanation']}")
```

## Support

For questions, issues, or feature requests, please open an issue on the GitHub repository or contact the development team.
