FROM node:16-alpine as build-stage
WORKDIR /app
RUN npm install -g http-server
COPY package*.json ./
RUN npm install
COPY . .

FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]