import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, ArtistAnimation
import matplotlib.animation as animation
import numpy as np
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip
from matplotlib import style
from PIL import Image


def Build(df,Video, timings):

    # Приводим данные
    timings = timings[0]
    t1, t2 = map(int, timings)
    timings[0] = t1
    timings[1] = t2
    involvement = np.array(df['Сила SGR + PPG'])
    involvement = involvement[int(timings[0]):int(timings[1])]
    involvement = np.concatenate((np.zeros(5), involvement))
    Sign = np.array(df['Знак PPG'])
    Sign = Sign[int(timings[0]):int(timings[1])]
    Sign = np.concatenate((np.zeros(5), Sign))

    Seconds = np.arange(0,len(Sign),1)
    total_seconds = len(Seconds)
    window_size = 10  # Размер окна в секундах
    midpoint = window_size // 2  # Центр окна

    # Настройка графика
    plt.style.use('fivethirtyeight')
    fig = plt.figure(figsize=(10, 6)) # Размер графика
    ax = fig.add_subplot(2,1,1)
    ax2 = fig.add_subplot(2,1,2)

    line, = ax.plot([], [], label = 'График вовлеченности')
    trendline, = ax.plot([], [], alpha=0.8, label = 'Линия тренда')

    # Настройка по вовлеченности
    vline = ax.axvline(x=midpoint, label='Текущий момент', alpha=0.7)  # Вертикальная линия посередине

    ax.set_xlim(0, window_size)
    ax.set_ylim(0, 6)
    ax.set_xlabel('Время (секунды)', fontsize=14)
    ax.set_ylabel('Вовлеченность', fontsize=14)
    ax.set_title('График вовлеченности', fontsize=16, fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.7)  # Сетка
    ax.tick_params(axis='both', which='major', labelsize=12)  # Размер меток
    ax.legend()  # Легенда

    x = np.arange(0, min(0 + window_size, total_seconds))
    y = involvement[0:0 + window_size]
    trend = np.polyfit(x[:6], y[:6], 1)

    # Сглаженные линии----------------------------------------------------------------
    line2, = ax2.plot([], [], label='График вовлеченности')
    trendline2, = ax2.plot([], [], alpha=0.8, label='Линия тренда')

    # Настройка по валентности

    vline2 = ax2.axvline(x=midpoint, label='Текущий момент', alpha=0.7)  # Вертикальная линия посередине

    ax2.set_xlim(0, window_size)
    ax2.set_ylim(0, 250)
    ax2.set_xlabel('Время (секунды)', fontsize=14)
    ax2.set_ylabel('Вовлеченность', fontsize=14)
    ax2.set_title('График эмоционального знака (валентности)', fontsize=16, fontweight='bold')
    ax2.grid(True, linestyle='--', alpha=0.7)  # Сетка
    ax2.tick_params(axis='both', which='major', labelsize=12)  # Размер меток
    ax2.legend()  # Легенда

    x2 = np.arange(0, min(0 + window_size, total_seconds))
    y2 = involvement[0:0 + window_size]
    trend2 = np.polyfit(x[:6], y[:6], 1)
    trendpoly2 = np.poly1d(trend)

    def init():
        line.set_data([], [])
        trendline.set_data([],[])
        line2.set_data([], [])
        trendline2.set_data([], [])
        return line, trendline, line2, trendline2

    # Функция обновления
    def update(frame):
        if frame < total_seconds:
            x = np.arange(frame, min(frame + window_size, total_seconds))
            y = involvement[frame:frame + window_size]
            line.set_data(x, y)  # Сдвигаем график
            # Обновление меток на оси X
            ax.set_xlim(frame, frame + window_size)
            ax.set_ylim(y.min(), y.max())

            trend = np.polyfit(x[:6], y[:6],1)
            trendpoly = np.poly1d(trend)
            trendline.set_data(x[:6], trendpoly(x[:6]))


            vline.set_xdata([frame + midpoint, frame + midpoint])

            x2 = np.arange(frame, min(frame + window_size, total_seconds))
            y2 = Sign[frame:frame + window_size]
            line2.set_data(x2, y2)  # Сдвигаем график
            # Обновление меток на оси X
            ax2.set_xlim(frame, frame + window_size)
            ax2.set_ylim(y2.min(), y2.max())
            trend2 = np.polyfit(x2[:6], y2[:6], 1)
            trendpoly2 = np.poly1d(trend2)
            trendline2.set_data(x2[:6], trendpoly2(x2[:6]))

            vline2.set_xdata([frame + midpoint, frame + midpoint])

        return line, line2


    # Создание анимации
    ani = FuncAnimation(fig, update, frames=total_seconds, init_func=init, blit=False, interval=1000)

    # Сохранение анимации в видеофайл
    writergif = animation.PillowWriter(fps=1)
    ani.save('animation.gif', writer=writergif)

    if Video!=1:
        print('Процесс запущен')
        video = Video

        gif = VideoFileClip("animation.gif")
        gif = gif.resize(0.6)
        # Получаем длину GIF
        gif_duration = gif.duration
        # Обрезаем видео до длины GIF
        video = video.subclip(0, gif_duration)

        # Установка положения наложения (например, в правом нижнем углу)
        gif = gif.set_position(("right", "bottom")).set_opacity(0.8)

        # Создание композитного видео с наложением GIF
        final_video = CompositeVideoClip([video, gif])

        # Сохранение итогового видео
        final_video.write_videofile("Сканпасс с полиграфом.mp4", codec="libx264")
    else:
        print("Видео не загружено")