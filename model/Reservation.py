
class Reservation:
    def __init__(self, client=None, rno=None, details=None, price=None, number=None):
        self.client = client
        self.rno = rno
        self.details =details
        self.price = price
        self.number = number

    def create(self, client, rno, details):
        self.client = client
        self.rno = rno
        self.details = details
        number = 0
        price = 0
        for room in set(details.values):
            number += room.get_maxNo()
        for room in details.values:
            price += room.get_price()
        price = (10 - client.get_level()) / 10 * price
        self.price = price
        self.number = number

    def checkReservation(self, rno):
        if self.rno == rno:
            return True
        if self.rno != rno:
            return False

    def get_price(self):
        return self.price

    def get_NumberofClient(self):
        return self.number