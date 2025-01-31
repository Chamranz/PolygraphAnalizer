import flet as ft
import sqlite3
from ForOnes.One import AnalysisForOneRespondent
from ForGroup.Group import AnalysisForGroup
from ForAnimation.Animations import AnimatedPlots
from ForTest.tab2 import tab1_content


def main(page: ft.Page):

    # Main properties
    page.title = 'Polygraph'
    page.theme_mode = 'dark'
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.vertical_alignment_alignment = ft.MainAxisAlignment.CENTER
    MFont = 'Montserrat'

    Content_one = ft.Column()
    One = ft.Tab(text="Анализ для одного респондента", content=AnalysisForOneRespondent(page, Content_one))

    Content_group = ft.Column()
    Group = ft.Tab(text="Анализ группы респондентов", content=AnalysisForGroup(page, Content_group))

    Content_Anim = ft.Column()
    Animations = ft.Tab(text="Анимированные графики", content=AnimatedPlots(page, Content_Anim))

    Content_test = ft.Column()
    Test = ft.Tab(text = 'Тестовая вкладка', content=tab1_content(page, Content_test))
    tabs = ft.Tabs(tabs=[One, Group, Animations, Test])

    #functions

    def auth_user(e):
        db = sqlite3.connect('DataBase')

        cur = db.cursor()
        cur.execute(f"SELECT * FROM users WHERE login = '{user_login.value}' AND pass = '{user_pass.value}'")
        if cur.fetchone()!=None:
            page.clean()
            page.add(tabs)
            page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text('Неправильные данные', font_family=MFont))
            page.snack_bar.open = True
            page.update()
        db.commit()
        db.close()
        page.update()

    def to_register(e):
        db = sqlite3.connect('DataBase')

        cur = db.cursor()
        cur.execute(f"SELECT * FROM superusers WHERE login = '{user_login.value}' AND pass = '{user_pass.value}'")
        if cur.fetchone()!=None:
            db.close()
            page.clean()
            page.add(panel_register)
            user_login.value = ''
            user_pass.value = ''
            page.update()

        else:
            page.snack_bar = ft.SnackBar(ft.Text('Это может делать только Камран и новый сисадмин', font_family=MFont))
            page.snack_bar.open = True
            page.update()

    def register(e):
        db = sqlite3.connect('DataBase')

        cur = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    login TEXT,
                    pass TEXT
                    )""")
        cur.execute(f"INSERT INTO users VALUES(NULL, '{user_login.value}','{user_pass.value}')")
        db.commit()
        db.close()

        user_login.value = ''
        user_pass.value = ''
        btn_reg.text = 'Добавлен пользователь'
        page.clean()
        page.add(panel_auth)
        page.update()

    def validate(e):
        if all([user_login.value, user_pass.value]):
            btn_reg.disabled = False
            btn_auth.disabled = False
            btn_to_reg.disabled = False
        else:
            btn_reg.disabled = True
            btn_auth.disabled = True
            btn_to_reg.disabled = True
        page.update()

    user_login = ft.TextField(label='Логин', width=200, on_change=validate)
    user_pass = ft.TextField(label='Пароль', password=True, width=200, on_change=validate)
    btn_reg = ft.OutlinedButton(text='Добавить', width=200, on_click=register, disabled=True)
    btn_auth = ft.OutlinedButton(text='Войти', width=200, on_click=auth_user, disabled=True)
    btn_to_reg = ft.OutlinedButton(text='Регистрация', width=200, on_click=to_register, disabled=True)

    panel_register = ft.Row(
        [
            ft.Column(
                [
                    user_login,
                    user_pass,
                    btn_reg,
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
    ], alignment=ft.MainAxisAlignment.CENTER)

    panel_auth = ft.Row(
        [
            ft.Column(
                [
                    user_login,
                    user_pass,
                    btn_auth,
                    btn_to_reg,
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
    ], alignment=ft.MainAxisAlignment.CENTER)

    page.add(panel_auth)


Page_menu = ft.app(target=main)
