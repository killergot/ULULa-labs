FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build  # => /app/dist/

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html