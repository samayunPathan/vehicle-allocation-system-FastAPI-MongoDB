# Vehicle Allocation System
A FastAPI-based REST API system for managing vehicle allocations in a company. This system allows employees to allocate vehicles for specific dates, with features to manage and track allocations efficiently.
## Features

- Create, update, and delete vehicle allocations
- Prevent double booking of vehicles
- Comprehensive allocation history with filtering options
- Optimized database queries with indexes
- RESTful API with Swagger documentation
- Future date validation for allocations
- Pagination support for listing allocations

## Prerequisites
```
Python 3.8 or higher
MongoDB 4.0 or higher

```
## Project Structure
```
vehicle_allocation/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py
│   └── routes/
│       ├── __init__.py
│       └── allocation.py
│
├── requirements.txt
└── README.md
```
## Installation

#### Clone the repository (or create the directory structure manually):

```bash
mkdir vehicle_allocation
cd vehicle_allocation
```

#### Create a virtual environment:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

#### Install the dependencies:

```bash
pip install -r requirements.txt
```

#### Database Setup

Install MongoDB if you haven't already
and configure config.py your system credentials
```
MONGODB_URL = Your mongodb_url
DATABASE_NAME = data name
```

## Start the FastAPI application:

```bash
uvicorn app.main:app --reload
```

The application will be available at:

```
API: http://localhost:8000
Swagger Documentation: http://localhost:8000/docs
```
## API Endpoints
#### Allocations
```bash
POST /api/v1/allocations/ - Create a new allocation
PATCH /api/v1/allocations/{allocation_id} - Update an existing allocation
DELETE /api/v1/allocations/{allocation_id} - Delete an allocation
GET /api/v1/allocations/ - Get allocation history with filters
```
#### API Documentation
Visit http://localhost:8000/docs for detailed Swagger documentation of all endpoints.



#### The API uses standard HTTP status codes:
```
200: Successful operation
400: Bad request (e.g., invalid dates, double booking)
404: Resource not found
500: Server error
```

