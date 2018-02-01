import os
import random

class HotelManagementProcessor():

    def __init__(self):
        self.calendar_dict = {}
        self.input_path = '../locals/'
        self.state_file = 'state.txt'
        self.client_file = 'client.txt'
        self.hotel_file = 'hotel.txt'
        self.reservation_file = 'reservation.txt'
        self.reservation_detailed_file = 'reservation_detailed.txt'
        self.checkin_file = 'checkin.txt'

    def check_client(self, client_num):
        client_level = 0
        client_name = ""
        self.check_path(self.input_path)
        with open(self.input_path + self.client_file, mode='r+') as input:
            for line in input.readlines():
                if line.strip() == "":
                    continue
                info = line.split()
                # print(info)
                if (int(info[0]) == client_num):
                    client_level = int(info[1])
                    # print(info[2])
                    client_name = info[2]
                    break
        return client_level, client_name

    def check_hotel(self):
        self.check_path(self.input_path)
        with open(self.input_path + self.hotel_file) as input:
            info = input.readlines()
        return {x.split(':')[0]: self.str2list(x.split(':')[1], ',') for x in info}

    def check_reserved(self, date):
        found = []
        index_found = -1
        self.check_path(self.input_path)
        with open(self.input_path + self.reservation_file, mode='r+') as input:
            for index, line in enumerate(input.readlines()):
                if line.strip() == "":
                    continue
                if date == line.split(':')[0]:
                    found = [x.strip() for x in line.split(':')[1].split(',')]
                    index_found = index
                    break
        return found, index_found

    def check_reservation_num(self, reservation_num):
        reservation_client = None
        reservation_detail = None
        index_found = -1
        check_in = 0
        self.check_path(self.input_path)
        with open(self.input_path+self.reservation_detailed_file, mode='r+') as input:
            for index, line in enumerate(input.readlines()):
                # self.debugPrint(line.split()[0])
                if line.strip() == "":
                    continue
                if reservation_num == int(line.split()[0]):
                    reservation_client = int(line.split()[1])
                    reservation_detail = {x.split(':')[0]: x.split(':')[1] for x in line.split()[2].split(',')}
                    check_in = int(line.split()[3])
                    index_found = index
                    break
        return reservation_client, reservation_detail, index_found, check_in

    def add_client(self, client_level, client_name):
        client_num = random.randint(100000, 999999)
        while(self.check_client(client_num)[0] > 0):
            client_num = random.randint(100000, 999999)
        input_str = '\n' + ' '.join([str(x) for x in [client_num, client_level, client_name]])
        self.check_path(self.input_path)
        with open(self.input_path + self.client_file, mode='a') as input:
            input.write(input_str)

    def checkin_by_reservation(self, reservation_num):
        client, details, index_found, checkin = self.check_reservation_num(reservation_num)
        if(index_found != -1):
            input_str = "\n"
            with open(self.input_path+self.checkin_file, mode='a+') as output:
                for key in details.keys():
                    input_str += str(key) + ': ' + str(details[key])
                output.write(input_str)
            self.change_line_in_file(self.input_path+self.reservation_detailed_file, index_found,
                                     after=' '.join([str(reservation_num), str(client), self.dict2str(details), "1"]))

    def checkout_by_reservation(self, reservation_num):
        client, details, index_found, checkin = self.check_reservation_num(reservation_num)
        price = 0
        successed = False
        if(index_found != -1 and checkin == 1):
            self.change_line_in_file(self.input_path + self.reservation_detailed_file, index_found,
                                     after=' '.join([str(reservation_num), str(client), self.dict2str(details), "2"]))
            with open(self.input_path+self.checkin_file, mode='r+') as input:
                info = input.readlines()
            for date in details.keys():
                info.remove(str(date) + ': ' + str(details[date])+'\n')
                price += self.calculate_price(client, details[date])
            with open(self.input_path+self.checkin_file, mode='w+') as output:
                output.write(''.join(info))
            successed = True
        return price, successed

    def str2list(self, before, splitter):
        return [x.strip() for x in before.split(splitter)]

    def check_path(self, file_path):
        if not os.path.exists(file_path):
            os.makedirs(file_path)

    def num2str(self, num):
        if num < 10:
            return '0'+str(num)
        return str(num)

    def check_int(self, string):
        try:
            a = int(string)
            isInt = True
        except BaseException:
            isInt = False
        return isInt

    def dict2str(self, _dict):
        _str = []
        for key in _dict.keys():
            _str.append(str(key)+':'+str(_dict[key]))
        return ','.join(_str)

    def change_line_in_file(self, filename, index, after=None):
        with open(filename, mode='r+') as input:
            lines = input.readlines()
        if after is None:
            lines.remove(lines[index])
        else:
            lines[index] = after
        with open(filename, mode='w+') as output:
            output.write(''.join(lines))

    def change_lines_in_file(self, filename, changes):
        with open(filename, mode='r+') as input:
            info = input.readlines()
        for index in changes.keys():
            info[index] = changes[index]
        with open(filename, mode='w+') as output:
            output.write(''.join(info))

    def warningPrint(self, string):
        print("\n############################################################################################")
        print('\n' + string + '\n')
        print("############################################################################################\n")

    def normalPrint(self, string):
        print("\n============================================================================================")
        print('\n' + string + '\n')
        print("============================================================================================\n")

    def debugPrint(self, string):
        print("\n############################################################################################"
              "\n############################################################################################")
        print('\n' + "Debug information: "+ string + '\n')
        print("############################################################################################\n"
              "############################################################################################\n")

    def check_state(self, checkin_num):
        state= ""
        if checkin_num == 0:
            state = "Reserved"
        elif checkin_num == 1:
            state = "Checked in"
        elif checkin_num == 2:
            state = "Checked out"
        return state