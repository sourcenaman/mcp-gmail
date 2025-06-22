# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install uv (for fast Python packaging and running)
RUN pip install --no-cache-dir uv

# Copy only dependency files first
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv pip install --system --requirement pyproject.toml || true

# Copy the rest of the project files
COPY . .

# Prevent uv from creating a virtual environment at runtime
ENV UV_VENV_CREATE=0

# Expose port (if your app runs a server, e.g., FastAPI/Flask)
EXPOSE 8000

# Set default command to run FastAPI with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
