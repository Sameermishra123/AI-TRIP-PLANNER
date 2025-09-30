FROM python:3.10-slim

WORKDIR /app

# Copy dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Make start.sh executable
RUN chmod +x start.sh

EXPOSE 8000 8501

CMD ["sh", "start.sh"]
