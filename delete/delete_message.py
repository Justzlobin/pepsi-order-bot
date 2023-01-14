class UnMessage:
    def __init__(self):
        self.dict_mess = {}
        self.dict_photo = {}

    def add(self, message_id):
        self.dict_mess['message_id'] = message_id

    def destr(self):
        return self.dict_mess['message_id']

    def add_photo(self, message_id):
        self.dict_photo['message_photo'] = message_id

    def destr_photo(self):
        return self.dict_photo['message_photo']