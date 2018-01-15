import os
import random
import model.Client

class utils():
    def __init__(self):
        self.calendar_dict = {}
        self.input_path = '../locals/'
        self.state_file = 'state.txt'
        self.client_file = 'client.txt'
        self.hotel_file = 'hotel.txt'
        self.reservation_file = 'reservation.txt'
        self.reservation_detailed_file = 'reservation_detailed.txt'
        self.checkin_file = 'checkin.txt'

    # '1' for available '0' for being used
    def access_start(self):
        self.check_path(self.input_path)
        with open(self.input_path + self.state_file, mode='r+') as input:
            i = input.readline()
        if i == '1':
            with open(self.input_path + self.state_file, mode='w+') as input:
                input.write('0')
            return True
        else:
            return False

    def access_end(self):
        self.check_path(self.input_path)
        with open(self.input_path + self.state_file, mode='w+') as input:
            input.write('1')

    # 0 for no client registered, others for the levels recorded
    def check_client(self, client_num):
        client_level = 0
        client_name = ""
        self.check_path(self.input_path)
        with open(self.input_path + self.client_file, mode='r+') as input:
            for line in input.readlines():
                info = line.split()
                # print(info)
                if (int(info[0]) == client_num):
                    client_level = int(info[1])
                    # print(info[2])
                    client_name = info[2]
                    break
        return client_level, client_name

    def add_client(self, client_level, client_name):
        client_num = random.randint(100000, 999999)
        while(self.check_client(client_num)[0] > 0):
            client_num = random.randint(100000, 999999)
        input_str = '\n' + ' '.join([str(x) for x in [client_num, client_level, client_name]])
        self.check_path(self.input_path)
        with open(self.input_path + self.client_file, mode='a') as input:
            input.write(input_str)

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
                if reservation_num == int(line.split()[0]):
                    reservation_client = int(line.split()[1])
                    reservation_detail = {x.split(':')[0]: x.split(':')[1] for x in line.split()[2].split(',')}
                    check_in = int(line.split()[3])
                    index_found = index
                    break
        return reservation_client, reservation_detail, index_found, check_in

    # 0 for beginner, 1 for normal client, 2 for VIP, 3 for manager
    def add_reservation_base(self, date, type, pre_chosen=None):
        reserved, index = self.check_reserved(date)
        if index == -1:
            chosen = self.check_hotel()[type][0] if pre_chosen == None else pre_chosen
            input_str = '\n' + date + ': ' + chosen
            # print(chosen)
            with open(self.input_path + self.reservation_file, mode='a') as input:
                input.write(input_str)
        else:
            rooms = [x for x in self.check_hotel()[type] if x not in reserved]
            chosen = pre_chosen if pre_chosen in rooms else rooms[random.randint(0, len(rooms)-1)]
            reserved.append(chosen)
            # print(chosen)
            with open(self.input_path + self.reservation_file, mode='r+') as input:
                lines = input.readlines()
            lines[index] = lines[index].strip('\n') + ', ' + chosen + '\n'
            with open(self.input_path + self.reservation_file, mode='w+') as input:
                input.write(''.join(lines))

        # with open(self.input_path + self.reservation_detailed_file, mode='r+') as input:
        #     lines = input.readlines()
        # info = lines[-1]
        # if int(info.split()[0]) == reservation_num:
        #     lines[-1] = info + ',' + date + ':' + chosen
        #     with open(self.input_path + self.reservation_detailed_file, mode='w+') as input:
        #         input.write(lines)
        # else:
        #     input_str = str(reservation_num) + ' ' + str(client_num) + ' ' + date + ':' + chosen
        #     with open(self.input_path + self.reservation_detailed_file, mode='a') as input:
        #         input.write(input_str)
        return chosen

    def add_reservation(self, date_list, type, client_num):
        reservation_num = random.randint(10000000, 99999999)
        # while(self.check_reservation_num(reservation_num)[2] == -1):
        #     reservation_num = random.randint(10000000, 99999999)
        # print(reservation_num)
        result = {}
        if(len(date_list) > 1):
            pre_chosen = None
            for date in date_list:
                pre_chosen = self.add_reservation_base(date, type, pre_chosen)
                result[date] = pre_chosen
        else:
            result[date_list[0]] = self.add_reservation_base(date_list[0], type)
        with open(self.input_path + self.reservation_detailed_file, mode='a+') as output:
            output.write('\n' + ' '.join([str(reservation_num), str(client_num), self.dict2str(result), "0"]))
        # print(result)
        return result, reservation_num

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

    def cancel_reservation(self, reservation_num, client_num):
        client, details, index_found, checkin = self.check_reservation_num(reservation_num)
        successed = False
        if(checkin==0 and index_found!=-1 and client==client_num):
            self.change_line_in_file(self.input_path+self.reservation_detailed_file, index_found)
            with open(self.input_path+self.reservation_file, mode='r+') as input:
                reservations = input.readlines()
            changes = {}
            for key in details.keys():
                for index, reservation in enumerate(reservations):
                    if(key == reservation.split(': ')[0]):
                        _list = reservation.strip().split(': ')[1].split(', ')
                        _list.remove(details[key])
                        modified = ', '.join(_list)
                        changes[index] = key + ': ' + modified + '\n'
            self.change_lines_in_file(self.input_path+self.reservation_file, changes)
            successed = True
        return successed

    def calculate_price(self, client_num, room):
        discount = 1-(self.check_client(client_num)[0]/10)
        hotel = self.check_hotel()
        original_price = hotel['Single_price'][0] if room in hotel['Single'] else hotel['Double_price']
        return original_price*discount

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