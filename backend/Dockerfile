# backend/Dockerfile
FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir /app
COPY . /app

# Set work directory
WORKDIR /app/backend

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8200

#ENTRYPOINT ["bash", "entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8200"]