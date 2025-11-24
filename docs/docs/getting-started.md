Getting started
===============

Поставить uv на систему и makefile (если нету).

Затем:

Склонить репозиторий

```bash
git clone https://github.com/3ndetz/titanic.git
```

Создать окружение

```bash
make create_environment
```

Поставить зависимости

```bash
make requirements
```

Если нужны хуки pre-commit, поставить:

```bash
pre-commit install
```

Запустить тесты в докере:

```bash
docker-compose up --build
```
