# Use an official Python runtime as a parent image
FROM python:3.7.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the Pipfile and Pipfile.lock into the container
COPY Pipfile Pipfile.lock ./

# Install pipenv
RUN pip install pipenv

# Install dependencies
RUN pipenv install --deploy --ignore-pipfile

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Expose port 8000 for the Django app
EXPOSE 8000

# Run the application
CMD ["pipenv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "EasyStocks.wsgi:application"]