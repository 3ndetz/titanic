# Modeling

This section describes the ML modeling process. It covers training procedures, evaluation metrics, and hyperparameter tuning.

## Эксперименты

В `params.yaml` в корне проекта лежат стандартные конфиги экспериментов. Сейчас используется модель Random Forest.

Эксперименты запускаются через `titanic/modeling/train.py`, который читает параметры из `params.yaml`. Здесь при необходимости можете изменять пайплайн тестирования (код).

Настроена удобная автоматизация запуска и версионирования экспериментов через DVC.
Например, если необходимо изменить только параметр `n_estimators` модели, можно запустить эксперимент командой:

`dvc exp run --name my_experiment -S train.n_estimators=200`

Сохранение эксперимента

```bash
dvc exp apply <experiment_name>
git add .
git commit -m "Applied experiment: <experiment_name>"
```

Для сравнения только что проведедённого эксперимента эксперимент рекомендуется запустить несколько раз с разными параметрами.

Посмотреть сравнительные результаты экспериментов можно командой:

`dvc exp show`

[UNIMPLEMENTED] `dvc metrics diff` покажет в упрощённом формате разницу метрик экспериментов.

Удалить ненужные эксперименты

`dvc exp remove <experiment_name>`

Очистить все временные эксперименты

`dvc exp gc --workspace`
