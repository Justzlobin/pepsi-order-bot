class UnMessage:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.dict_mess = {}

    def add_message(self, message_id):
        self.dict_mess['message_id'] = message_id
        self.dict_mess['chat_id'] = self.chat_id
        return self.dict_mess

    def dict_message(self):
        return self.dict_mess
