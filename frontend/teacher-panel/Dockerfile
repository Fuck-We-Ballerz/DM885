FROM node:latest
WORKDIR /app

COPY . .

RUN npm install

ENTRYPOINT [ "npm", "run", "dev", "--", "--host", "0.0.0.0" ]