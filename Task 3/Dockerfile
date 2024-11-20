# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install any dependencies
# --no-cache-dir used to prevent pip from caching the downloaded packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI project files into the container
# first dot refers to the current directory on your host machine
# second dot refers to the working directory inside the container
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# Define the command to run the application
# first app refers to the app.py file in my current directory
# second app refers to the name of the initialize of my FastAPI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]