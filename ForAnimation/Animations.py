import flet as ft
import sqlite3
import pandas as pd
import numpy as np
from moviepy.editor import VideoFileClip
from ForAnimation.AnimeBuild import Build
def AnimatedPlots(page, content):

    def load_poly(e):
        if e.files:
            file_path = e.files[0].path
            try:
                global df
                df = pd.read_excel(file_path)
                DoneButton.disabled = False
                page.update()
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text('Выберите файл видеозаписи!', font_family=MFont))
                page.snack_bar.open = True
                page.update()

    def load_video(e):
        global Video
        if e.files:
            file_path = e.files[0].path
            try:
                Video = VideoFileClip(file_path)
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text('Выберите файл ECXEL!', font_family=MFont))
                page.snack_bar.open = True
                page.update()
                Video = 1
        else:
            Video = 1

    def change_theme(e):
        page.theme_mode = 'light' if page.theme_mode == 'dark' else 'dark'
        theme_button =  ft.IconButton(ft.icons.SHIELD_MOON, on_click=change_theme)
        page.update()

    def collect_data(e):
        start = []
        end = []
        for control in content.controls:
            if isinstance(control, ft.TextField):
                if "Начало" in control.label:
                    start.append(control.value)
                elif "Конец" in control.label:
                    end.append(control.value)
        data_time = np.array(list(zip(start, end)))
        Build(df, Video, data_time)

    #Video=None
    content = ft.Column()
    MFont = 'montserrat'
    theme_button = ft.IconButton(ft.icons.SUNNY, on_click=change_theme)

    global Video
    Video = 1

    poly_picker = ft.FilePicker(on_result=load_poly)
    upload_button_poly = ft.OutlinedButton(text='Загрузить файл с п', on_click=lambda e: poly_picker.pick_files())

    video_picker = ft.FilePicker(on_result=load_video)
    upload_button_video = ft.OutlinedButton(text='Загрузить видео (по желанию)', on_click=lambda e: video_picker.pick_files())

    DoneButton = ft.OutlinedButton(text='Сделать анимацию', on_click=collect_data,
                                   disabled=True)
    start_time = ft.TextField(label="Начало формирования (в секундах)")
    end_time = ft.TextField(label="Конец формирования (в секундах)")

    content.controls.extend([ft.Column(
        [
            ft.Row([ft.Text(value='Построение анимированных графиков', font_family=MFont)],
                   alignment=ft.MainAxisAlignment.CENTER)], alignment=ft.MainAxisAlignment.CENTER)])
    content.controls.append(start_time)
    content.controls.append(end_time)
    content.controls.extend([
            ft.Row([poly_picker, upload_button_poly], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([video_picker,upload_button_video], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([DoneButton],alignment=ft.MainAxisAlignment.CENTER),
            ft.Row(
                [
                    ft.TextButton(text='Поменять тему', on_click=change_theme),
                    theme_button
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )])
    return content
