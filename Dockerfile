# Use an official Python runtime as a parent image
FROM puckel/docker-airflow:latest

#USER
USER airflow

# Set the working directory to /app
WORKDIR /usr/local/airflow/app

# Copy the current directory contents into the container at /app
ADD --chown=airflow:airflow . /usr/local/airflow/app

# Changing working directory to /app
WORKDIR /usr/local/airflow/app

# Install any needed packages specified in requirements.txt
RUN pip install ./src/dist/BranceAuto-0.1-py3-none-any.whl





