# 1. Use a lightweight Python image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy only the requirements first (optimizes build caching)
# If you don't have a requirements.txt yet, see the note below.
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your application code
COPY . .

# 6. Expose the port Flask is running on
EXPOSE 5005

# Use Gunicorn to serve the app safely
CMD ["gunicorn", "--bind", "0.0.0.0:5005", "--workers", "4", "app.main:app"]