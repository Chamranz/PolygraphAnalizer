import flet as ft
from ForOnes.ByHand.Handler import HandInsertion
import numpy as np
import pandas as pd
def AnalysisForOneRespondent(page, content):

    def choose_Handdata(e):
        HandData.value = True if HandData.value == False else False
        page.update()

    def choose_Loggerdata(e):
        LoggerData.value = True if LoggerData.value == False else False
        page.update()

    def choose_Exceldata(e):
        ExcelData.value = True if ExcelData.value == False else False
        page.update()

    def change_theme(e):
        page.theme_mode = 'light' if page.theme_mode == 'dark' else 'dark'
        page.update()

    def InsertData(e):
        print('go shorty')
        DataMode = np.array([HandData.value, LoggerData.value, ExcelData.value])
        if DataMode.sum()>1 or DataMode.sum()==0:
            page.snack_bar = ft.SnackBar(ft.Text('Пожалуйста, выберите один тип данных', font_family=MFont))
            page.snack_bar.open = True
            page.update()
        elif DataMode[0] == 1:
            print("it's your birthday")
            HandInsertion(page, content)

        elif DataMode[1] == 1:
            page.snack_bar = ft.SnackBar(ft.Text('Пока в разработке', font_family=MFont))
            page.snack_bar.open = True
            page.update()


    def Hover(e):
        page.bgcolor = ft.colors.PINK if e.data == "true" else "black"
        page.update()

    HandData = ft.Checkbox(value=False)
    LoggerData = ft.Checkbox(value=False)
    ExcelData = ft.Checkbox(value=False)
    MFont = 'montserrat'
    theme_button = ft.IconButton(ft.icons.SUNNY, on_click=change_theme)

    content.controls.extend([

            ft.Row([ft.Text(value='Анализ полиграфов', font_family=MFont)], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([ft.Text(value='Выберите имеющиеся у вас данные', font_family=MFont)],
                   alignment=ft.MainAxisAlignment.CENTER),

            ft.Row(
                [
                    HandData,
                    ft.TextButton(text='Есть тайминги по каждому заданию (вбивать вручную)', on_click=choose_Handdata)
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),

            ft.Row(
                [
                    LoggerData,
                    ft.TextButton(text='Есть тайминги с логгера (в разработке)', on_click=choose_Loggerdata)
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),

            ft.Row(
                [
                    ft.TextButton(text='Далее', on_click=InsertData),
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),

            ft.Row(
                [
                    ft.TextButton(text='Поменять тему', on_click=change_theme),
                    theme_button
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )])
    return content


