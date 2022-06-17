# api_yamdb


### Для чего этот проект:
Проект **YaMDb** собирает отзывы пользователей на различные произведения.

API проекта YaMDb дает возможность просматривать просматривать описания произведений, читать отзывы и комментарии.

После регистрации доступно написание отзывов и выставление оценок для произведений. 
### Технологии:
Python 3.7
Django 2.2.16
Django rest framework 3.12.4
Djoser 2.1.0

### Как запустить проект через Docker:
Шаблон наполнения env-файла:
```
SECRET_KEY = "***"

DB_ENGINE = django.db.backends.postgresql
DB_NAME = postgres
POSTGRES_USER = postgres
POSTGRES_PASSWORD = xxxyyyzzz
DB_HOST = db
DB_PORT = 1234
```
Запустите docker-compose командой:
```
docker-compose up -d --build
```
Теперь в контейнере web нужно выполнить миграции, создать суперпользователя и собрать статику:
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input 
```
Команды для заполнения базы данными (копирование фикстур в запущенный контейнер):
```
/infra_sp2$ cd infra
tar -cv fixtures.json | docker exec -i infra_web_1 tar x -C .
docker-compose exec web python manage.py loaddata fixtures.json
```
*infra_web_1 - имя контейнера, так же можно использовать ID.
Эти данные можно получить командой ``` docker ps```

### Примеры использования:
Когда вы запустите проект, по адресу:

```
http://localhost/redoc/
```
будет доступна документация для API Yatube. 

Документация представлена в формате Redoc.

### Авторы:
- https://github.com/Andr3w-k
- https://github.com/Aleksey-Savchuk
- https://github.com/yoninjago
