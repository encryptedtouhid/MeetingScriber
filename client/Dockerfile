FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy client code
COPY . .

# Expose client web interface port
EXPOSE 3000

CMD ["python", "-u", "main.py"]