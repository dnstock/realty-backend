# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements file first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy only necessary application files
COPY ./app /app/app

# Create a non-root user and switch to it
RUN useradd -m appuser
USER appuser

# Set environments
ENV ENVIRONMENT=production
ENV APP_IS_DOCKED=true

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Set the entrypoint to a script that handles environment-based commands
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
