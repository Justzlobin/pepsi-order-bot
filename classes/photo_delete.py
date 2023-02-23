class PhotoDelete:

    def __init__(self):
        self.photo_dict = {}
        self.photo_list = []

    def add(self, chat_id, photo):
        self.photo_dict[chat_id] = self.photo_list.append(photo)

    def delete(self, chat_id):
        del self.photo_dict[chat_id]
