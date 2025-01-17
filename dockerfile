# Use an official Python runtime as a base image
FROM python:3.10-slim

# Copy the current directory contents into the container
COPY app /app

# Expose the port your server listens on
EXPOSE 8080

# Define the command to run your application
# CMD ["python", "solution.py"]
CMD ["python", "app/solution.py"]
