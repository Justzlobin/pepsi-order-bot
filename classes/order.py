class Order:

    def __init__(self):
        self.order_dict = {}
        self.pos_dict = {}
        self.checkin = {}

    def start_order(self, user_id):
        self.order_dict[user_id] = {}
        self.pos_dict[user_id] = {}
        self.checkin[user_id] = False

    def add_in_pos_dict(self, user_id, pos_id, value):
        self.pos_dict[user_id][pos_id] = value

    def add_in_order_dict(self, user_id, pos_id, value):
        del self.pos_dict[user_id][pos_id]
        self.order_dict[user_id][pos_id] = value
