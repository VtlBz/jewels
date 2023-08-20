# Проект Jewels

Cервис **Jewels**, для получения статистики по сделкам покупателей с драгоценными камнями.


---

### Использованные технологии:

- ***Django** 4.2*
- ***Django REST Framework** 3.14*
- *WSGI сервер **gunicorn** 21.2*
- *База Данных  **PostgreSQL***
- *Кэширование **Redis***
- *Контейнеризация **Docker***

*Приложение написано на **Python** 3.9*

---

### Как начать работу с проектом:

Клонировать репозиторий:
```bash
git clone git@github.com:VtlBz/jewels.git
```

Перейти в папку с проектом.

В указанной папке в файле .env указать переменные окружения, соответствующие проекту.
Пример заполнения:

```bash
SECRET_KEY=<указать-тут-ключ-проекта>
ALLOWED_HOSTS=<перечислить разрешенные хосты через пробел>

DEBUG_STATE=False # статус режима DEBUG, по умолчанию False

DB_ENGINE=django.db.backends.postgresql # Тип используемой БД. В проекте используется PostgreSQL
DB_NAME=postgres # Имя базы
POSTGRES_USER=postgres # Имя пользователя БД
POSTGRES_PASSWORD=postgres # Пароль пользователя БД
DB_HOST=db # Название сервиса (контейнера), по умолчанию - db
DB_PORT=5432 # Порт для подключения к сервису, стандартный по умолчанию

REDIS_HOST=localhost # Название сервиса (контейнера), по умолчанию - cache
REDIS_PORT=6379 # Порт для подключения к сервису, стандартный по умолчанию

COMPOSE_PROJECT_NAME=jewels # имя проекта проекта в Docker Compose
```

Запустить сборку контейнеров командой:

```bash
sudo docker compose up -d
```
- *В зависимости от настроек системы возможно тут и далее потребуется использовать команду **docker compose** c дефисом вместо пробела: **docker-compose***

При первом запуске создать и применить миграции:

```bash
sudo docker exec -it jewels-srv python manage.py makemigrations
sudo docker exec -it jewels-srv python manage.py migrate
```

При необходимости создать суперпользователя:

```bash
sudo docker exec -it jewels-srv python manage.py createsuperuser
```

[Базовая документация находится по адресу ```localhost:8000/api/v1/swagger/```](localhost:8000/api/v1/swagger/)

\* *ТЗ и тестовые данные лежат в папке ./data*