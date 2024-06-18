# Используем базовый образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл зависимостей в рабочую директорию
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё содержимое проекта в рабочую директорию
COPY . .

# Открываем порт 5000 для Flask
EXPOSE 5000

# Команда для запуска приложения
CMD ["python", "app.py"]