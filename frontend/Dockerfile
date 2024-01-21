# Stage 1: Build the React application
FROM node:alpine as build

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . ./

# Set the REACT_APP_BACKEND_URL environment variable for the Docker build
# ARG REACT_APP_BACKEND_URL
# ENV REACT_APP_BACKEND_URL=$REACT_APP_BACKEND_URL

ENV VITE_URL_MICROSERVICE_ONE=http://localhost:8001
ENV VITE_URL_MICROSERVICE_TWO=http://localhost:8002
ENV VITE_URL_MICROSERVICE_THREE=http://localhost:8003
ENV VITE_URL_MICROSERVICE_FOUR=http://localhost:8004
ENV VITE_WEBSOCKET_SERVER_URL=ws://localhost:8765

RUN npm run build

# Stage 2: Serve the application with Nginx
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
