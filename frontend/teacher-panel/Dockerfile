FROM node:latest
WORKDIR /app

ENV PORT=5173

COPY . .

RUN cat secrets.env config.env > .env

RUN npm install

# build the app 
RUN npm run build 

ENV ORIGIN=https://localhost

# start the node.js app in build folder
CMD ["node", "-r", "dotenv/config", "build"] 