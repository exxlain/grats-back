# Grats Backend

Backend service built with **FastAPI**, designed to generate greeting images using an AI neural network packaged in Docker.

## 🚀 Features
- FastAPI backend server
- REST API to communicate with AI image-generation container
- Docker Compose setup for easy development and deployment

## ⚙️ Tech Stack
- **FastAPI** (Python)
- **Docker** & **Docker Compose**

## 📂 Project Structure

```
grats-back/
├── app/
│   ├── main.py      # API endpoints
│   └── schemas.py   # Request and response schemas
├── Dockerfile       # Dockerfile for FastAPI app
├── docker-compose.yml # Docker Compose configuration
└── requirements.txt # Python dependencies
```

## ▶️ Running the project

### Local Development

Activate the virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run FastAPI backend locally:

```bash
uvicorn app.main:app --reload
```

Access Swagger documentation at:

- [http://localhost:8000/docs](http://localhost:8000/docs)

### Make commands:
Builds the Docker image
```bash
make build
```
Automatically builds and starts the container
```bash
make run
```
Stops and removes the running container
```bash
make stop
```
Stops the container (if running) and starts it again.
```bash
make restart
```

### Docker Compose

To run backend with neural network container:

```bash
docker-compose up --build
```

## 📚 API Documentation

API endpoints are auto-documented with Swagger at:
- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Redoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 📦 Technologies
- **FastAPI** for REST API
- **Docker Compose** for service orchestration

© 2025 Grats Back. All rights reserved.
