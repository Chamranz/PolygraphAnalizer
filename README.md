## Для перехода в ветку с проектом перейдите в ветку "master"
## Установка зависимостей

1. Создайте виртуальное окружение:
   ```bash
   python -m venv venv
2. Активирууйте виртуальное окружение
   venv\Scripts\activate
3. Установите зависимости
   pip install -r requirements.txt
   ## файл requirements.txt находится в ветке с проектом

## Запуск программы

1. Запустите проект
2. Запустите программу
   python Start.py
3. Немного подождите..

## Описание проекта

Это программа для анализа данных полиграфа. В сущности это уже обработанные психофизилогические данные, переведенные в метрики "эмоции", которые отображены в файле excel. 
Эмоции описываются двумя составляющими - вовлеченность и эмоциональный знак. Вовлеченность - грубо говоря, сила эмоции. Эмоциональный знак - ее модальность - говорит о том,
положительная у была эмоция или отрицательная. 
Важно понимать, что значение имеют не абсолютные показатели, а их динамика. Поэтому мы смотрим данные за некоторый промежуток времени и то, как они меняются. Например, 
если вовлеченность растет, а эмоциональный знак падает - значет были сильные отрицательные эмоции - гнев, разражение. По аналогии можно вывести все иные эмоции. Для описания
таких изменении обычно использутеся апроксимация линией тренде (полиномиальной функцией первой степени). Однако это не годится, когда у нас измеряется не эпизод в несколько десятков секунд,
а скажем, целый фильм. Тогда нужно апроксимировать полиномом более большой степени. Так или иначе это создает определенные трудности. В качестве решения я вывел наиболее подходящую формулу,
для определения степени этого полинома - ln(duration/10). Монотонно возрастающая функция с постепенным затуханием - то что нужно, чтобы степени полинома росла, но не слишком быстро (делим на 10 - это 
обусловлено скоростью проявления психофизиологических процессов).

Имеются функции как для анализа по нескольким заданиям/эпизодов для одного респондента, так идля сравнения разных респондентов по ряду задании/эпизодов. Также программа добавляет анимированные графики с 
динамически обновляющейся линией тренда за последние 5 секунд. Все примеры есть в ветке main.

Кажется все, если есть какие-то вопросы - пишите в тг @witcherbit :D

P.S. логин и пароль для входа - "1"
