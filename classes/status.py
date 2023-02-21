class Status:
    def __init__(self):
        self.dialog_status = {}

    def current_dialog_status_price(self, user_id):
        self.dialog_status[user_id] = 'price'

    def current_dialog_status_order(self, user_id):
        self.dialog_status[user_id] = 'order'

    def current_dialog_status_admin(self, user_id):
        self.dialog_status[user_id] = 'admin'
