
class Room:
    def __init__(self, room_number, max_number, price):
        self.roomNo = room_number
        self.maxNo = max_number
        self.price = price

    def get_maxNo(self):
        return self.maxNo

    def get_price(self):
        return self.price
