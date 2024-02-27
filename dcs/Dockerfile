FROM python:3.12
LABEL authors="Toksi86"

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Запустите приложение
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]