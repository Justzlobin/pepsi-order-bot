class Count:

    def __init__(self):
        self.count_list = []
        self.chat_dict = {}
        self.uns_list = []

    def len_list_messages(self, chat_id):
        return len(self.chat_dict[chat_id])

    def add_message(self, chat_id, message_id):
        self.count_list.append(message_id)
        self.chat_dict = {chat_id: self.count_list}
        return self.chat_dict

    def delete_last_message(self, chat_id):
        return self.chat_dict[chat_id][0]

    def list_of_deleted_messages(self, chat_id):
        list_messages = self.chat_dict[chat_id]
        while len(list_messages) > 1:
            self.uns_list.append(self.count_list.pop(-1))
        return self.uns_list
