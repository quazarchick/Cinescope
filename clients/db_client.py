import psycopg2
from resources.db_creds import DatabaseCreds

def connect_to_postgres():
    connection = None
    cursor = None

    try:
        connection = psycopg2.connect(
            dbname = "db_movies",
            user = DatabaseCreds.USER,
            password = DatabaseCreds.PASSWORD,
            host = "80.90.191.123",
            port = "31200"
        )

        print("Подключение успешно установлено")

        cursor = connection.cursor()

        print("Информация о сервере:")
        print(connection.get_dsn_parameters(), "\n")

        cursor.execute("SELECT version();")

        record = cursor.fetchone()
        print("Вы подключены к - ", record, "\n")
    except Exception as error:
        print("Ошибка при работе с базой:", error)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("Соединение закрыто")

if __name__ == "__main__":
    connect_to_postgres()