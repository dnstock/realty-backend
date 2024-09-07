# Build the image with a different environment:
#    docker build --build-arg ENVIRONMENT=production -t realty-backend .

# Run the container with a different environment:
#    docker run -e ENVIRONMENT=production -p 8000:8000 realty-backend

# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install gcc and other necessary packages
RUN apt-get update && apt-get install -y gcc python3-dev

# Copy the requirements file into the container
COPY requirements.txt .

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Set the environment variable for the environment (e.g., development)
ENV ENVIRONMENT=development

# Set an environment variable for the Docker container
ENV APP_IS_DOCKED=true

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
