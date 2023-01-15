

class UnMessage:
    def __init__(self):
        self.dict_mess = {}
        self.dict_photo = {}
        self.dict_chat = {}

    def add(self, message_id, chat_id):
        self.dict_mess['message_id'] = message_id
        self.dict_chat['chat_id'] = chat_id

    def destr(self, chat_id):
        if chat_id == self.dict_chat['chat_id']:
            return self.dict_mess['message_id']
        else:
            pass

    def add_photo(self, message_id, chat_id):
        self.dict_photo['message_photo'] = message_id
        self.dict_chat['chat_id'] = chat_id

    def destr_photo(self, chat_id):
        if chat_id == self.dict_chat['chat_id']:
            return self.dict_mess['message_photo']
        else:
            pass
