# Use an official Python runtime as a parent image
FROM python:3.12-slim

RUN apt-get update && apt-get install -y lsb-release
RUN apt-get -y update; apt-get -y install curl
RUN curl -fsSLo /usr/share/keyrings/docker-archive-keyring.asc \
  https://download.docker.com/linux/debian/gpg
RUN echo "deb [arch=$(dpkg --print-architecture) \
  signed-by=/usr/share/keyrings/docker-archive-keyring.asc] \
  https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list
RUN apt-get update && apt-get install -y docker-ce-cli

# Set the working directory in the container
WORKDIR /usr/src/app

# Define environment variable
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5050

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt, or list them explicitly
RUN pip install -r requirements.txt 

# Run app.py when the container launches
CMD ["flask", "run"]