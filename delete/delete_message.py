class UnMessage:
    def __init__(self):
        self.dict_mess = {}

    def mess(self, message_id):
        self.dict_mess['message_id'] = message_id
        return self.dict_mess
