import flet as ft
import numpy as np

def main(page: ft.Page):
    task_count_input = ft.TextField(label="Введите количество заданий", keyboard_type=ft.KeyboardType.NUMBER)
    create_button = ft.TextButton(text="Создать поля для ввода", on_click=lambda e: create_input_fields(int(task_count_input.value)))
    task_inputs = ft.Column()  # Колонка для динамически создаваемых полей

    def create_input_fields(task_count):
        task_inputs.controls.clear()  # Очистить предыдущие поля
        for i in range(task_count):
            start_time = ft.TextField(label=f"Задание {i + 1} - Время начала")
            end_time = ft.TextField(label=f"Задание {i + 1} - Время конца")
            task_inputs.controls.append(start_time)
            task_inputs.controls.append(end_time)
        task_inputs.controls.append(ft.TextButton(text="Собрать данные", on_click=collect_data))  # Кнопка для сбора данных
        page.update()

    def collect_data(e):
        start_times = []
        end_times = []
        for control in task_inputs.controls:
            if isinstance(control, ft.TextField):
                if "Время начала" in control.label:
                    start_times.append(control.value)
                elif "Время конца" in control.label:
                    end_times.append(control.value)

        # Создание матрицы NumPy
        data_matrix = np.array(list(zip(start_times, end_times)))
        print(data_matrix)  # Вывод матрицы в консоль (или используйте по вашему усмотрению)

    page.add(task_count_input, create_button, task_inputs)

ft.app(target=main)