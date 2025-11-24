FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Копирование файлов зависимостей
COPY pyproject.toml ./

# Установка зависимостей
RUN uv pip install --system --no-cache -r pyproject.toml

# Копирование только нужных файлов и папок
COPY titanic/ ./titanic/
COPY tests/ ./tests/

# Ридми нужен для flitcore
COPY README.md LICENSE ./

# Установка самого пакета
RUN uv pip install --system --no-cache -e .

# Создание необходимых директорий
RUN mkdir -p data/raw data/processed models

# CMD ["python", "-m", "titanic.train"]

# Expose Jupyter port
EXPOSE 8888

# Default command
CMD ["/bin/bash"]