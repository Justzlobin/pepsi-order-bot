class Order:

    def __init__(self):
        self.order_dict = {}
        self.pos_dict = {}
        self.checkin = {}
        self.order_settings_dict = {}

    def start_order(self, user_id):
        self.order_dict[user_id] = {}
        self.pos_dict[user_id] = {}
        self.checkin[user_id] = False
        self.order_settings_dict[user_id] = {'payment': 'Готівка', 'comment': 'Без коментарів'}

    def add_in_pos_dict(self, user_id, pos_id, value):
        self.pos_dict[user_id][pos_id] = value

    def add_in_order_dict(self, user_id, pos_id, value):
        del self.pos_dict[user_id][pos_id]
        self.order_dict[user_id][pos_id] = value

    def add_comment(self, user_id, comment):
        self.order_settings_dict[user_id]['comment'] = comment

    def add_payment(self, user_id, payment):
        self.order_settings_dict[user_id]['payment'] = payment
