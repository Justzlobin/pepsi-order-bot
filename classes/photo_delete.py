class PhotoDelete:

    def __init__(self):
        self.photo_dict = {}
        self.photo_list = []

    def add(self, chat_id, message):
        self.photo_list.append(message)
        self.photo_dict[chat_id] = self.photo_list

    def delete(self, chat_id):
        self.photo_dict[chat_id].clear()
