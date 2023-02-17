class Order:

    def __init__(self):
        self.order_dict = {}

    def start_order(self, user_id):
        self.order_dict[user_id] = {}

    def add_pos(self, user_id, pos_id, value):
        self.order_dict[user_id][pos_id] = value
