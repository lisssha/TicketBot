import psycopg2
from config import host, user, password, db_name
from dotenv import load_dotenv
import os
import logging
from threading import Lock, Thread
# надо ли связывать комментраий в таблице тикетов с комментарием в таблице комментариев, именно текст 
# я сделала выбор статуса задачи через enum, но мне кажется это бесполезно
# переписала на многопоточного одиночку примером был refractoring.guru
load_dotenv()
logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")

class SingletonMeta(type):
    _instances = {}
    _lock: Lock = Lock()
    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]
    
class DatabaseSingleton(metaclass=SingletonMeta):

    def __init__(self) -> None:
        #нужно ли изнчальное подключение брать за none или и так ок?
        self.init_db()
    

    def init_db(self):
        try:
            self.connection = psycopg2.connect(
                host=os.getenv("host"),
                user=os.getenv("user"),
                password=os.getenv("password"),
                database=os.getenv("db_name")
            )
            self.connection.autocommit = True
            with self.connection.cursor() as cursor:
                cursor.execute(
                     """DO $$
                     BEGIN
                        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'ticket_status') THEN 
                            CREATE TYPE ticket_status AS enum('Отправлено','В работе','Готово');
                        END IF;
                     END $$;"""
                )
                cursor.execute(
                    """CREATE TABLE IF NOT EXISTS Tickets(
                    id serial PRIMARY KEY,
                    contact_information VARCHAR,
                    complain_text VARCHAR NOT NULL,
                    status ticket_status DEFAULT 'Отправлено',
                    time_create TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    comment VARCHAR );"""
                    )
                cursor.execute(
                     """CREATE TABLE IF NOT EXISTS Admins(
                     id SERIAL PRIMARY KEY,
                     name VARCHAR,
                     login VARCHAR NOT NULL UNIQUE,
                     password VARCHAR NOT NULL
                     );"""
                    )
                cursor.execute(
                     """CREATE TABLE IF NOT EXISTS Comments(
                     id SERIAL PRIMARY KEY,
                     id_ticket INTEGER,
                     text_comment TEXT,
                     time_addition TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                     FOREIGN KEY (id_ticket) REFERENCES Tickets (id) ON DELETE CASCADE
                     );"""
                    )
        except Exception as _ex:
                logging.error(f"when working with the database: {_ex}")


    def get_connection(self):
        return self.connection
    
    # def insert_ticket(self,contact_information:str,complain_text:str):
    #     try:
    #         with self.connection.cursor() as cursor:
    #             query = """INSERT INTO Tickets (contact_information, complain_text)VALUES (%s, %s)"""
    #             cursor.execute(query, (contact_information, complain_text))
    #             print("данные сохранены")
    #     except Exception as _ex:
    #             print(f"ошибка при работе с бд: {_ex}")