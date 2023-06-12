# Quiz App (bewise_task1)

Привет! Добро пожаловать в Quiz App! Это приложение Django, которое позволяет пользователю получить случайные вопросы из открытого API и сохранить их в базе данных PostgreSQL.

## Установка

1. Установите Docker, если его еще нет на вашей системе.

2. Склонируйте репозиторий Quiz App на свою локальную машину:

  `git clone https://github.com/eromanv/bewise_task1.git`

3. Перейдите в каталоге infra:

    `cd infra`

4. Создайте файл .env

        DB_ENGINE=django.db.backends.postgresql
        DB_NAME=postgres
        POSTGRES_USER=postgres
        POSTGRES_PASSWORD=postgres
        DB_HOST=db
        DB_PORT=5432

5. Запустите контейнеры Docker с помощью docker-compose:

`docker-compose up`

6. После запуска контейнеров приложение будет доступно по адресу <http://localhost:8000>.

## Использование

Чтобы получить случайные вопросы, отправьте POST-запрос на <http://localhost:8000/api/process_questions/> с параметром questions_num, указывающим количество вопросов, которое вы хотите получить.

Например:

    POST /api/process_questions/ HTTP/1.1
    Host: localhost:8000
    Content-Type: application/json

    {
    "questions_num": 5
    }

Вопросы будут получены из открытого API jservice.io. Полученные вопросы будут сохранены в базе данных PostgreSQL.
Вы также можете получить конкретный вопрос, отправив GET-запрос на <http://localhost:8000/api/question/{id}/>, где {id} - идентификатор вопроса.

## Технологии

Django REST Framework, PostgreSQL, Docker

## Автор
Егоров Роман (@eromanvad)
