import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from cycler import cycler
import matplotlib as mpl
import os
from loguru import logger

# Глобальная настройка логгера
LOGGING_FILE = 'logs.log'
LOGGING_FORMAT = "{time} {level} {message}"

# Добавляем файл для записи логов
logger.add(LOGGING_FILE, format=LOGGING_FORMAT, level="DEBUG", rotation="1 MB", backtrace=True, diagnose=True)

@logger.catch
def init_n_polynom(x, npoly):
    """
    Функция для определения степени полинома.
    """
    if isinstance(npoly, int):
        logger.debug(f"npoly is an integer: {npoly}")
        return npoly + 1
    else:
        logger.debug(f"npoly is a function: {npoly}")
        result = npoly(x)
        logger.debug(f"Result of npoly(x): {result}")
        return result

@logger.catch
def Building(dfs, timings, plot_number, N_resp, directory, N_task, npoly):
    """
    Функция для построения графиков по данным респондентов.
    """
    logger.info("Starting Building function")

    if not os.path.exists(directory):
        logger.warning(f"Directory '{directory}' does not exist. Creating it...")
        os.makedirs(directory)

    Resps = []
    resp = 0

    # Разбиение задач на группы
    while N_resp / plot_number >= 1:
        N_resp -= plot_number
        Resps.append(plot_number)
    if N_task % plot_number != 0:
        Resps.append(N_task % plot_number)

    logger.debug(f"Tasks divided into groups: {Resps}")

    for team in Resps:
        TaskNumber = -1

        if team == 1:
            for taskNumber in range(len(timings)):
                TaskNumber += 1
                logger.debug(f"Processing task {TaskNumber + 1} for respondent {resp + 1}")

                try:
                    file = pd.read_excel(dfs[resp])
                    data = timings[resp]
                    Valency = file['Знак PPG']
                    Involvement = file['Сила SGR + PPG']
                except Exception as e:
                    logger.error(f"Error reading Excel file for respondent {resp + 1}: {e}")
                    plt.close('all')
                    continue

                time = data[TaskNumber]
                Val = Valency[time[0] - 1:time[1]]
                Inv = Involvement[time[0] - 1:time[1]]
                duration = np.arange(time[0] - 1, time[1])

                # Вычисление трендов
                TrendValency = np.poly1d(np.polyfit(list(duration), Val, init_n_polynom(duration, npoly)))
                TrendInvolvement = np.poly1d(np.polyfit(list(duration), Inv, init_n_polynom(duration, npoly)))

                logger.debug(f"TrendValency coefficients: {TrendValency.coeffs}")
                logger.debug(f"TrendInvolvement coefficients: {TrendInvolvement.coeffs}")

                # Создание графиков
                fig, axs = plt.subplots(2, figsize=(10, 15))
                axs[0].plot(duration, Val, color='#2D9182')
                axs[0].grid(True)
                axs[0].spines['top'].set_visible(False)
                axs[0].spines['right'].set_visible(False)
                axs[0].spines['bottom'].set_visible(False)
                axs[0].spines['left'].set_visible(False)

                trend_color = '#912D2D' if np.polyfit(list(duration), Val, 1)[0] < 0 else '#2D9182'
                axs[0].plot(duration, TrendValency(duration), '--', label='Линия тренда по валентности', color=trend_color)
                axs[0].set_title(f'Эмоциональный знак по заданию {TaskNumber + 1} респондента № {resp + 1}')

                axs[1].plot(duration, Inv, '-', color='#8B9BB3')
                axs[1].grid(True)
                axs[1].spines['top'].set_visible(False)
                axs[1].spines['right'].set_visible(False)
                axs[1].spines['bottom'].set_visible(False)
                axs[1].spines['left'].set_visible(False)

                trend_color = '#912D2D' if np.polyfit(list(duration), Inv, 1)[0] < 0 else '#2D9182'
                axs[1].plot(duration, TrendInvolvement(duration), '--', label='Линия тренда по вовлеченности', color=trend_color)
                axs[1].set_title(f'Вовлеченность по заданию {TaskNumber + 1} респондента № {resp + 1}')

                name = f'Задание {TaskNumber + 1}'
                filepath = os.path.join(directory, name)
                plt.savefig(filepath)
                logger.info(f"Saved plot for task {TaskNumber + 1} of respondent {resp + 1} to {filepath}")
                plt.show()

            resp += 1

        else:
            for taskNumber in range(N_task):
                fig, axs = plt.subplots(2, team, figsize=(10, 15))
                TaskNumber += 1

                for hero in range(team):
                    actualNumResp = hero + resp
                    logger.debug(f"Processing task {TaskNumber + 1} for respondent {actualNumResp + 1}")

                    try:
                        file = pd.read_excel(dfs[actualNumResp])
                        data = timings[actualNumResp]
                        Valency = file['Знак PPG']
                        Involvement = file['Сила SGR + PPG']
                    except Exception as e:
                        logger.error(f"Error reading Excel file for respondent {actualNumResp + 1}: {e}")
                        plt.close('all')
                        continue

                    time = data[TaskNumber]
                    Val = Valency[time[0] - 1:time[1]]
                    Inv = Involvement[time[0] - 1:time[1]]
                    duration = np.arange(time[0] - 1, time[1])

                    # Вычисление трендов
                    TrendValency = np.poly1d(np.polyfit(list(duration), Val, init_n_polynom(duration, npoly)))
                    TrendInvolvement = np.poly1d(np.polyfit(list(duration), Inv, init_n_polynom(duration, npoly)))

                    logger.debug(f"TrendValency coefficients: {TrendValency.coeffs}")
                    logger.debug(f"TrendInvolvement coefficients: {TrendInvolvement.coeffs}")

                    # Создание графиков
                    axs[0, hero].plot(duration, Val, color='#2D9182')
                    axs[0, hero].grid(True)
                    axs[0, hero].spines['top'].set_visible(False)
                    axs[0, hero].spines['right'].set_visible(False)
                    axs[0, hero].spines['bottom'].set_visible(False)
                    axs[0, hero].spines['left'].set_visible(False)

                    trend_color = '#912D2D' if np.polyfit(list(duration), Val, 1)[0] < 0 else '#2D9182'
                    axs[0, hero].plot(duration, TrendValency(duration), '--', label='Линия тренда по валентности', color=trend_color)
                    axs[0, hero].set_title(f'Эмоциональный знак по заданию {TaskNumber + 1} респондента № {actualNumResp + 1}')

                    axs[1, hero].plot(duration, Inv, '-', color='#8B9BB3')
                    axs[1, hero].grid(True)
                    axs[1, hero].spines['top'].set_visible(False)
                    axs[1, hero].spines['right'].set_visible(False)
                    axs[1, hero].spines['bottom'].set_visible(False)
                    axs[1, hero].spines['left'].set_visible(False)

                    trend_color = '#912D2D' if np.polyfit(list(duration), Inv, 1)[0] < 0 else '#2D9182'
                    axs[1, hero].plot(duration, TrendInvolvement(duration), '--', label='Линия тренда по вовлеченности', color=trend_color)
                    axs[1, hero].set_title(f'Вовлеченность по заданию {TaskNumber + 1} респондента № {actualNumResp + 1}')

                name = f'Задание {TaskNumber + 1}'
                filepath = os.path.join(directory, name)
                plt.savefig(filepath)
                logger.info(f"Saved plot for task {TaskNumber + 1} of respondents {resp + 1}-{resp + team} to {filepath}")
                plt.show()

            resp += team

    logger.info("Finished Building function")