from datadase import sqlite_db


class Order:

    def __init__(self, user_id):
        self.user_id = user_id
        self.new_order = sqlite_db.create_new_custom(user_id)
        self.dict_item = {}
        self.dict_order = {}
        print(self.user_id)
        print(self.new_order)
        print(self.dict_item)
        print(self.dict_order)

    def add_item(self, pos_id, values):
        self.dict_item[pos_id] = values
        self.dict_item[self.new_order] = self.dict_item
        print(self.dict_item)
        print(self.dict_item)
