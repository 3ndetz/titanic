# Titanic

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Solving simple titanic competition using advanced engineering practices

## Project Organization

```text
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data`
├── README.md          <- The top-level README for developers using this project.
├── data               <- See docs/docs/data.md for details
│
├── docs               <- A default mkdocs project
│   └── reports        <- Course reports
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         titanic and configuration for tools like ruff
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
└── titanic   <- Source code for use in this project.
```

--------

## Распределение веток

```text
├── main            <- Текущая последняя проверенная версия кода
├── gh-pages        <- Автособираемая документация проекта mkdocs
├── task2           <- Branch for task 2
├── task3           <- Branch for task 3
...
└── taskN           <- Branch for task N
```

--------

> Task 1 сделан в main т.к. initial

## Документация

Документация проекта, в том числе по запуску: <https://3ndetz.github.io/titanic/>

> Билдится из `docs/docs` и подгружается в GH Pages по ссылке

## Отчёты

Отчёты для курса лежат в `docs/reports`:

1. [x] [HW 1](./docs/reports/hw1_initial.md)
2. [x] [HW 2](./docs/reports/hw2.md)
3. [ ] HW 3
4. [ ] HW 4
5. [ ] HW 5
6. [ ] HW 6
