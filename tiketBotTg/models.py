from __future__ import annotations
from datetime import datetime
import logging
from databaseSingleton import DatabaseSingleton


class Ticket:
    def __init__(self, contact_information: str, complain_text: str, status: str='Отправлено', time_create:datetime=None, comment: str=None) -> None:
        self.contact_information = contact_information
        self.complain_text = complain_text
        self.status=status
        self.time_create=time_create if time_create is not None else datetime.now()
        self.comment=comment
        

    @staticmethod
    def all() -> list[Ticket]:
        connect = DatabaseSingleton().get_connection()
        try:
            with connect.cursor() as cursor:
                cursor.execute("""SELECT contact_information, complain_text, status, time_create, comment FROM Tickets;""")
                tickets =cursor.fetchall()
        except Exception as _ex:
            logging.error(f" when receiving tickets from the database: {_ex}")

        result: list[Ticket] = []
        for row in tickets:
            #или лучше было заполнять contact_information=row[0]?
            result.append(Ticket(row[0], row[1],row[2],row[3],row[4]))
        return result
    

    @staticmethod
    def get(id: int = None)-> 'Ticket':
        connect = DatabaseSingleton().get_connection()
        try:
            with connect.cursor() as cursor:
                cursor.execute("""SELECT contact_information, complain_text, status, time_create, comment FROM Tickets WHERE id=%s;""",(id,))
                ticket_row =cursor.fetchone()
        except Exception as _ex:
            logging.error(f"when receiving a ticket by id from the database: {_ex}")

        if ticket_row:
            ticket= Ticket(ticket_row[0], ticket_row[1], ticket_row[2], ticket_row[3], ticket_row[4])
        else:
            logging.error(f"no ticket with id:{id} ")
            return None
        return ticket
    
    # другие параметры здесь не нужны, вроде
    @staticmethod
    def insert(contact_information: str, complain_text: str ):
        connect = DatabaseSingleton().get_connection()
        try:
            with connect.cursor() as cursor:
                query = """INSERT INTO Tickets (contact_information, complain_text)VALUES (%s, %s)"""
                cursor.execute(query, (contact_information, complain_text))
                logging.info("The data is saved")
                #вроде ничего возвращать не надо
        except Exception as _ex:
            logging.error(f"when adding a ticket: {_ex}")   
    

tickets = Ticket.all()
#выводить все можно адекватно через фор а то так <__main__.Ticket object at 0x00000288B197CB50>
print(tickets)
ticket=Ticket.get(1)
print(ticket.complain_text)