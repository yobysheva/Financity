# Используем официальный Node.js образ
FROM node:18-alpine
# Копируем приложение
COPY . /app
# Устанавливаем рабочую директорию
WORKDIR /app/frontend
# Устанавливаем зависимости
COPY package*.json /app/frontend/
RUN npm add global @vue/cli
RUN npm install
# Устанавливаем NODE_ENV в production
ENV NODE_ENV=production
# Собираем приложение
RUN npm run build
# Устанавливаем сервер для раздачи статических файлов
RUN npm install -g serve
# Expose порт для сервера
EXPOSE 8280
# Запускаем сервер для собранных файлов
CMD ["npm", "run", "serve"]