import datetime


class SelectDate:
    def __init__(self):
        self.select_date = {}
        self.select_date['from'] = datetime.date.today().strftime('%Y:%m:%d')
        self.select_date['to'] = datetime.date.today().strftime('%Y:%m:%d')

    def select_date_from(self, user_id, date):
        self.select_date[user_id]['from'] = date

    def select_date_to(self, user_id, date):
        self.select_date[user_id]['to'] = date
