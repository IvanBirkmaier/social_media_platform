# Stage 1: Build the React application
FROM node:alpine as build

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . ./

# Arg deswegen, damit man diese mit Env zu laufzeit des Containeras überschreiben kann.
ARG VITE_URL_MICROSERVICE_ONE=http://localhost:8001
ARG VITE_URL_MICROSERVICE_TWO=http://localhost:8002
ARG VITE_URL_MICROSERVICE_THREE=http://localhost:8003
ARG VITE_URL_MICROSERVICE_FOUR=http://localhost:8004
ARG VITE_WEBSOCKET_SERVER_URL=ws://localhost:8765

RUN npm run build

# Stage 2: Serve the application with Nginx
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
