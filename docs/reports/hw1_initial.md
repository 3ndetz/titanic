# Initial Report

## Задача

<section id="дз-1-настройка-рабочего-места-data-scientist" class="level2">
<h2 class="anchored" data-anchor-id="дз-1-настройка-рабочего-места-data-scientist">ДЗ 1: Настройка рабочего места Data Scientist<a class="anchorjs-link " aria-label="Anchor" data-anchorjs-icon="" href="#дз-1-настройка-рабочего-места-data-scientist" style="font: 1em / 1 anchorjs-icons; margin-left: 0.1875em; padding-right: 0.1875em; padding-left: 0.1875em;"></a></h2>
<ul>
<li><strong>Баллы:</strong> 8 баллов<br>
</li>
<li><strong>Срок сдачи:</strong> 24 ноября</li>
</ul>
<section id="описание" class="level3">
<h3 class="anchored" data-anchor-id="описание">Описание<a class="anchorjs-link " aria-label="Anchor" data-anchorjs-icon="" href="#описание" style="font: 1em / 1 anchorjs-icons; margin-left: 0.1875em; padding-right: 0.1875em; padding-left: 0.1875em;"></a></h3>
<p>Настройте полноценное рабочее место для Data Science с использованием современных инженерных практик.</p>
</section>
<section id="требования" class="level3">
<h3 class="anchored" data-anchor-id="требования">Требования<a class="anchorjs-link " aria-label="Anchor" data-anchorjs-icon="" href="#требования" style="font: 1em / 1 anchorjs-icons; margin-left: 0.1875em; padding-right: 0.1875em; padding-left: 0.1875em;"></a></h3>
<ol type="1">
<li><strong>Структура проекта (2 балла):</strong>
<ul>
<li>Создать структуру папок с помощью Cookiecutter или Copier</li>
<li>Настроить шаблоны для новых проектов</li>
<li>Создать README с описанием проекта</li>
</ul></li>
<li><strong>Качество кода (2 балла):</strong>
<ul>
<li>Настроить pre-commit hooks</li>
<li>Настроить форматирование кода (Black, isort, Ruff)</li>
<li>Настроить линтеры (Ruff, MyPy, Bandit)</li>
<li>Создать конфигурационные файлы</li>
</ul></li>
<li><strong>Управление зависимостями (2 балла):</strong>
<ul>
<li>Настроить пакетный менджер (например poretry или pixi) для управления зависимостями</li>
<li>Создать pyproject с точными версиями</li>
<li>Настроить виртуальное окружение</li>
<li>Создать Dockerfile для контейнеризации</li>
</ul></li>
<li><strong>Git workflow (1 балл):</strong>
<ul>
<li>Настроить Git репозиторий</li>
<li>Создать .gitignore для ML проекта</li>
<li>Настроить ветки для разных этапов работы</li>
</ul></li>
<li><strong>Отчет о проделанной работе (1 балл):</strong>
<ul>
<li>Создать отчет в формате Markdown</li>
<li>Описать настройку каждого инструмента</li>
<li>Добавить скриншоты результатов</li>
<li>Сохранить отчет в Git репозитории</li>
</ul></li>
</ol>
</section>
<section id="критерии-оценки" class="level3">
<h3 class="anchored" data-anchor-id="критерии-оценки">Критерии оценки<a class="anchorjs-link " aria-label="Anchor" data-anchorjs-icon="" href="#критерии-оценки" style="font: 1em / 1 anchorjs-icons; margin-left: 0.1875em; padding-right: 0.1875em; padding-left: 0.1875em;"></a></h3>
<ul>
<li><strong>Отлично (8 баллов):</strong> Все требования выполнены, код качественный</li>
<li><strong>Хорошо (6-7 баллов):</strong> Основные требования выполнены</li>
<li><strong>Удовлетворительно (4-5 баллов):</strong> Большинство требований выполнено</li>
<li><strong>Неудовлетворительно (0-3 балла):</strong> Требования не выполнены</li>
</ul>
<p><strong>⚠️ ВАЖНО:</strong> Менторы будут воспроизводить ваши результаты, поэтому постарайтесь все автоматизировать. Если что-то не совпадет при воспроизведении, можно потерять баллы.</p>
<hr>
</section>
</section>

