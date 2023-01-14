class UnMessage:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.list_message = []

    def add_message(self, message_id):
        self.list_message.append(message_id)
        return self.list_message

    def full_list_message(self):
        return self.list_message
