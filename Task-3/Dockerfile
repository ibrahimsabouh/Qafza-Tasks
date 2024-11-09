# Specifies the base Docker image to use for the container.
# The slim variant of the Python image more lightweight version.
FROM python:3.10-slim

# Sets the working directory inside the container to /app.
WORKDIR /app

# Copies the requirements.txt file, which contains the list of Python dependencies
# for the FastAPI application into the working directory of the container.
COPY requirements.txt .

# Installs the Python dependencies listed in the requirements.txt file using the pip install command.
# --no-cache-dir used to avoid caching the downloaded packages, which can help reduce the overall image size.
RUN pip install --no-cache-dir -r requirements.txt

# Copies the entire FastAPI project directory into the working directory of the container.
COPY . .

# Specifies that the container will listen on port 8000, 
# which is the default port used by the FastAPI application.
EXPOSE 8000

# Sets the command that will be executed when the container starts.
# It runs the FastAPI application using the uvicorn server.
# The IP addresses (--host "0.0.0.0") and the port 8000 (--port "8000").
# The app:app refers to the FastAPI application instance, and my main application
# file is named app.py and the application instance is also named app.
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]