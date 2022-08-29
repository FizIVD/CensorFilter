# образ на основе которого создаём контейнер

FROM python:3.9

# рабочая директория внутри проекта
WORKDIR /cen

# переменные окружения для python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
# копируем содержимое текущей папки в контейнер
EXPOSE 8000
COPY . .

CMD ["python","manage.py","runserver", "0.0.0.0:8000","--insecure"]