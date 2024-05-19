FROM node:latest
WORKDIR /app

COPY . .

RUN npm install

ENV PORT=5173
# build the app 
RUN npm run build 

ENV ORIGIN=https://localhost

# start the node.js app in build folder
CMD ["node", "-r", "dotenv/config", "build"] 