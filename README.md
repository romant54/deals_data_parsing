# Deals data trees parsing application

Это приложение реализизовано на фреймворке FastAPI с использованием базы данных PostgreSQL.
Внутри репозитория реализована логика для развертывания приложения с Docker и Docker Compose.

## Требования

Для запуска потребуется:

- Docker
- Docker Compose

## Установка и запуск

1. **Клонирование репозитория**

   `git clone https://github.com/romant54/contracts_parsing.git`

   `cd contracts_parsing/`

2. **Настройка**

По необходимости убедитесь, что конфигурации файлов `Dockerfile` и `docker-compose.yml` корректны для вашей локальной среды.

3. **Запуск с помощью Docker Compose**

`docker-compose up`

Эта команда соберет образ для приложения FastAPI и запустит его вместе с базой данных PostgreSQL.

4. **Проверка**

После запуска приложение будет доступно по адресу `http://localhost:8000`.

5. **Тестирование**

В корне проекта расположена директория `testing/`, в которой представлены:
- Готовая [Postman-коллекция](testing/Deals_trees_processing.postman_collection.json) для тестирования приложения
- Файлы форматов JSON/XML содержащие сигнатуры запросов для тестирования с помощью других инструментов
