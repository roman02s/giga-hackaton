FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y \
    curl \
    &&  apt-get install gcc --only-upgrade \
    && apt-get install python3-pip \
    && rm -rf /var/lib/apt/lists/*


RUN pip install -r requirements.txt

EXPOSE 8080


HEALTHCHECK CMD curl --fail http://localhost:8080/health

COPY . /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

# docker build -t api-service .
# docker run -it -v "$(pwd):/app" -p 8000:8000 api-service bash
# docker run -d --restart=always -v "$(pwd)/data:/app/data" -v "$(pwd)/logs:/app/logs" -p 8000:8000 api-service
