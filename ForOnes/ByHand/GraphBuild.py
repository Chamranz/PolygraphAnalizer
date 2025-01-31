import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from cycler import cycler
import matplotlib as mpl
import os

def init_n_polynom(x, npoly):
    if isinstance(npoly, int):
        return npoly+1
    else:
        print('chacl poly func = ', npoly(x))
        return npoly(x)
def Building(file, data, plot_number, directory, N_task, npoly):
    #Проверим, является ли степень полинома заданным числом или он подбирается автоматически
    print('primaly power poly = ', npoly)
    Valency = file['Знак PPG']
    Involvement = file['Сила SGR + PPG']
    Tasks = []
    TaskNumber = -1

    # Дизайн графиков
    #plt.style.use('fivethirtyeight')
    mpl.rcParams['axes.prop_cycle'] = cycler(color=['#163969', '#F87D00', '#8B9BB3'])
    mpl.rcParams['axes.linewidth'] = 1
    mpl.rcParams['lines.linewidth'] = 4
    mpl.rcParams['lines.solid_capstyle'] = 'butt'

    while N_task / plot_number >= 1:
        N_task -= plot_number
        Tasks.append(plot_number)
    if N_task % plot_number != 0:
        Tasks.append(N_task % plot_number)
    for team in Tasks:
        if team == 1 :

            TaskNumber += 1
            time = data[TaskNumber]

            Val = Valency[time[0]-1:time[1]]
            Inv = Involvement[time[0]-1:time[1]]
            duration = np.arange(time[0]-1,time[1])
            print(f'Val = {len(Val)}, duration = {len(duration)}')

            # Станадартизация данных, что графики наложенных линни тренда совпадали с графиками выше

            TrendValency = np.poly1d(np.polyfit(list(duration), Val, init_n_polynom(duration, npoly)))
            print('poly power valency',init_n_polynom(duration, npoly))# Для проверки
            TrendInvolvement = np.poly1d(np.polyfit(list(duration), Inv, init_n_polynom(duration, npoly)))
            print('poly power involvement',init_n_polynom(duration, npoly))
            fig, axs = plt.subplots(2, 1, figsize=(10, 15))
            axs[0].plot(duration, Val, color='#2D9182')
            axs[0].grid(True)
            axs[0].spines['top'].set_visible(False)
            axs[0].spines['right'].set_visible(False)
            axs[0].spines['bottom'].set_visible(False)
            axs[0].spines['left'].set_visible(False)
            if np.polyfit(list(duration), Val, 1)[0]<0:
                axs[0].plot(duration, TrendValency(duration), '--', label='Линия тренда по валентности', color='#912D2D') #линия тренда для проверки
            else:
                axs[0].plot(duration, TrendValency(duration), '--', label='Линия тренда по валентности',
                            color='#2D9182')  # линия тренда для проверки
            axs[0].set_title(f'Эмоциональный знак по заданию {TaskNumber}')

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
            axs[1].set_title(f'Вовлеченность по заданию {TaskNumber}')


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
        else:
            tasks_per_page = team
            fig, axs = plt.subplots(2, tasks_per_page, figsize=(10, 15))
            for task in range(team):
                # Расчеты
                TaskNumber += 1
                time = data[TaskNumber]

                duration = np.arange(time[0] - 1, time[1])
                Val = Valency[time[0] - 1:time[1]]
                Inv = Involvement[time[0] - 1:time[1]]


                TrendValency = np.poly1d(np.polyfit(duration, Val, init_n_polynom(duration, npoly)))
                TrendInvolvement = np.poly1d(np.polyfit(duration, Inv, init_n_polynom(duration, npoly)))

                axs[0, task].plot(duration, Val, color='#2D9182')
                axs[0, task].grid(True)
                axs[0, task].spines['top'].set_visible(False)
                axs[0, task].spines['right'].set_visible(False)
                axs[0, task].spines['bottom'].set_visible(False)
                axs[0, task].spines['left'].set_visible(False)
                if np.polyfit(list(duration), Val, 1)[0] < 0:
                    axs[0, task].plot(duration, TrendValency(duration), '--', label='Линия тренда по валентности',
                                color='#912D2D')  # линия тренда для проверки
                else:
                    axs[0, task].plot(duration, TrendValency(duration), '--', label='Линия тренда по валентности',
                                      color='#2D9182')  # линия тренда для проверки
                axs[0, task].set_title(f'Эмоциональный знак по заданию {TaskNumber}')

                axs[1, task].plot(duration, Inv, '-', color='#8B9BB3')
                axs[1, task].grid(True)
                axs[1, task].spines['top'].set_visible(False)
                axs[1, task].spines['right'].set_visible(False)
                axs[1, task].spines['bottom'].set_visible(False)
                axs[1, task].spines['left'].set_visible(False)
                if np.polyfit(list(duration), Inv, 1)[0] < 0:
                    axs[1, task].plot(duration, TrendInvolvement(duration), '--', label='Линия тренда по валентности',
                                      color='#912D2D')  # линия тренда для проверки
                else:
                    axs[1, task].plot(duration, TrendInvolvement(duration), '--', label='Линия тренда по валентности',
                                      color='#2D9182')  # линия тренда для проверки
                axs[1, task].set_title(f'Вовлеченность по заданию {TaskNumber}')


                # отдельные расчеты для наложенных

                #axs[2, task].plot(duration, TrendValency(duration), label='Линия тренда по валентности')
                #axs[2, task].plot(duration, TrendInvolvement(duration), label='Линия тренда по вовлеченности')
                #axs[2, task].grid(True)
                #axs[2, task].spines['top'].set_visible(False)
                #axs[2, task].spines['right'].set_visible(False)
                #axs[2, task].spines['bottom'].set_visible(False)
                #axs[2, task].spines['left'].set_visible(False)
                #axs[2, task].set_title(f'Линии тренда по заданию {TaskNumber}')

    plt.show()
