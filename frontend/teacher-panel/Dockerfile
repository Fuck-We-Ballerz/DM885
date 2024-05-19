FROM node:latest
WORKDIR /app

ENV PORT=5173

COPY . .

ARG ENVIRONMENT=dev

# Copy the appropriate environment file based on the value of ENVIRONMENT
RUN if [ "$ENVIRONMENT" = "dev" ]; then \
        cat secrets.env config.env > .env; \
    else \
        cat secrets-prod.env config-prod.env > .env; \
    fi

RUN npm install

# build the app 
RUN npm run build 

ENV ORIGIN=https://localhost

# start the node.js app in build folder
CMD ["node", "-r", "dotenv/config", "build"] 