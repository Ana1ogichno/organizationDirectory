# organizationDirectory

**organizationDirectory** — сервис/бэкэнд для управления организациями, зданиями, их адресами и видами деятельности. Использует FastAPI, SQLAlchemy, асинхронный PostgreSQL, миграции Alembic, Poetry для зависимостей, Docker для контейнеризации.

---

## Содержание
- [Описание](#описание)
- [Технологии](#технологии)
- [Начало работы](#начало-работы)
- [Работа на базе репозитория](#работа-на-базе-репозитория)
- [Структура проекта](#структура-проекта)
- [Миграции Alembic](#миграции-alembic)
- [Deploy и CI/CD](#deploy-и-cicd)
- [Источники](#источники)

---

## Описание

Проект предназначен для хранения и поиска организаций по адресу, виду деятельности и зданиям. Реализованы фильтры, связи многие ко многим, поддержка сложных иерархий, кастомные репозитории и сервисы.

---

## Технологии

- Python 3.12+
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Poetry](https://python-poetry.org/)
- Docker, Docker Compose

---

## Начало работы

### Клонирование проектов и установка зависимостей
```sh
git clone <ссылка на репозиторий>
```
```sh
cd organizationDirectory
```
```sh
poetry install
```

### Запуск приложения через Docker
```sh
cp .env.example .env
```

### Запуск приложения через Docker
```sh
docker-compose up
```

### Запуск приложения вручную
```sh
chmod +x ./scripts/backend-start.sh
```
```sh
./scripts/backend-start.sh
```

---

## Работа на базе репозитория
Перед коммитом выполнить команды для проверки, исправления ошибок и форматирования кода:
- Проверка линтера ruff
```bash
make ruff-linter
```
- Автоматическое исправление ошибок линтера ruff
```bash
make ruff-linter-fix
```
- Форматирование когда
```bash
make ruff-formatter
```

---

## Структура проекта

- **alembic/** — миграции базы данных и скрипты Alembic
- **scripts/** — скрипты для запуска, инициализации окружения, вспомогательные утилиты
- **src/client/** — работа с базой данных, интеграция с Postgres, утилиты, схемы хранилищ
- **src/common/** — общие компоненты, схемы, модели, адаптеры, декораторы, ошибки
- **src/config/** — глобальные настройки, переменные окружения, документация
- **src/modules/activity/** — бизнес-логика, классы моделей, репозитории, сервисы (виды деятельности)
- **src/modules/building/** — бизнес-логика, классы моделей, фильтры, сервисы (здания)
- **src/modules/organization/** — управление организациями, адресами, телефонами, связями
- **src/server/** — основная точка входа, настройки FastAPI, middleware, роутинг

---

## Миграции Alembic

Файлы миграций размещаются в каталоге `alembic/`.
- Инициализация миграций:
    ```
    alembic init alembic
    ```
- Создать новую миграцию:
    ```
    alembic revision --autogenerate -m "описание изменений"
    ```
- Применить миграции:
    ```
    alembic upgrade head
    ```

---

## Deploy и CI/CD

- Используйте файлы Dockerfile, docker-compose.yaml и .env для быстрого продакшн-развертывания.

---

## Источники

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)