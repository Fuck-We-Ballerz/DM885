# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Define environment variable
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5050

# Install any needed packages specified in requirements.txt, or list them explicitly
RUN pip install -r requirements.txt 

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Run app.py when the container launches
CMD ["flask", "run"]