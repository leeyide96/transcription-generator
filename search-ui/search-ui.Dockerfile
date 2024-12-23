FROM node:18

WORKDIR /app

COPY . /app/

RUN yarn add @elastic/search-ui-elasticsearch-connector

RUN yarn install

EXPOSE 3000

CMD ["yarn", "start"]