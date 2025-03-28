# Используем официальный образ Python
FROM python:3.13-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y gcc python3-dev libpq-dev postgresql-client locales gettext && rm -rf /var/lib/apt/lists/*
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    sed -i '/ru_RU.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
RUN dpkg-reconfigure --frontend=noninteractive locales && \
    locale-gen ru_RU.UTF-8 && \
    update-locale LANG=ru_RU.UTF-8
ENV LANG=ru_RU.UTF-8
ENV LANGUAGE=ru_RU:ru
ENV LC_ALL=ru_RU.UTF-8
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# Копируем весь проект в контейнер
COPY . /app/

# Собираем статику (при необходимости, можно раскомментировать)
RUN python manage.py collectstatic --noinput

# Компилируем .po файлы в .mo файлы
RUN python manage.py compilemessages

# Запускаем Gunicorn, привязываясь к порту 3245
CMD ["gunicorn", "pyweb_hw_10.wsgi:application", "--bind", "0.0.0.0:3245"]
