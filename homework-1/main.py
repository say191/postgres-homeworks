"""Скрипт для заполнения данными таблиц в БД Postgres."""
import psycopg2  # Импортируем библиотеку для работы с БД
import os  # Импортируем библиотеку для определения пути к необходимым файлам


def read_file(name_file):
    path = os.path.join(os.path.dirname(__file__), f"north_data/{name_file}")
    # Записываем путь к введенному файлу в переменную
    clean_data_list = []
    # Создаем пустой список, где будут храниться строки со всеми необходимыми значениями
    # из файла в чистом формате (т е без лишних ковычек и т.д)
    with open(path, 'r') as file:  # Открываем файл для чтения
        columns = len(file.readline().split(','))
        # Записываем в переменную число строк в файле
        # Это понадобиться в дальнейшем для создания условия
        # В данных условиях мы не можем строчки всех файлов разделить по (',"'),
        # из-за содержимого файла orders_data, где в середине колонок есть численные значения
        # Соответственно алгоритм деления строчки на значения в этом файле будет иным
        data = file.readlines()  # Считываем все строчки, введенного файла, и записываем их в переменную
        if columns != 5:  # Если чесло колонок в файле не равно 5 (исключаем файл orders_data)
            for line in data:  # Проходимся по каждой строчке
                list_data = line.strip().split(',"')
                # Отсекаем от строчки лишние знаки и символы (например '/n')
                # с помощью метода strip() и делим строчку на значения
                list_elements = []  # Создаем пустой список из элементов строчки
                for element in list_data:  # Проходимся по каждому элементу
                    list_elements.append(element.strip('"'))
                    # Отсекаем от каждого элемента лишние знаки ('"') и
                    # добавляем "чистый элемент" в список
                clean_data_list.append(list_elements)
                # Добавляем в список все строчки со всеми значениями (элементами)
                # в чистом формате (без лишних ковычек)
        else:  # В ином случае
            for line in data:  # Так же проходимся по всем строчкам
                list_data = line.strip().split(',')  # Разбиваем каждую строчку на элементы уже по запятым
                list_elements = []  # Создаем пустой список из элементов строчки
                for element in list_data:  # Проходимся по каждому элементу
                    list_elements.append(element.strip('"'))
                    # Отсекаем от каждого элемента лишние знаки ('"') и
                    # добавляем "чистый элемент" в список
                clean_data_list.append(list_elements)
                # Добавляем в список все строчки со всеми значениями (элементами)
                # в чистом формате (без лишних ковычек)
    return clean_data_list  # Возвращаем список из строчек со значениями


"""
Функция служит для чтения информации из файла и преобразования его в словарь, для
дальнейшего удобства работы с информацией. 
Т к с файла мы можем прочитать информацию только целиком или построчно, то необходимо 
провести ряд малипуляций. Вся сложность заключается в файле employees_data.csv.
Из-за которого мы не можем разбить строчку на значения по запятым, т к в файле
есть колонка notes, где находится текст, в котором могут быть запятые.
"""

with psycopg2.connect(
        host="localhost",
        database="north",
        user="postgres",
        password="sayMe123"
) as conn:  # Создаем переменную соединения с выбранными параметрами
    with conn.cursor() as cur:  # Создаем переменную курсора
        for value in read_file('customers_data.csv'):  # Проходимся по списку со значениями
            cur.execute('INSERT INTO customers VALUES (%s, %s, %s)',
                        (value[0], value[1], value[2]))  # Записываем значения в таблицу
        for value in read_file('employees_data.csv'):
            cur.execute("INSERT INTO employees VALUES (%s, %s, %s, %s, %s, %s)",
                        (value[0], value[1], value[2], value[3], value[4], value[5]))
        for value in read_file('orders_data.csv'):
            cur.execute("INSERT INTO orders VALUES (%s, %s, %s, %s, %s)",
                        (value[0], value[1], value[2], value[3], value[4]))
conn.close()  # Закрываем соединение
