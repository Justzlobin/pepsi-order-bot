# class PhotoDelete:
#
#     def __init__(self):
#         self.photo_dict = {}
#         self.photo_list = []
#
#     def add_message_photo(self, chat_id, message_id):
#         self.photo_list.append(message_id)
#         self.photo_dict[chat_id] = self.photo_list
#         return self.photo_dict
class PhotoDelete:

    def __init__(self, chat_id, message_id):
        self.photo_list = []
        self.photo_dict = {}
        self.photo_list.append(message_id)
        self.photo_dict[chat_id] = self.photo_list


