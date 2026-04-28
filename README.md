# DevOps Project

Проект реализует контейнеризированную инфраструктуру для запуска веб-приложения и автоматизированного тестирования. Инфраструктура описана через Docker Compose: один контейнер запускает Flask-приложение, второй используется для выполнения проверок и имеет доступ к исходникам приложения в режиме read-only.

## Что входит в проект

- `Dockerfile_app` - образ приложения на базе Ubuntu 22.04. Внутри устанавливаются Python, Flask-зависимости, SSH-сервер и исходники примера `EXAMPLE_APP` из репозитория `moevm/devops-examples`.
- `Dockerfile_tester` - образ тестового окружения с Python, `requests`, `css-html-prettify` и SSH-сервером.
- `docker-compose.yml` - описание сервисов `app` и `tester`, портов, volume и лимитов CPU.
- `.env.example` - пример переменных окружения для запуска.
- `tester/tests` - скрипты проверок.
- `tester/logs` - директория для логов запуска тестов.

## Архитектура

```text
host
  |
  |-- 127.0.0.1:${APP_PORT}      -> app:5000
  |-- 127.0.0.1:${APP_SSH_PORT}  -> app:22
  |-- 127.0.0.1:${TESTER_SSH_PORT} -> tester:22

docker volume: app_source
  |
  |-- /app      в контейнере app
  |-- /app:ro   в контейнере tester
```

Сервис `app` запускает Flask-приложение на порту `5000`. Сервис `tester` зависит от `app`, монтирует папку `/app` только для чтения и выполняет тесты, взаимодействуя с приложением по HTTP и анализируя его исходный код. Внутри Docker-сети контейнер `tester` обращается к приложению по адресу `http://app:5000`.

## Требования

- Docker
- Docker Compose

## Быстрый старт

1. Склонируйте репозиторий:

```bash
git clone https://github.com/elinatar/DevOps_project.git
cd DevOps_project
```

2. Создайте файл окружения:

```bash
cp .env.example .env
```

3. При необходимости измените значения в `.env`:

```env
APP_PORT=8000
APP_SSH_PORT=2222
TESTER_SSH_PORT=2223

SSH_USER=devops
SSH_PASSWORD=devops80

CPUS=1
```

4. Соберите и запустите контейнеры:

```bash
docker compose up --build -d
```

5. Откройте приложение:

```text
http://127.0.0.1:8000
```

Если вы изменили `APP_PORT` в `.env`, используйте выбранный порт.

## Запуск тестов

Тесты запускаются внутри контейнера `tester`:

```bash
docker compose exec tester python3 tests/run_tests.py
```

Скрипт `run_tests.py` выполняет следующие проверки:

- `test_html_format.py` - проверяет форматирование HTML-шаблонов приложения через `css-html-prettify`.
- `test_custom_rule.py` - выполняет статический анализ Python-файлов приложения с пользовательским правилом: запрещено использование переменных с именем `elina`.
- `test_upload.py` - интеграционный тест загрузки файла через endpoint `/upload` приложения.

Во время выполнения тестов вывод направляется в стандартные потоки контейнера: `stdout` и `stderr`. Поэтому результаты можно просматривать через `docker logs`:

```bash
docker compose logs tester
```

Дополнительно результаты сохраняются в файлы:

```text
tester/logs/stdout.log
tester/logs/stderr.log
```

Каждая строка логов записывается с timestamp в формате:

```text
[YYYY-MM-DD HH:MM:SS] message
```

Если все проверки прошли успешно, в `stdout.log` появится строка:

```text
ALL TESTS PASSED
```

## SSH-доступ к контейнерам

В оба контейнера добавляется пользователь из переменных `SSH_USER` и `SSH_PASSWORD`.

Подключение к контейнеру приложения:

```bash
ssh devops@127.0.0.1 -p 2222
```

Подключение к тестовому контейнеру:

```bash
ssh devops@127.0.0.1 -p 2223
```

Пароль по умолчанию:

```text
devops80
```

## Полезные команды

Посмотреть статус контейнеров:

```bash
docker compose ps
```

Посмотреть логи приложения:

```bash
docker compose logs -f app
```

Посмотреть логи тестового контейнера:

```bash
docker compose logs -f tester
```

Остановить проект:

```bash
docker compose down
```

Остановить проект и удалить volume:

```bash
docker compose down -v
```

## Переменные окружения

| Переменная | Назначение | Значение по умолчанию |
| --- | --- | --- |
| `APP_PORT` | Порт приложения на хосте | `8000` |
| `APP_SSH_PORT` | SSH-порт контейнера `app` на хосте | `2222` |
| `TESTER_SSH_PORT` | SSH-порт контейнера `tester` на хосте | `2223` |
| `SSH_USER` | Пользователь для SSH-доступа | `devops` |
| `SSH_PASSWORD` | Пароль пользователя для SSH-доступа | `devops80` |
| `CPUS` | CPU limit для сервисов Docker Compose | `1` |

## Структура проекта

```text
.
|-- .env.example
|-- Dockerfile_app
|-- Dockerfile_tester
|-- docker-compose.yml
|-- README.md
`-- tester
    |-- logs
    |   `-- тестовые логи создаются при запуске проверок
    `-- tests
        |-- run_tests.py
        |-- test_custom_rule.py
        |-- test_html_format.py
        `-- test_upload.py
```

## Назначение проекта

Проект подходит для практики базового DevOps-сценария:

- сборка Docker-образов;
- запуск нескольких связанных сервисов через Docker Compose;
- настройка переменных окружения;
- проброс портов на localhost;
- организация отдельного контейнера для тестов;
- сохранение логов тестирования;
- доступ к контейнерам по SSH.

## Результат выполнения

Все этапы тестирования успешно пройдены:

- форматирование HTML;
- статический анализ;
- интеграционный тест.

```text
ALL TESTS PASSED
```

Автор: Элина Тараненко