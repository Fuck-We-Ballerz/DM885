FROM node:latest
WORKDIR /app

COPY . .

# Use a build argument to specify the environment (default to 'dev')
ARG ENVIRONMENT=dev

# Copy the appropriate environment file based on the value of ENVIRONMENT
RUN if [ "$ENVIRONMENT" = "dev" ]; then \
        cp /app/.env.dev /app/config.env; \
    else \
        cp /app/.env.prod /app/config.env; \
    fi

RUN npm install

ENTRYPOINT [ "npm", "run", "dev", "--", "--host", "0.0.0.0" ]