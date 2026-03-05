# Dockerfile
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy dependency files first (layer caching)
COPY requirements.txt pyproject.toml ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the project
COPY . .

# Install project as editable package
RUN pip install -e .

# Run the ETL pipeline first, then start Flask
CMD ["sh", "-c", "python run_pipeline.py && python app.py"]
