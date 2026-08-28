FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --default-timeout=1000 -r requirements.txt
COPY . .
EXPOSE 8000 8501