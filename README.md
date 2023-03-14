## Описание
Данный проект является сайтом с рецептами Foodgram.

В проекте хранятся рецепты публикуемые пользователями. У каждого рецепта можно указать ингредиенты и тэги.
Пользователи могут подписывать на авторов рецептов, могут добавлять рецепты в избранное, могут добавлять рецепты в корзину и скачивать необходимые ингредиенты в txt файле.

Аутентификация в проекте построена на токенах.

Неаутентифицированные пользователи имеют разрешение только на чтение.
Авторизованный пользователь может изменять только свои рецепты.


## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Algor45/foodgram-project-react.git
```

```
cd foodgram-project-react/
```

Cоздать и активировать виртуальное окружение:

```
py -3.7 -m venv env
```

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
py -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```


Перейти в папку, в которой находится файл manage.py:
```
cd backend/
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```


#### (Опционально) Заполнение БД.
Проект поддерживает заполнение базы данных из csv файлов.

Можно заполнить ингредиенты и тэги.

Чтобы залить данные в базу необходимо выполнить комманду:

```
python manage.py ingredients_csv_to_db

python manage.py tags_csv_to_db
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
