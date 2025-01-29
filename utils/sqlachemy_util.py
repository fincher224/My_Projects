from sqlalchemy import select, create_engine, Table, column, INTEGER, String, MetaData, ForeignKey, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, ProgrammingError, OperationalError


class SQL:
    _engine = None
    _Session = None
    @classmethod
    def get_engine(cls, bd):
        if cls._engine is None:
            db_url = f'postgresql+psycopg2://postgres:zxasqw123qwaszx@localhost:5432/postgres'
            cls._engine = create_engine(db_url, echo=False)
        return cls._engine

    @classmethod
    def get_session(cls, bd):
        if cls._Session is None:
            engine = cls.get_engine(bd)
            cls._Session = sessionmaker(bind=engine)
        return cls._Session()

    @staticmethod
    def sql_query(bd, sql_query_text):
        try:
            session = SQL.get_session(bd)
        except OperationalError as e:
            print(f"Не удалось подключиться к БД {bd}: {e}")
            return
        try:
            result_session = session.execute(
                text("SELECT pg_backend_pid() AS session_id"))
            session_id = result_session.scalar()
            print(f'\nУспешное подключение к БД {bd}')
            print(f"Идентификатор сессии: {session_id}")

            res = session.execute(text(sql_query_text))
            result_list = res.fetchall()
            result = [item for row in result_list for item in row]

            if result:
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
            session.close()

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
