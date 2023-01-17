from datadase.sqlite_db import create_new_custom


class Order:

    def __init__(self):
        self.user_dict = {}
        self.order_dict = {}
        self.item_dict = {}
        self.check_in = False

    def init_user(self, user_id):
        self.user_dict['user_id'] = user_id
        return self.user_dict

    def init_order(self, user_id):
        if self.user_dict['user_id'] == user_id:
            self.order_dict[user_id] = create_new_custom(user_id)
        else:
            pass

    def add_item(self, pos_id, value, user_id):
        if self.user_dict['user_id'] == user_id:
            self.item_dict[pos_id] = value
        else:
            pass

    def full_order(self):
        return {self.user_dict['user_id']: {self.order_dict['order_id']: {self.item_dict}}}

    def box(self):
        self.check_in = True
        return True

    def multi(self):
        self.check_in = False
        return False
