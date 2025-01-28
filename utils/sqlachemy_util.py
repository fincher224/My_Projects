from sqlalchemy import select, create_engine, Table, column, INTEGER, String, MetaData, ForeignKey, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, ProgrammingError, OperationalError


class SQL:
    _engine = None                                                                              # переменная для хранения единственного экземпляра движка
    _Session = None                                                                             # переменная для хранения единственного экземпляра сессии

    @classmethod
    def get_engine(cls, bd):                                                                     # Метод для получения движка или "образа" БД
        if cls._engine is None:
            db_url = f'postgresql+psycopg2://postgres:zxasqw123qwaszx@localhost:5432/{bd}'
            cls._engine = create_engine(db_url, echo=False)
        return cls._engine

    @classmethod
    def get_session(cls, bd):  # Метод для получения сессии
        if cls._Session is None:
            engine = cls.get_engine(bd)
            cls._Session = sessionmaker(bind=engine)
        return cls._Session()

    @staticmethod
    def sql_query(bd, sql_query_text):
        try:
            session = SQL.get_session(bd)  # Запуск сессии для работы с БД
        except OperationalError as e:
            print(f"Не удалось подключиться к БД {bd}: {e}")
            return
        try:
            result_session = session.execute(
                text("SELECT pg_backend_pid() AS session_id"))  # sql запрос для получения Id сессии
            session_id = result_session.scalar()  # Этот метод возвращает первый элемент первой строки запроса
            print(f'\nУспешное подключение к БД {bd}')
            print(f"Идентификатор сессии: {session_id}")

            res = session.execute(text(sql_query_text))  # Сессия в которую помещается наш запрос
            result_list = res.fetchall()  # Используется для получения всех строк результата выполнения sql запроса
            result = [item for row in result_list for item in row]  # Распаковка кортежа и преобразование его в список

            if result:  # Условия при которых выводится результат
                assert True
                print(f'Результат запроса: {result}\n')
                return result
            else:
                assert False, 'Значение не найдено'
        except ProgrammingError as e:
            print(f"Ошибка в SQL-запросе: {e}")
        except SQLAlchemyError as e:
            print(f'\nОшибка выполнения SQL-запроса: {e}\n')
            return None
        finally:
            session.close()  # Закрытие сессии

    @staticmethod
    def sql_execute(bd, sql_query_text, params=None):
        try:
            session = SQL.get_session(bd)
        except OperationalError as e:
            print(f"Не удалось подключиться к БД {bd}: {e}")
            return None
        try:
            success = False
            result_session = session.execute(text("SELECT pg_backend_pid() AS session_id"))
            session_id = result_session.scalar()
            print(f'\nУспешное подключение к БД {bd}\nИдентификатор сессии: {session_id}')

            result = session.execute(text(sql_query_text), params)
            session.commit()
            success = True
            print(f'Запрос выполнен успешно: {sql_query_text}\n')

            return success
        except ProgrammingError as e:
            print(f"Ошибка в SQL-запросе: {e}")
        except SQLAlchemyError as e:
            print(f'\nОшибка выполнения SQL-запроса: {e}\n')
            return None
        finally:
            session.close()
