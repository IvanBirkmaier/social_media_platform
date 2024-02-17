# Stage 1: Build the React application
FROM node:alpine as build

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . ./

# ENV deswegen, damit man diese mit Env zu laufzeit des Containeras überschreiben kann.
ENV VITE_URL_MICROSERVICE_ONE=http://localhost:8001
ENV VITE_URL_MICROSERVICE_TWO=http://localhost:8002
ENV VITE_URL_MICROSERVICE_THREE=http://localhost:8003
ENV VITE_URL_MICROSERVICE_FOUR=http://localhost:8004
ENV VITE_WEBSOCKET_SERVER_URL=ws://localhost:8765

RUN npm run build

# Stage 2: Serve the application with Nginx
FROM nginx:alpine

# Installiere envsubst (Teil von gettext)
RUN apk add --no-cache gettext

# Kopiere den gebauten dist Ordner von der Build-Stage
COPY --from=build /app/dist /usr/share/nginx/html

COPY config-template.js /config-template.js
COPY start-container.sh /start-container.sh


# Mache das Start-Skript ausführbar
RUN chmod +x /start-container.sh

# Setze das Start-Skript als CMD
CMD ["/start-container.sh"]


# # Stage 2: Serve the application with Nginx
# FROM nginx:alpine

# COPY --from=build /app/dist /usr/share/nginx/html
# EXPOSE 80
# CMD ["nginx", "-g", "daemon off;"]
