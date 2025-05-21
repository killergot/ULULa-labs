FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
# Создаем директорию для SSL
RUN mkdir -p /etc/nginx/ssl
# Копируем SSL-сертификат и ключ
COPY --from=build /app/server.crt /etc/nginx/ssl/
COPY --from=build /app/server.key /etc/nginx/ssl/
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80 443
CMD ["nginx", "-g", "daemon off;"]