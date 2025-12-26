"""Draft of ClearML Native Pipeline for Titanic HW.

This is a simple example of how to create a ClearML Native Pipeline. Not fully integrated with main pipeline (configs.)
"""

from clearml import PipelineDecorator


# --- Обертки для шагов пайплайна ---
@PipelineDecorator.component(
    cache=True,  # Если шаг уже выполнялся с такими же входами - взять из кэша
    task_type="data_processing",
    # execution_queue="default",
)
def step_process_data():
    # Импортируем внутри функции, чтобы не грузить модули раньше времени (особенно для remote execution)
    from titanic.dataset import main as run_process

    run_process()
    return True


@PipelineDecorator.component(
    cache=False,
    task_type="training",
    # execution_queue="default",
)
def step_train_model():
    from titanic.modeling.train import train_model as run_train

    # Вызываем нашу функцию
    run_train()
    return True


# --- Сам Пайплайн ---


@PipelineDecorator.pipeline(name="Titanic Native Pipeline", project="Titanic_HW", version="2.0")
def execution_logic():
    # 1. Запускаем обработку данных
    if step_process_data():
        # 2. Передаем этот путь в тренировку
        return step_train_model()


if __name__ == "__main__":
    # Запускаем локально (без агентов, прямо в текущем процессе)
    # Это создаст граф, выполнит код и зальет логи
    PipelineDecorator.run_locally()

    # Запуск с параметрами (которые можно менять в UI при перезапуске!)
    execution_logic()
