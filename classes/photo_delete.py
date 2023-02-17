class PhotoDelete:

    def __init__(self, chat_id, message_id):
        self.photo_list = []
        self.photo_dict = {}
        self.photo_list.append(message_id)
        self.photo_dict[chat_id] = self.photo_list


