"""Draft of ClearML Native Pipeline for Titanic HW.

This is a simple example of how to create a ClearML Native Pipeline. Not fully integrated with main pipeline (configs.)
"""

import argparse
from datetime import datetime, timedelta, timezone

from clearml import PipelineDecorator
from clearml.automation import TaskScheduler


# --- Обертки для шагов пайплайна ---
@PipelineDecorator.component(
    cache=True,  # Если шаг уже выполнялся с такими же входами - взять из кэша
    task_type="data_processing",
    execution_queue="default",
)
def step_process_data():
    # Импортируем внутри функции, чтобы не грузить модули раньше времени (особенно для remote execution)
    from titanic.dataset import main as run_process

    run_process()
    return True


@PipelineDecorator.component(
    cache=False,
    task_type="training",
    execution_queue="default",
)
def step_train_model():
    from titanic.modeling.train import train_model as run_train

    # Вызываем нашу функцию
    run_train()
    return True


# --- Сам Пайплайн ---


@PipelineDecorator.pipeline(
    name="Titanic Native Pipeline",
    project="Titanic_HW",
    version="2.0",
    pipeline_execution_queue="default",
)
def execution_logic():
    # 1. Запускаем обработку данных
    if step_process_data():
        # 2. Передаем этот путь в тренировку
        return step_train_model()


def main():
    """Main function to parse run arguments and run the selected pipeline."""

    parser = argparse.ArgumentParser(description="Run Titanic Pipeline")
    parser.add_argument(
        "--mode",
        choices=["local", "schedule", "ui"],
        default="queue"
    )
    parser.add_argument(
        "--queue",
        default="default",
        help="Queue name for execution",
    )
    args = parser.parse_args()

    if args.mode == "local":
        # Запуск локально (прямо в текущем процессе)
        print("Running pipeline locally...")
        PipelineDecorator.run_locally()
        execution_logic()
    elif args.mode == "ui":
        execution_logic()
    elif args.mode == "schedule":
        # 1. Сначала нам нужно, чтобы задача Пайплайна существовала в ClearML.
        # Вызов execution_logic() создаст/обновит Task в ClearML, но не запустит его.
        print("Registering pipeline task...")
        execution_logic()
        
        # PipelineDecorator автоматически создает Task. Нам нужно получить его ID.
        # Обычно это последняя созданная задача в проекте с таким именем.
        from clearml import Task
        # Ищем задачу, которую только что создал декоратор
        task = Task.get_task(project_name="Titanic_HW", task_name="Titanic Native Pipeline")
        
        print(f"Found Pipeline Task ID: {task.id}")

        scheduled_time = datetime.now(timezone.utc) + timedelta(minutes=2)
        scheduled_time = scheduled_time.replace(second=0, microsecond=0)
        
        print(f"Scheduling for {scheduled_time} UTC...")

        scheduler = TaskScheduler()
        scheduler.add_task(
            schedule_task_id=task.id,
            queue=args.queue,
            name="Titanic_Auto_Schedule",
            minute=scheduled_time.minute,
            hour=scheduled_time.hour,
            day=scheduled_time.day,
            month=scheduled_time.month,
            year=scheduled_time.year,
            recurring=False
        )
        
        # ГЛАВНОЕ: Запустить шедулер.
        # start() запустит бесконечный цикл на ТВОЕМ компьютере, который будет ждать время Ч.
        # Как только время наступит, он отправит задачу в очередь и завершится (т.к. recurring=False).
        print("Scheduler started locally. Waiting for trigger time...")
        scheduler.start()


if __name__ == "__main__":
    main()
