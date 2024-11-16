FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose the Flask app's port
EXPOSE 5000

COPY . .

CMD ["python", "tts_service.py"]