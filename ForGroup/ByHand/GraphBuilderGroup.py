import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from cycler import cycler
import matplotlib as mpl
import os
from loguru import logger



LOGGING = 'logs.log'
FORMAT = "{time} {level} {message}"
@logger.catch
def init_n_polynom(x, npoly):
    if isinstance(npoly, int):
        return npoly+1
    else:
        return npoly(x)
def Building(dfs, timings, plot_number, N_resp, directory, N_task, npoly):
    #Проверим, является ли степень полинома заданным числом или он подбирается автоматически
    Resps= []
    resp = 0
    logger.add(LOGGING, format=FORMAT, rotation='1 MB')


    # Дизайн графиков
    #plt.style.use('fivethirtyeight')
    mpl.rcParams['axes.prop_cycle'] = cycler(color=['#163969', '#F87D00', '#8B9BB3'])
    mpl.rcParams['axes.linewidth'] = 1
    mpl.rcParams['lines.linewidth'] = 4
    mpl.rcParams['lines.solid_capstyle'] = 'butt'

    while N_resp / plot_number >= 1:
        N_resp -= plot_number
        Resps.append(plot_number)
    if N_task % plot_number != 0:
        Resps.append(N_task % plot_number)
    for team in Resps:
        TaskNumber = -1
        if team == 1:
            for taskNumber in range(len(timings)):
                fig, axs = plt.subplots(2, team, figsize=(10, 15))
                TaskNumber += 1

                file = pd.read_excel(dfs[resp])
                data = timings[resp]
                Valency = file['Знак PPG']
                Involvement = file['Сила SGR + PPG']
                time = data[TaskNumber]

                Val = Valency[time[0]-1:time[1]]
                Inv = Involvement[time[0]-1:time[1]]
                duration = np.arange(time[0]-1,time[1])

                # Станадартизация данных, что графики наложенных линни тренда совпадали с графиками выше

                TrendValency = np.poly1d(np.polyfit(list(duration), Val, init_n_polynom(duration, npoly)))
                TrendInvolvement = np.poly1d(np.polyfit(list(duration), Inv, init_n_polynom(duration, npoly)))
                #fig, axs = plt.subplots(2, N_resp, figsize=(10, 15))
                axs[0].plot(duration, Val, color='#2D9182')
                axs[0].grid(True)
                axs[0].spines['top'].set_visible(False)
                axs[0].spines['right'].set_visible(False)
                axs[0].spines['bottom'].set_visible(False)
                axs[0].spines['left'].set_visible(False)
                if np.polyfit(list(duration), Val, 1)[0]<0:
                    axs[0, resp].plot(duration, TrendValency(duration), '--', label='Линия тренда по валентности', color='#912D2D') #линия тренда для проверки
                else:
                    axs[0, resp].plot(duration, TrendValency(duration), '--', label='Линия тренда по валентности',
                                color='#2D9182')  # линия тренда для проверки
                axs[0, resp].set_title(f'Эмоциональный знак по заданию {TaskNumber+1} респондента № {resp+1}')

                axs[1].plot(duration, Inv, '-', color='#8B9BB3')
                axs[1].grid(True)
                axs[1].spines['top'].set_visible(False)
                axs[1].spines['right'].set_visible(False)
                axs[1].spines['bottom'].set_visible(False)
                axs[1].spines['left'].set_visible(False)
                if np.polyfit(list(duration), Inv, 1)[0] < 0:
                    axs[1].plot(duration, TrendInvolvement(duration), '--', label='Линия тренда по вовлеченности',
                                color='#912D2D')  # линия тренда для проверки
                else:
                    axs[1].plot(duration, TrendInvolvement(duration), '--', label='Линия тренда по вовлеченности',
                                color='#2D9182')  # линия тренда для проверки
                print(f'coef_polynom_involvemnt = {TrendInvolvement}')
                axs[1].set_title(f'Вовлеченность по заданию {TaskNumber+1} респондента № {resp+1}')


                # отдельные расчеты для наложенных
                #axs[2].plot(duration, Trend_Std_Val(duration), label='Линия тренда по эмоциональному знаку', color='#2D9182')
                #axs[2].plot(duration,  Trend_Std_Inv(duration), label='Линия тренда по вовлеченности', color='#8B9BB3')
                #axs[2].grid(True)
                #axs[2].spines['top'].set_visible(False)
                #axs[2].spines['right'].set_visible(False)
                #axs[2].spines['bottom'].set_visible(False)
                #axs[2].spines['left'].set_visible(False)
                #axs[2].set_title(f'Линии тренда по заданию {TaskNumber}')

                name = f'Задание {TaskNumber+1}'
                filepath = os.path.join(directory, name)
                plt.savefig(filepath)
                plt.show()
            resp+=1

        else:
            for taskNumber in range(len(timings)):
                fig, axs = plt.subplots(2, team, figsize=(10, 15))
                TaskNumber += 1
                for hero in range(team):
                    actualNumResp = hero+resp
                    file = pd.read_excel(dfs[actualNumResp])
                    data = timings[actualNumResp]
                    Valency = file['Знак PPG']
                    Involvement = file['Сила SGR + PPG']
                    time = data[TaskNumber]

                    Val = Valency[time[0] - 1:time[1]]
                    Inv = Involvement[time[0] - 1:time[1]]
                    duration = np.arange(time[0] - 1, time[1])

                    # Станадартизация данных, что графики наложенных линни тренда совпадали с графиками выше

                    TrendValency = np.poly1d(np.polyfit(list(duration), Val, init_n_polynom(duration, npoly)))
                    TrendInvolvement = np.poly1d(np.polyfit(list(duration), Inv, init_n_polynom(duration, npoly)))

                    # fig, axs = plt.subplots(2, N_resp, figsize=(10, 15))
                    axs[0, hero].plot(duration, Val, color='#2D9182')
                    axs[0, hero].grid(True)
                    axs[0, hero].spines['top'].set_visible(False)
                    axs[0, hero].spines['right'].set_visible(False)
                    axs[0, hero].spines['bottom'].set_visible(False)
                    axs[0, hero].spines['left'].set_visible(False)
                    if np.polyfit(list(duration), Val, 1)[0] < 0:
                        axs[0, hero].plot(duration, TrendValency(duration), '--', label='Линия тренда по валентности',
                                          color='#912D2D')  # линия тренда для проверки
                    else:
                        axs[0, hero].plot(duration, TrendValency(duration), '--', label='Линия тренда по валентности',
                                          color='#2D9182')  # линия тренда для проверки
                    axs[0, hero].set_title(f'Эмоциональный знак по заданию {TaskNumber + 1} респондента № {actualNumResp + 1}')

                    axs[1, hero].plot(duration, Inv, '-', color='#8B9BB3')
                    axs[1, hero].grid(True)
                    axs[1, hero].spines['top'].set_visible(False)
                    axs[1, hero].spines['right'].set_visible(False)
                    axs[1, hero].spines['bottom'].set_visible(False)
                    axs[1, hero].spines['left'].set_visible(False)
                    if np.polyfit(list(duration), Inv, 1)[0] < 0:
                        axs[1, hero].plot(duration, TrendInvolvement(duration), '--',
                                          label='Линия тренда по вовлеченности',
                                          color='#912D2D')  # линия тренда для проверки
                    else:
                        axs[1, hero].plot(duration, TrendInvolvement(duration), '--',
                                          label='Линия тренда по вовлеченности',
                                          color='#2D9182')  # линия тренда для проверки
                    axs[1, hero].set_title(f'Вовлеченность по заданию {TaskNumber + 1} респондента № {actualNumResp + 1}')

                    # отдельные расчеты для наложенных
                    # axs[2].plot(duration, Trend_Std_Val(duration), label='Линия тренда по эмоциональному знаку', color='#2D9182')
                    # axs[2].plot(duration,  Trend_Std_Inv(duration), label='Линия тренда по вовлеченности', color='#8B9BB3')
                    # axs[2].grid(True)
                    # axs[2].spines['top'].set_visible(False)
                    # axs[2].spines['right'].set_visible(False)
                    # axs[2].spines['bottom'].set_visible(False)
                    # axs[2].spines['left'].set_visible(False)
                    # axs[2].set_title(f'Линии тренда по заданию {TaskNumber}')

                    name = f'Задание {TaskNumber + 1}'
                    filepath = os.path.join(directory, name)
                    plt.savefig(filepath)

                plt.show()
            resp+=team