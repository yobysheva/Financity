# Используем официальный Node.js образ
FROM node:18-alpine

# Устанавливаем рабочую директорию
WORKDIR /app/frontend

# Копируем только package.json и package-lock.json для установки зависимостей
COPY frontend/package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем остальную часть приложения
COPY ./frontend /app/frontend

# Собираем приложение
RUN npm run build

# Устанавливаем сервер для раздачи статических файлов
RUN npm install -g serve

# Expose порт для сервера
EXPOSE 8280

# Запускаем сервер для собранных файлов
CMD ["npm", "run", "serve"]
