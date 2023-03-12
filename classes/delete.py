
class StateMessage:

    def __init__(self):
        self.message_dict = {}

    def add_message(self, message):
        self.message_dict['message'] = message


class DeleteMessage:

    def __init__(self):
        self.delete_message_dict = {}

    def change_message(self, user_id, message_id):
        self.delete_message_dict[user_id] = message_id
