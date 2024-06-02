FROM node:14.18-alpine3.15

WORKDIR /yunpdp

COPY package*.json ./


RUN npm install

RUN npm install -g nodemon

COPY . .


EXPOSE 3000

CMD ["npm", "start"]