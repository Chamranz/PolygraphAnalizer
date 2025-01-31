import flet as ft
import numpy as np
import pandas as pd
from ForOnes.ByHand.GraphBuild import Building

def HandInsertion(page, content):

    def back(e):
        if previous_state_1:
            content.controls = previous_state_1.pop()  # Восстанавливаем предыдущее состояние
            page.update()

    def load_file(e):
        if e.files:
            file_path = e.files[0].path
            try:
                global df
                df = pd.read_excel(file_path)
                NextButton.disabled = False
                page.update()
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text('Выберите файл ECXEL!', font_family=MFont))
                page.snack_bar.open = True
                page.update()

    def next_page(e):
        if auto_n_polunom.value == True:
            npolynom = lambda x: round(np.log(len(x)/10))
        else:
            if N_polynom.value != '':
                npolynom = round(int(N_polynom.value))
            else:
                npolynom = 0
        if N_Task.value == '':
            page.snack_bar = ft.SnackBar(ft.Text('Введите количество заданий/эпизодов!', font_family=MFont))
            page.snack_bar.open = True
            page.update()
        else:
            if plot_number.value == '':
                TimeInsertion(page, content, int(N_Task.value), df, plot_number = 1, time_type=time_type.value, npoly=npolynom)
            else:
                if int(plot_number.value) > int(N_Task.value):
                    page.snack_bar = ft.SnackBar(ft.Text('Количество графиков не должно превышать количество заданий!', font_family=MFont))
                    page.snack_bar.open = True
                    page.update()
                else:
                    TimeInsertion(page, content, int(N_Task.value), df, plot_number=int(plot_number.value), time_type=time_type.value, npoly=npolynom)

    # Добавляем объекты-переменные на страницу
    MFont = 'monterrat'
    selected_directory = ""
    previous_state_1 =[]
    previous_state_1.append(content.controls.copy())
    N_Task = ft.TextField(label='Введие количество заданий/эпизодов', keyboard_type=ft.KeyboardType.NUMBER)
    plot_number = ft.TextField(label='Введите количество графиков, выводимых на одной картинке (по умолчанию 1)', keyboard_type=ft.KeyboardType.NUMBER)
    N_polynom = ft.TextField(label='Введите количество волн, которым будет описано распределение данных (по умолчанию 0 - линия тренда)',
                               keyboard_type=ft.KeyboardType.NUMBER)
    auto_n_polunom = ft.Checkbox(value=False)
    file_picker = ft.FilePicker(on_result=load_file)
    upload_button = ft.OutlinedButton(text='Загрузить файл с полиграфом', on_click=lambda e: file_picker.pick_files())
    time_type = ft.Checkbox(value=False)
    NextButton = ft.OutlinedButton(text='Далее', on_click=next_page, disabled=True)
    content.controls.clear()
    content.controls.extend([ft.Column([
        ft.Row([
            N_Task,plot_number, ft.Column([N_polynom, ft.Row([ft.Text(value='Автоматически определить опитмальное количество волн', font_family=MFont), auto_n_polunom])])], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([
            file_picker, upload_button
        ], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(
            [ft.Text(value='Формат ввода таймингов в минутах мм:сс (по умолчанию в секундах)', font_family=MFont),
             time_type], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([
            ft.OutlinedButton(text='Назад', on_click=back),
            NextButton], alignment=ft.MainAxisAlignment.CENTER)])])
    page.update()

def TimeInsertion(page, content, n_task, df, plot_number=1, time_type=None, npoly=0):

    def back(e):
        if previous_state_2:
            content.controls = previous_state_2.pop()  # Восстанавливаем предыдущее состояние
            page.update()

    def get_path(e: ft.FilePickerResultEvent):
        global directory
        directory = e.path
        done_button.disabled = False
        page.update()

    def collect_data(e):
        start = []
        end = []
        if time_type == True:
            for control in content.controls:
                if isinstance(control, ft.TextField):
                    if "Время начала" in control.label:
                        time = control.value
                        minutes, seconds = map(int, time.split(':'))
                        tot_sec = minutes * 60 + seconds
                        start.append(tot_sec)
                    elif "Время конца" in control.label:
                        time = control.value
                        minutes, seconds = map(int, time.split(':'))
                        tot_sec = minutes * 60 + seconds
                        end.append(tot_sec)
        else:
            for control in content.controls:
                if isinstance(control, ft.TextField):
                    if "Время начала" in control.label:
                        start.append(int(control.value))
                    elif "Время конца" in control.label:
                        end.append(int(control.value))
        data_time = np.array(list(zip(start, end)))
        Building(df, data_time, PN, directory, n_task, npoly)

    PN = plot_number
    MFont = 'monterrat'
    previous_state_2 = []
    previous_state_2.append(content.controls.copy())
    save_directory = ft.FilePicker(on_result=get_path)
    choose_directory = ft.OutlinedButton(text='Выбрать папку для сохранения', on_click=lambda e: save_directory.get_directory_path())
    done_button = ft.OutlinedButton(text='Готово', on_click=collect_data, disabled=True)
    content.controls.clear()

    for task in range(n_task):
        start_time = ft.TextField(label=f"Задание {task + 1} - Время начала")
        end_time = ft.TextField(label=f"Задание {task + 1} - Время конца")
        content.controls.append(start_time)
        content.controls.append(end_time)
    content.controls.extend([ft.Row([
        ft.Row([save_directory, choose_directory], alignment=ft.MainAxisAlignment.CENTER),
        ft.OutlinedButton(text='Назад', on_click=back),
        done_button
    ], alignment=ft.MainAxisAlignment.CENTER)])
    page.update()