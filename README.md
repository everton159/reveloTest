# Actuate SDET Exercise

## Overview
This project implements an HTTP server to handle URL shortening and retrieval, along with automated tests for functionality and edge cases.

### Features
- Shorten a long URL into a unique short URL.
- Retrieve the original URL from a shortened URL.
- Redirect from a shortened URL to the original URL.
- Basic logging for all requests.

## Requirements
- Python 3.8+
- Flask
- pytest
- requests

## Setup

### Install Dependencies
1. Create a virtual environment:
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```
2. Install the required libraries from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

### Run the Server
1. Start the server:
   ```bash
   python server.py
   ```
2. The server will be available at `http://127.0.0.1:5000/`.

## Endpoints

### 1. Shorten a URL
**POST** `/shorten`
- **Input**:
  ```json
  {
      "url": "https://www.google.com"
  }
  ```
- **Curl Command**:
  ```bash
  curl -X POST http://127.0.0.1:5000/shorten -H "Content-Type: application/json" -d '{"url": "https://www.google.com"}'
  ```
- **Output**:
  ```json
  {
      "short_url": "abc12345"
  }
  ```

### 2. Retrieve the Original URL
**GET** `/retrieve/<short_url>`
- **Curl Command**:
  ```bash
  curl -X GET http://127.0.0.1:5000/retrieve/abc12345
  ```
- **Output**:
  ```json
  {
      "long_url": "https://www.google.com"
  }
  ```

### 3. Redirect to Original URL
**GET** `/<short_url>`
- **Curl Command**:
  ```bash
  curl -X GET http://127.0.0.1:5000/abc12345 -i
  ```


## Testing

### Run Tests
1. Start the server as described above.
2. Run the tests:
```
bash
pytest --html=report.html --cov=server --cov-report=html   
```

3. It will generate a  report.html file

### Test Cases
- Valid URL shortening and retrieval.
- Invalid inputs.
- Redirection validation.
- Thread safety with concurrent requests (basic simulation).

## Design Notes
- **In-Memory Storage**: There is not a database, only a dictionary

