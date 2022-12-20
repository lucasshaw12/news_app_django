# Pull base image
FROM python:3.8

EXPOSE 80
EXPOSE 8080
EXPOSE 8081

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY Pipfile Pipfile.lock /code/
COPY requirements.txt /usr/src/requirements.txt
RUN pip install pipenv && pipenv install --system

# Copy project
COPY . /code/


CMD ["python", "/code/manage.py", "runserver", "0.0.0.0:8000"]
FROM lucasshaw12/news-web:latest