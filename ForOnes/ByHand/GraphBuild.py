import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from cycler import cycler
import matplotlib as mpl
import os
from loguru import logger



LOGGING = 'logs.log'
FORMAT = "{time} {level} {message}"
logger.add(
    LOGGING,
    format=FORMAT,
    level="DEBUG",
    rotation="10 MB",
    retention="7 days",
    backtrace=True,
    diagnose=True,
    enqueue=True  # Асинхронная запись
)
@logger.catch
def init_n_polynom(x, npoly):
    if isinstance(npoly, int):
        return npoly+1
    else:
        print('chacl poly func = ', npoly(x))
        return npoly(x)
@logger.catch
def Building(file, data, plot_number, directory, N_task, npoly):
    logger.info("Starting Building function")


    # Логирование параметров
    logger.debug(f"Parameters: file={file.shape}, data={len(data)}, plot_number={plot_number}, "
                 f"directory={directory}, N_task={N_task}, npoly={npoly}")

    Valency = file['Знак PPG']
    Involvement = file['Сила SGR + PPG']

    Tasks = []
    TaskNumber = -1

    # Разбиение задач на группы
    while N_task / plot_number >= 1:
        N_task -= plot_number
        Tasks.append(plot_number)
    if N_task % plot_number != 0:
        Tasks.append(N_task % plot_number)

    logger.debug(f"Tasks divided into groups: {Tasks}")

    for team in Tasks:
        if team == 1:
            TaskNumber += 1
            time = data[TaskNumber]
            duration = np.arange(time[0] - 1, time[1])

            # Логирование временного интервала
            logger.debug(f"Processing task {TaskNumber + 1} with duration: {duration}")

            Val = Valency[time[0] - 1:time[1]]
            Inv = Involvement[time[0] - 1:time[1]]

            TrendValency = np.poly1d(np.polyfit(duration, Val, init_n_polynom(duration, npoly)))
            TrendInvolvement = np.poly1d(np.polyfit(duration, Inv, init_n_polynom(duration, npoly)))

            logger.debug(f"TrendValency coefficients: {TrendValency.coeffs}")
            logger.debug(f"TrendInvolvement coefficients: {TrendInvolvement.coeffs}")

            # Создание графиков
            fig, axs = plt.subplots(2, 1, figsize=(10, 15))
            axs[0].plot(duration, Val, color='#2D9182')
            axs[0].grid(True)
            axs[0].set_title(f'Эмоциональный знак по заданию {TaskNumber}')

            trend_color = '#912D2D' if np.polyfit(list(duration), Val, 1)[0] < 0 else '#2D9182'
            axs[0].plot(duration, TrendValency(duration), '--', label='Линия тренда по валентности', color=trend_color)

            axs[1].plot(duration, Inv, '-', color='#8B9BB3')
            axs[1].grid(True)
            axs[1].set_title(f'Вовлеченность по заданию {TaskNumber}')

            trend_color = '#912D2D' if np.polyfit(list(duration), Inv, 1)[0] < 0 else '#2D9182'
            axs[1].plot(duration, TrendInvolvement(duration), '--', label='Линия тренда по вовлеченности', color=trend_color)

            name = f'Задание {TaskNumber + 1}'
            filepath = os.path.join(directory, name)
            plt.savefig(filepath)
            logger.info(f"Saved plot for task {TaskNumber + 1} to {filepath}")

        else:
            tasks_per_page = team
            fig, axs = plt.subplots(2, tasks_per_page, figsize=(10, 15))

            for task in range(team):
                TaskNumber += 1
                time = data[TaskNumber]
                duration = np.arange(time[0] - 1, time[1])
                Val = Valency[time[0] - 1:time[1]]
                Inv = Involvement[time[0] - 1:time[1]]

                TrendValency = np.poly1d(np.polyfit(duration, Val, init_n_polynom(duration, npoly)))
                TrendInvolvement = np.poly1d(np.polyfit(duration, Inv, init_n_polynom(duration, npoly)))

                logger.debug(f"Processing task {TaskNumber + 1} with duration: {duration}")
                logger.debug(f"TrendValency coefficients: {TrendValency.coeffs}")
                logger.debug(f"TrendInvolvement coefficients: {TrendInvolvement.coeffs}")

                axs[0, task].plot(duration, Val, color='#2D9182')
                axs[0, task].grid(True)
                axs[0, task].set_title(f'Эмоциональный знак по заданию {TaskNumber}')

                trend_color = '#912D2D' if np.polyfit(list(duration), Val, 1)[0] < 0 else '#2D9182'
                axs[0, task].plot(duration, TrendValency(duration), '--', label='Линия тренда по валентности', color=trend_color)

                axs[1, task].plot(duration, Inv, '-', color='#8B9BB3')
                axs[1, task].grid(True)
                axs[1, task].set_title(f'Вовлеченность по заданию {TaskNumber}')

                trend_color = '#912D2D' if np.polyfit(list(duration), Inv, 1)[0] < 0 else '#2D9182'
                axs[1, task].plot(duration, TrendInvolvement(duration), '--', label='Линия тренда по вовлеченности', color=trend_color)

    logger.info("Finished Building function")
    plt.show()
