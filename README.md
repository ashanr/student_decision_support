# Student Decision Support System (DSS) API

A data-driven recommendation system for helping students find optimal university courses based on their preferences, budget constraints, and academic goals.

## Project Overview

The Student DSS is designed to simplify the process of finding suitable university programs globally. It matches student preferences with program data using a sophisticated scoring algorithm that considers multiple factors:

- Academic fit
- Tuition costs
- Living expenses
- University rankings
- Career prospects
- Geographic preferences
- Language requirements

## Installation

### Prerequisites

- Python 3.9+
- SQLite3
- Git

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/student-dss.git
   cd student-dss
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```bash
   python data/initialize_database.py
   ```

5. Make sure the database file is located at `data/studentDSS.db` relative to the project root

## Database Structure

The system uses an SQLite database (`data/studentDSS.db`) with the following tables:

- **countries**: Information about countries including living costs and quality metrics
- **cities**: City-level data with population and cost of living
- **universities**: University details including rankings and locations
- **programs**: Academic program information with tuition and admission requirements
- **fields_of_study**: Information about academic disciplines and career prospects

Additionally, the system leverages student migration data from `data/student_migration_data.csv` to enhance recommendations based on patterns from previous student decisions.

## Running the API

Start the API server with:

```bash
# Using Docker
docker-compose up

# Or directly with Python
python app.py
```

The API will be available at `http://localhost:5000`

## Docker Configuration

The project includes Docker support for easy deployment and consistent environments.

### Docker Setup

1. Make sure you have Docker and Docker Compose installed on your system
2. Build and start the containers:
   ```bash
   docker-compose build
   docker-compose up
   ```
   
3. To run in detached mode:
   ```bash
   docker-compose up -d
   ```

4. To stop the containers:
   ```bash
   docker-compose down
   ```

### Docker Environment Variables

The following environment variables can be configured in the `.env` file:

- `DB_PATH`: Path to the SQLite database (default: `./data/studentDSS.db`)
- `API_PORT`: Port for the API server (default: `5000`)
- `DEBUG_MODE`: Enable debug mode (default: `false`)

## Base URL

All endpoints are relative to: `http://localhost:5000`

## Endpoints

### Health Check

Verify if the API service is running and can connect to the database.

- **URL**: `/health`
- **Method**: `GET`

**cURL Example:**

```bash
curl -X GET http://localhost:5000/health
```

**Response Example:**

```json
{
  "status": "ok",
  "timestamp": "2024-01-28T15:30:45.123456",
  "service": "python-api",
  "database": "connected"
}
```

### Get Recommendations

Generates course recommendations based on user preferences using the advanced recommendation engine.

- **URL**: `/api/python/recommendations`
- **Method**: `POST`
- **Content-Type**: `application/json`

**Request Body:**

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

**Required Fields:**
- `field_of_study`: Field or discipline the student is interested in
- `degree_level`: Academic level (Bachelor, Master, PhD)

**Optional Fields:**
- `max_tuition`: Maximum annual tuition in USD
- `max_living_expenses`: Maximum monthly living expenses in USD
- `preferred_countries`: List of preferred countries
- `language_preference`: One of: "English only", "Any language with English programs", "Open to learning a new language"

**cURL Example:**

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

**Response Example:**

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

### Get Countries

Retrieves a list of all countries in the database.

- **URL**: `/api/python/countries`
- **Method**: `GET`

**cURL Example:**

```bash
curl -X GET http://localhost:5000/api/python/countries
```

**Response Example:**

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

### Get Universities

Retrieves a list of universities with optional filtering.

- **URL**: `/api/python/universities`
- **Method**: `GET`
- **Query Parameters**:
  - `country` (optional): Filter by country name
  - `limit` (optional): Maximum number of results (default: 100)
  - `offset` (optional): Result offset for pagination (default: 0)

**cURL Example:**

```bash
curl -X GET 'http://localhost:5000/api/python/universities?country=Germany&limit=5'
```

**Response Example:**

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

## Architecture

The Student DSS API is built using the following components:

- **Flask**: Lightweight web framework for API endpoints
- **SQLite**: Database for storing university and program information
- **Pandas/NumPy**: Data processing and recommendation algorithms
- **Matplotlib**: Visualization for recommendation results

## Development

### Project Structure

```
student-dss/
│
├── api/                    # API implementation
│   ├── python/             # Python API
│   │   ├── app.py          # Main application file
│   │   ├── requirements.txt # Python dependencies
│   │   └── ...             # Additional Python modules
│   │
│   └── ...                 # Other language APIs (e.g., Node.js, Java)
│
├── data/                   # Data files
│   ├── studentDSS.db       # SQLite database
│   └── ...                 # Other data files
│
├── docker-compose.yml       # Docker Compose configuration
└── README.md               # Project documentation
```

### Testing

- Unit tests are located in the `tests/` directory
- To run tests, execute:
  ```bash
  pytest tests/
  ```

### Improvement Plan

Future improvements to the Student DSS API may include:

- Expanding the database with more universities and programs
- Enhancing the recommendation algorithm with machine learning
- Adding user authentication and profile management
- Supporting additional languages and currencies
- Providing a web-based user interface

Contributions are welcome! Please submit a pull request or open an issue for discussion.
