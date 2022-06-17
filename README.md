# api_yamdb


### Для чего этот проект:
Проект **YaMDb** собирает отзывы пользователей на различные произведения.

API проекта YaMDb дает возможность просматривать просматривать описания произведений, читать отзывы и комментарии.

После регистрации доступно написание отзывов и выставление оценок для произведений. 

### Как запустить проект локально:
В документации описано, как должен работать API. 
Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Andr3w-k/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
### Примеры использования:
Когда вы запустите проект, по адресу:

```
http://127.0.0.1:8000/redoc/
```
будет доступна документация для API Yatube. 

Документация представлена в формате Redoc.