## Преподготовка

Создадим папку проекта, подгрузим шаблон, подтянем окружение.

1. Установил uv
2. `mkdir titanic`, `cd titanic`
3. Создал и активировал venv

   ```bash
   uv venv --python 3.12.12
   .venv/Scripts/activate.bat
   ```

4. Поставил cookiecutter
   
   `uv pip install cookiecutter-data-science`

5. Кастомизировал шаблон и создал проект

    ```
    (titanic) C:\Stud\Repos\titanic>ccds
    project_name (project_name): titanic
    repo_name (titanic): titanic
    module_name (titanic): 
    author_name (Your name (or your organization/company/team)): 3ndetz
    description (A short description of the project.): Solving simple titanic competition with advanced engineering practices
    python_version_number (3.10): 3.12.12
    Select dataset_storage
        1 - none
        2 - azure
        3 - s3
        4 - gcs
        Choose from [1/2/3/4] (1): 1
    Select environment_manager
        1 - virtualenv
        2 - conda
        3 - pipenv
        4 - uv
        5 - pixi
        6 - poetry
        7 - none
        Choose from [1/2/3/4/5/6/7] (1): 4
    Select dependency_file
        1 - requirements.txt
        2 - pyproject.toml
        3 - environment.yml
        4 - Pipfile
        5 - pixi.toml
        Choose from [1/2/3/4/5] (1): 2
    Select pydata_packages
        1 - none
        2 - basic
        Choose from [1/2] (1): 
    Select testing_framework
        1 - none
        2 - pytest
        3 - unittest
        Choose from [1/2/3] (1): 2
    Select linting_and_formatting
        1 - ruff
        2 - flake8+black+isort
        Choose from [1/2] (1): 
    Select open_source_license
        1 - No license file
        2 - MIT
        3 - BSD-3-Clause
        Choose from [1/2/3] (1): 2
    Select docs
        1 - mkdocs
        2 - none
        Choose from [1/2] (1): 1
    Select include_code_scaffold
        1 - Yes
        2 - No
        Choose from [1/2] (1): 
    ```

    Всё создалось на уровне ниже (`titanic/titanic`), поэтому в следующий раз перед `ccds` буду делать `cd ..`

## Настройка

1. Настроим gitignore, пока что уберём uv.lock
2. Добавим .env.example
3. Добавим pre-commit hook в .pre-commit-config.yaml (Конфиги линтера уже подтянулись от cookiecutter в pyproject.toml, поэтому настраиваю только пре-коммит)
4. Добавим pre-commit его в pyproject.toml через `uv add`.

    Важная ремарка: пока не ставлю точные версии пакетов в pyproject.toml, зафиксирую уже когда буду работать с питоном, данными, экспериментами.
5. Сделаем докерфайл `Dockerfile`
6. докеркомпоз (т.к. мне неудобно запускать через докерфайл, проще сразу делать композ)
7. Забилдил gh pages c документацией сразу
   1. делал просто `cd docs` && `mkdocs gh-deploy`
8. Обновил ридми, добавил ссылок

## Итоги и скрины

Подготовил репозиторий к работе.

Докер `docker-compose up --build` ставит зависимости и запускает "тесты", пока там просто заглушка, которая выбивает fail, так и должно быть:

![alt text](images/hw1_initial/image.png)

Пре-коммит работает:

`pre-commit run --all-files`

![alt text](images/hw1_initial/image-1.png)

Тестовые штуки (из шаблона самого cookiecutter) работают, например `make data`:

![alt text](images/hw1_initial/image-2.png)
