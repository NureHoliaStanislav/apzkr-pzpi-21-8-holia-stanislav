FROM python:3.7-buster
# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install postgresql-client
RUN apt-get update && apt-get install -y postgresql-client

# Install postgis
RUN apt-get update && apt-get install -y postgis

# Install GDAL library
RUN apt-get update && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin \
    libgdal-dev

# Set GDAL library path
ENV GDAL_LIBRARY_PATH=/usr/lib/libgdal.so


# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install djangorestframework-gis
RUN pip install PyJWT
RUN pip install django-cors-headers

# Bundle app source
COPY . .

# Change permissions of the django.sh script to make it executable
RUN chmod +x /app/django.sh

# Expose port
EXPOSE 8000

# entrypoint to run the django.sh file
ENTRYPOINT ["/app/django.sh"]


