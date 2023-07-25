import psycopg2

def connection_to_database():
    # Подключение к базе данных
    database = "postgres"
    user = "postgres"
    password = "12345"
    host = "127.0.0.1"
    port = "5432"
    conn = psycopg2.connect(f'postgresql://{user}:{password}@{host}:{port}/{database}')
    cursor = conn.cursor()
    return (conn, cursor)

def close_connection(conn, cursor):
    # Закрытие соединения
    cursor.close()
    conn.close()

def find_employees(cursor, id):
    # Функция поиска сотрудников из одного офиса
    def get_name(id):
        # Получаем фамилию сотрудника/наименование отдела/офиса по id
        cursor.execute('SELECT Name FROM employees WHERE id=(%s)', (id, ))
        name = cursor.fetchone()
        if name is not None:
            name = name[0]
        return name

    def get_parentid(id):
        # Получаем родительский id записи по текущему id
        cursor.execute('SELECT ParentId FROM employees WHERE id=(%s)', (id, ))
        parentid = cursor.fetchone()
        if parentid is not None:
            parentid = parentid[0]
        return parentid

    def get_type(id):
        # Получаем тип записи по id
        cursor.execute('SELECT Type FROM employees WHERE id=(%s)', (id, ))
        type = cursor.fetchone()
        if type is not None:
            type = type[0]
        return type

    employees_names = []
    type = get_type(id)
    while type != 1:
        id = get_parentid(id)
        type = get_type(id)
    name = get_name(id)
    office_name = name
    id += 1
    type = get_type(id)
    while type != 1 and type is not None:
        if type == 3:
            name = get_name(id)
            employees_names.append(name)
        if id == 14:
            id = 16
        else:
            id += 1
        type = get_type(id)
    return (office_name, employees_names)

try:
    # Пытаемся подключиться к базе данных
    conn, cursor = connection_to_database()
    try:
        # Проверяем вводимое пользователем значение
        id = int(input("Введите идентификатор сотрудника: "))
        cursor.execute('SELECT * FROM employees WHERE id = (%s)', (id,))
        if cursor.fetchone() is None:
            print("Нет такого сотрудника")
        else:
            office_name, employeers_names = find_employees(cursor, id)
            print(office_name, end=": ")
            print(*employeers_names, sep=', ')
    except ValueError:
        # В случае нецелочисленного значения будет выведена ошибка
        print('Введено неверное значение')
    close_connection(conn, cursor)
except ImportError:
    # В случае сбоя подключения будет выведено сообщение
    print('Не установлено соединение с базой данных')