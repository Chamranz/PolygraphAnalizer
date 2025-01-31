import flet as ft
import sqlite3
import numpy as np
from ForGroup.ByHand.HandlerGroup import HandInsertion
def AnalysisForGroup(page, content):

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
        theme_button =  ft.IconButton(ft.icons.SHIELD_MOON, on_click=change_theme)
        page.update()


    def InsertData(e):
        DataMode = np.array([HandData.value, LoggerData.value, ExcelData.value])
        if DataMode.sum()>1 or DataMode.sum()==0:
            page.snack_bar = ft.SnackBar(ft.Text('Пожалуйста, выберите один тип данных', font_family=MFont))
            page.snack_bar.open = True
            page.update()
        elif DataMode[0] == 1:
            HandInsertion(page, content)

        elif DataMode[1] == 1:
            page.snack_bar = ft.SnackBar(ft.Text('Пока в разработке', font_family=MFont))
            page.snack_bar.open = True
            page.update()

    HandData = ft.Checkbox(value=False)
    LoggerData = ft.Checkbox(value=False)
    ExcelData = ft.Checkbox(value=False)
    MFont = 'montserrat'
    theme_button = ft.IconButton(ft.icons.SUNNY, on_click=change_theme)

    content.controls.extend(
        [
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
                    ExcelData,
                    ft.TextButton(text='Есть тайминги с таблицы excel', on_click=choose_Exceldata)
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
