# build stage
FROM node:18.19 as build-stage

#Get Build Arguments
ARG VITE_API_URL
ARG VITE_USE_LIVE_DATA
ARG VITE_CACHE_DATA

WORKDIR /app

# Create env file with necessary values
# Create Local Environment Variables
RUN touch .env
RUN echo "VITE_API_URL=$VITE_API_URL\nVITE_USE_LIVE_DATA=$VITE_USE_LIVE_DATA\nVITE_CACHE_DATA=$VITE_CACHE_DATA" > .env

COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage
RUN mkdir /app
COPY --from=build-stage /app/dist /app
COPY nginx/nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]