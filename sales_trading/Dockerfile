# Используем официальный образ Python
FROM python:3.10

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт для Django
EXPOSE 8000

CMD ["sh", "-c", "python manage.py makemigrations && python manage.py runserver 0.0.0.0:8000"]