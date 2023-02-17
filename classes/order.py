class Order:

    def __init__(self, user_id):
        self.user_id = user_id
        self.order_dict = {user_id: {}}

    def add_pos(self, pos_id, value):
        self.order_dict[self.user_id][pos_id] = value
