# еще не думала
class Manager:
    def __init__(self) -> None:
        self.__buttons = [
            {'text': 'Создать заявку', 'answer': 'Заявка создана'}
        ]

    def answer(self, message_text):
        for button in self.__buttons:
            if message_text == button.text:
                return button.answer