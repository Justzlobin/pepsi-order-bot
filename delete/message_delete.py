class Count:

    def __init__(self):
        self.count_list = []
        self.chat_dict = {}
        self.uns_list = []
        self.photo_dict = {}
        self.photo_list = []

    def add_message(self, chat_id, message_id):
        self.count_list.append(message_id)
        self.chat_dict = {chat_id: self.count_list}
        return self.chat_dict

    def add_message_photo(self, chat_id, message_id):
        self.photo_list.append(message_id)
        self.photo_dict[chat_id] = self.photo_list
        return self.photo_dict