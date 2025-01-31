import flet as ft

def tab1_content(page, content):

    previous_state = []  # Список для хранения предыдущих состояний
    huy = ft.TextField()
    def delete(e):
        content.controls.clear()
        page.update()

    def change_color(e):
        page.bgcolor = huy.value
        page.update()

    def clear_content(e):
        previous_state.append(content.controls.copy())  # Сохраняем текущее состояние
        content.controls.clear()  # Очищаем содержимое
        content.controls.extend([
            ft.Text("Содержимое очищено."),
            ft.TextButton("Назад", on_click=restore_content)  # Кнопка "Назад"
        ])
        page.update()

    def restore_content(e):
        if previous_state:
            content.controls = previous_state.pop()  # Восстанавливаем предыдущее состояние
            page.update()

    # Изначальное содержимое
    content.controls.extend([
        ft.TextButton('delete everythng', on_click=delete),
        ft.Text("Содержимое вкладки 1"),
        ft.TextButton("Изменить цвет фона на синий", on_click=change_color),
        ft.TextButton("Очистить содержимое", on_click=clear_content),
        huy
    ])

    return content