# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory to /app
WORKDIR /app 

# Copy the current directory contents into the container at /app
COPY ./ /app

RUN mkdir staticfiles
RUN apt-get update && apt-get install -f -y postgresql-client
RUN apt-get install wget -y
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb && apt install -y -f ./wkhtmltox_0.12.6-1.buster_amd64.deb

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pytest --cov --cov-report=html:reports/coverage

# Expose port 8000 for the Django app
EXPOSE 8000

# Define environment variable for Python
ENV PYTHONUNBUFFERED 1

# Run Django production server
CMD ["./run.sh"]
