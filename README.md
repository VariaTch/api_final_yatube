Yatube API

Yatube API — это учебный проект, представляющий собой бэкенд на Django REST Framework для платформы блогов Yatube, включающий:

    Систему публикации постов — создание, редактирование и просмотр;

    Систему пользователей — создание пользователей, подписка на других;

    Систему комментариев — возможность оставлять комментарии к постам.

Установка и запуск

    Клонируйте репозиторий на свой компьютер:

git clone https://github.com/gutsy51/ya-practicum-backend/tree/master/api_yatube2
cd api_yatube2

Создайте и активируйте виртуальное окружение:

Windows:

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

Linux/MacOS:

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Примените миграции:

cd api_yatube
python manage.py migrate

Запустите сервер:

    python manage.py runserver

Быстрая справка по API

Полное описание доступно по адресу: http://localhost/redoc/
JWT Токен

POST /api/v1/jwt/create/

Тело запроса:

{
  "username": "username",
  "password": "password"
}

Ответ:

{
  "refresh": "refresh_token",
  "access": "access_token"
}

Посты
Путь	Метод	Описание	Доступ
/api/v1/posts/	GET	Получить посты (с пагинацией)	Всем
/api/v1/posts/	POST	Создать новый пост	Авторизованный
/api/v1/posts/{id}/	GET	Получить информацию о посте	Всем
/api/v1/posts/{id}/	PUT/PATCH	Обновить пост	Автор + Автор поста
/api/v1/posts/{id}/	DELETE	Удалить пост	Автор + Автор поста

Примеры:

    GET /api/v1/posts/ — Получить все посты (первая страница, до 10 постов);

    GET /api/v1/posts/?limit=10&offset=10 — Получить все посты (вторая страница, 10 постов);

    GET /api/v1/posts/?search=hello — Получить все посты с "hello" в заголовке.

Комментарии
Путь	Метод	Описание	Доступ
/api/v1/posts/{post_id}/comments/	GET	Все комментарии	Всем
/api/v1/posts/{post_id}/comments/	POST	Добавить новый комментарий	Авторизованный
/api/v1/posts/{post_id}/comments/{id}/	GET	Получить информацию о комментарии	Всем
/api/v1/posts/{post_id}/comments/{id}/	PUT/PATCH	Обновить комментарий	Автор + Автор комментария
/api/v1/posts/{post_id}/comments/{id}/	DELETE	Удалить комментарий	Автор + Автор комментария

Примеры:

    GET /api/v1/posts/1/comments/ — Получить все комментарии к посту с id=1;

    POST /api/v1/posts/1/comments/ — Создать новый комментарий к посту с id=1.

Подписки
Путь	Метод	Описание	Доступ
/api/v1/follow/	GET	Все подписки	Авторизованный
/api/v1/follow/	POST	Подписаться на другого пользователя	Авторизованный
/api/v1/follow/{id}/	DELETE	Отписаться от пользователя	Авторизованный

Примеры:

    GET /api/v1/follow/ — Получить все подписки текущего пользователя;

    POST /api/v1/follow/ — Подписаться на другого пользователя.