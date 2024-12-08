# api_final
student: Nick_Light

Сервис предназначен для платформы блогов, где можно создать и прокомментировать публикации.

# Yatube

## Описание

Yatube — это социальная сеть, где пользователи могут создавать и делиться публикациями, комментировать их, а также подписываться на других пользователей и сообщества. Проект решает задачу взаимодействия пользователей через публикации и комментарии, позволяя им делиться мнениями и находить единомышленников.

## Установка

Для развертывания проекта на локальной машине выполните следующие шаги:


Клонируйте репозиторий:
```
git clone https://github.com/NikLight/Yatube.git
```

Откройте проэкт:
```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/bin/activate  # Для Linux/Mac
venv\Scripts\activate  # Для Windows
```

Установить зависимости из файла requirements.txt:


```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Перейдите в папку с основным исполнительным файлом manage.py
```
cd yatube_api
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

Создайте суперпользователя:

```
python manage.py createsuperuser
```

Запустите сервер:

```
python manage.py runserver
```

## Примеры запросов к API

Перед отправлением запросов установите необходимые приложения, внимание на контроль версий


Получение публикаций.
Получить список всех публикаций с пагинацией:

```
GET /api/posts/?limit=10&offset=0

```
Ответ:
```
{
    "count": 123,
    "next": "http://api.example.org/posts/?offset=10&limit=10",
    "previous": null,
    "results": [
        {
            "id": 1,
            "author": "user1",
            "text": "Hello World!",
            "pub_date": "2024-01-01T12:00:00Z",
            "image": null,
            "group": null
        }
    ]
}

```

Создание публикации

Добавить новую публикацию:

```
POST /api/posts/
Content-Type: application/json

{
    "text": "Моя первая публикация",
    "image": null,
    "group": null
}
```

Ответ:
```
{
    "id": 1,
    "author": "user1",
    "text": "Моя первая публикация",
    "pub_date": "2024-01-01T12:00:00Z",
    "image": null,
    "group": null
}

```

## Получение JWT-токена

Получить JWT-токен:

```
POST /api/token/
Content-Type: application/json

{
    "username": "user1",
    "password": "password"
}

```

Ответ:
```
{
    "refresh": "refresh_token_string",
    "access": "access_token_string"
}
```

## Лицензия

Yandex Practicum License


### Описание

Этот `README.md` содержит информацию о проекте Yatube,
его установке и примерах работы с API. 
