class SelectDate:
    def __init__(self):
        self.select_date = {}

    def select_date_from(self, user_id, date):
        self.select_date[user_id]['from'] = date

    def select_date_to(self, user_id, date):
        self.select_date[user_id]['to'] = date

