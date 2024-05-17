FROM node:latest
WORKDIR /app

COPY . .

RUN npm install

ENV PORT=5000
ENTRYPOINT [ "npm", "run", "dev", "--", "--host", "0.0.0.0" ]