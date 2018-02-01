class calendar:

    def __init__(self):
        self.calendar_dict = {}
        self.input_path = '../locals/'
        self.state_file = 'state.txt'
        self.client_file = 'client.txt'
        self.hotel_file = 'hotel.txt'
        self.reservation_file = 'reservation.txt'
        self.reservation_detailed_file = 'reservation_detailed.txt'
        self.checkin_file = 'checkin.txt'

    def createCalendar(self, year):
        day1 = list(reversed(range(1, 29 + (1 if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) else 0))))
        day2 = list(reversed(range(1, 31)))
        day3 = list(reversed(range(1, 32)))
        day2_list = [4, 6, 9, 11]
        day3_list = [1, 3, 5, 7, 8, 10, 12]
        for day in day2_list:
            self.calendar_dict[day] = day2
        for day in day3_list:
            self.calendar_dict[day] = day3
        self.calendar_dict[2] = day1

    def check_state(self, checkin_num):
        state= ""
        if checkin_num == 0:
            state = "Reserved"
        elif checkin_num == 1:
            state = "Checked in"
        elif checkin_num == 2:
            state = "Checked out"
        return state