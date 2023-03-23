![example workflow](https://github.com/Algor45/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)


## Описание
Данный проект является сайтом с рецептами Foodgram.

В проекте хранятся рецепты публикуемые пользователями. У каждого рецепта можно указать ингредиенты и тэги.
Пользователи могут подписывать на авторов рецептов, могут добавлять рецепты в избранное, могут добавлять рецепты в корзину и скачивать необходимые ингредиенты в txt файле.

Аутентификация в проекте построена на токенах.

Неаутентифицированные пользователи имеют разрешение только на чтение.
Авторизованный пользователь может изменять только свои рецепты.


## Технологии:
Проект создан средствами Python, DgangoORM и Dgango REST Framework.
Аутентификация в проекте построена на simple_jwt.
Подключены Gunicorn и Nginx.
Проект запакован в контейнер средствами Docker.

## Как запустить проект:

Клонировать репозиторий:

```
git clone https://github.com/Algor45/foodgram-project-react.git
```

Перейти в папку infra:

```
cd infra/
```

Создать .env файл и заполнить его по шаблону:

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=<название базы данных>
POSTGRES_USER=<имя пользователя базы данных>
POSTGRES_PASSWORD=<пароль базы данных>
DB_HOST=db
DB_PORT=<порт>(по умолчанию = 5432)
```

В этой же папке выполнить команду развертывания проекта:

```
docker-compose up
```

Выполнить миграции:
```
docker-compose exec backend python manage.py migrate
```

Создать суперпользователя:
```
docker-compose exec backend python manage.py createsuperuser
```

Подключить статику:
```
docker-compose exec backend python manage.py collectstatic --no-input
```


Проект станет доступен по адресу:

```
http://localhost/
```

Для остановки проекта выполните команду:

```
docker-compose stop
```
Или воспользуйтесь комбинацией клавиш Ctrl+C в терминале с запущенным докером.


#### (Опционально) Заполнение БД.
Проект поддерживает заполнение базы данных из csv файлов.

Можно заполнить ингредиенты и тэги.

Чтобы залить данные в базу необходимо выполнить комманду:

```
docker-compose exec backend python manage.py ingredients_csv_to_db

docker-compose exec backend python manage.py tags_csv_to_db
```

## Системные требования

Версия Python:

```
Python 3.7
```

Зависимости:

```
Зависимости указаны в файле requirements.txt .
```

## Примеры
### Создание нового пользователя.

Запрос
```
POST http://127.0.0.1:8000/api/users/
Content-Type: application/json

{

    "email": "vpupkin@yandex.ru",
    "username": "vasya.pupkin",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "password": "Qwerty123"

}
```

Вернет
```
{

    "email": "vpupkin@yandex.ru",
    "id": 0,
    "username": "vasya.pupkin",
    "first_name": "Вася",
    "last_name": "Пупкин"

}
```
Создаст нового пользователя в базе данных.

### Получение токена.

Запрос
```
POST http://127.0.0.1:8000/api/auth/token/login/
Content-Type: application/json

{

    "password": "string",
    "email": "string"

}
```

Вернет
```
{

    "auth_token": "string"

}
```

Вернет токен в поле, который необходимо указывать в header Authorization в формате:
Authorization: Token <token>

### Просмотр списка произведений.

Запрос
```
GET http://127.0.0.1:8000/api/recipes/
Content-Type: application/json
Authorization: Token <token>

```

Вернет список рецептов в формате.

```
{
  "count": 123,
  "next": "http://foodgram.example.org/api/recipes/?page=4",
  "previous": "http://foodgram.example.org/api/recipes/?page=2",
  "results": [
    {
      "id": 0,
      "tags": [
        {
          "id": 0,
          "name": "Завтрак",
          "color": "#E26C2D",
          "slug": "breakfast"
        }
      ],
      "author": {
        "email": "user@example.com",
        "id": 0,
        "username": "string",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "is_subscribed": false
      },
      "ingredients": [
        {
          "id": 0,
          "name": "Картофель отварной",
          "measurement_unit": "г",
          "amount": 1
        }
      ],
      "is_favorited": true,
      "is_in_shopping_cart": true,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
      "text": "string",
      "cooking_time": 1
    }
  ]
}
```
