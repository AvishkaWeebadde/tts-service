FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Expose the Flask app's port
EXPOSE 5000

CMD ["python", "tts-service.py"]
