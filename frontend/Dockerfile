FROM node:20-slim

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
#COPY . .
COPY frontend/ .

EXPOSE 5137

CMD [ "npm","start" ]