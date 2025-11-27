Getting started
===============

Поставить необходимое ПО на систему.

Информация о платформе и используемых версиях ПО для воспроизводимости:

- Платформа: Windows 11 Pro 25H2 64 Bit, build 26200.7171
- Версия [UV](https://docs.astral.sh/uv/#installation): uv 0.9.3 (83635a6c4 2025-10-15)
  - Поставлен через Windows powershell

    `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

- Версия Make: GNU Make 4.4.1 built for Windows32
  - Поставлен через [chocolatey](https://chocolatey.org/install)

    `choco install make`

- [Docker](https://www.docker.com/) на базе WSL, 28.5.1, build e180ab8
  - Docker Compose version v2.40.0-desktop.1
  - Docker Desktop Windows version 4.52.0

- [Git](https://git-scm.com/) version 2.51.0.windows.2

Затем:

Склонить репозиторий

```bash
git clone https://github.com/3ndetz/titanic.git
cd titanic
```

Если нужно, перейти в необходимую ветку

```bash
git checkout <имя_ветки>
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
