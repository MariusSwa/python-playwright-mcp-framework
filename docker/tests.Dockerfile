FROM mcr.microsoft.com/playwright/python:v1.52.0-noble

WORKDIR /app

RUN apt-get update && apt-get install -y nodejs npm && rm -rf /var/lib/apt/lists/*

COPY automation/requirements.txt automation/requirements.txt

RUN pip install --no-cache-dir -r automation/requirements.txt

COPY . .

WORKDIR /app/automation

CMD ["pytest"]