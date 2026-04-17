# Concept 4: Containerization
# This Dockerfile packages the entire ML Pipeline and API into an isolated, reproducible container
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies first (caches this heavy step)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Inform Docker that our API talks over port 8000
EXPOSE 8000

# Specify exactly what command Docker should run when the container turns on
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
