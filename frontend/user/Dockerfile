# Use an official Python runtime as a parent image
FROM python:3.12-slim

RUN apt-get update && apt-get install -y lsb-release
RUN curl -fsSLo /usr/share/keyrings/docker-archive-keyring.asc \
    https://download.docker.com/linux/debian/gpg
RUN echo "deb [arch=$(dpkg --print-architecture) \
    signed-by=/usr/share/keyrings/docker-archive-keyring.asc] \
    https://download.docker.com/linux/debian \
    $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list

# Set the working directory in the container
WORKDIR /usr/src/app

COPY . .

ARG ENVIRONMENT=dev

# Run the command to move config.env to .env
RUN if [ "$ENVIRONMENT" = "dev" ]; then \
        cat config.env > .env; \
    else \
        cat config-prod.env > .env; \
    fi
    

# Define environment variable
ENV SCRIPT_NAME=/student

# Install any needed packages specified in requirements.txt, or list them explicitly
RUN pip install -r requirements.txt 

# Run app.py when the container launches
CMD ["gunicorn", "-b" ,":5050", "app:app"]