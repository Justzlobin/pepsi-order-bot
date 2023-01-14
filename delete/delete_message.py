class UnMessage:
    def __init__(self):
        self.dict_mess = {}

    def add(self, message_id):
        self.dict_mess['message_id'] = message_id

    def destr(self):
        return self.dict_mess['message_id']
