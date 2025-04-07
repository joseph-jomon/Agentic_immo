# syntax=docker/dockerfile:1

# Base image with an argument for Python version
ARG PYTHON_VERSION=3.11-slim
FROM python:${PYTHON_VERSION} as base

# Optimize Python behavior in Docker
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Working directory for the app
WORKDIR /realtime_vector_app

# Create a non-privileged user for security
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/home/appuser" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Create necessary directories with correct permissions
RUN mkdir -p /realtime_vector_app/logs && chown -R appuser:appuser /realtime_vector_app

# Copy requirements file first for dependency caching
COPY requirements.txt /realtime_vector_app/

# Install dependencies with cache optimizations
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . /realtime_vector_app/

# Switch to the non-privileged user
USER appuser

# Expose the port that FastAPI will run on
EXPOSE 8000

# Start the FastAPI app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
