# Calculator-Calories

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Описание

Calculator-Calories - это веб-приложение на Flask для учета калорий. Пользователи могут отслеживать потребление калорий на каждый день, добавлять записи о приеме пищи, просматривать статистику и многое другое.

## Требования

- Python 3.x
- Flask
- SQLAlchemy
- PostgreSQL (или другая база данных, совместимая с SQLAlchemy)

## Установка

1. Клонируйте репозиторий на свой компьютер:

git clone https://github.com/XRN-wq/Calculator-Calories.git
cd Calculator-Calories
Установите зависимости:
pip install -r requirements.txt
Создайте базу данных (если используете PostgreSQL, убедитесь, что у вас установлена и настроена PostgreSQL):

createdb db  # Замените "db" на имя вашей базы данных
Запустите приложение:

python script.py
Приложение будет доступно по адресу http://127.0.0.1:5000/.

Как пользоваться
Откройте приложение в веб-браузере по адресу http://127.0.0.1:5000/.
На главной странице вы можете вводить свои калории и сохранять их.
Для просмотра статистики, перейдите на страницу http://127.0.0.1:5000/statistics.
Тестирование
Для запуска тестов выполните следующую команду:

python -m unittest test_app.py