FROM node:lts as dependencies
WORKDIR /frontend

COPY package.json package-lock.json ./
RUN npm ci

ENV NODE_ENV development
EXPOSE 3000
CMD ["npm", "run", "dev"]
