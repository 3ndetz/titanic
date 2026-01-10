"""Draft of ClearML Native Pipeline for Titanic HW.

This is a simple example of how to create a ClearML Native Pipeline. Not fully integrated with main pipeline (configs.)
"""

import argparse
from datetime import datetime, timedelta

from clearml import PipelineDecorator


# --- Обертки для шагов пайплайна ---
@PipelineDecorator.component(
    cache=True,  # Если шаг уже выполнялся с такими же входами - взять из кэша
    task_type="data_processing",
)
def step_process_data():
    # Импортируем внутри функции, чтобы не грузить модули раньше времени (особенно для remote execution)
    from titanic.dataset import main as run_process

    run_process()
    return True


@PipelineDecorator.component(
    cache=False,
    task_type="training",
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
    version="2.0"
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
        choices=["local", "queue", "schedule"],
        default="queue",
        help="Execution mode: local (run_locally), queue (enqueue to default), schedule (set schedule)",
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

    elif args.mode == "schedule":
        from clearml import Task
        # schedule time in UTC (avoid local timezone surprises)
        scheduled_time = datetime.now() + timedelta(minutes=2)
        print(f"Scheduling pipeline to run at {scheduled_time} UTC...")

        # create a controller Task that contains the pipeline code/artifacts
        task = Task.init(
            project_name="Titanic_HW",
            task_name="Titanic Native Pipeline (scheduled)",
            task_type=Task.TaskTypes.controller,
            reuse_last_task_id=False,
        )

        # set schedule: non-repeating, run on the requested queue
        task.set_schedule(
            repeating=False,
            scheduled_time=scheduled_time,
            execution_queue=args.queue,
        )

        # finish the Task definition so ClearML stores it; do NOT execute pipeline now
        task.close()
        print("Scheduled. Exiting.")
        return


if __name__ == "__main__":
    main()
