# api/Dockerfile
FROM python:3.11-slim

WORKDIR /api

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the api directory contents
COPY ./api .

EXPOSE 8000

# Updated command to correctly reference the app instance
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]