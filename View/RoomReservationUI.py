from utils import utils
import sys

class RoomReservationUI():
    def __init__(self):
        self.util = utils()
        self.date = []
        self.type = None
        self.warning = {}
        self.warning['format'] = "Wrong input format "
        self.warning['date'] = "Date input doesn't exist "
        self.warning['missing'] = "Missing search filter of "
        self.warning['signin'] = "Please contact manager to register your account "
        self.warning['notfound'] = "Can not find "
        self.warning['failure'] = "Failure operation of "
        self.year = None
        self.month = None
        self.day = None
        self.client = None
        self.client_num = None
        self.reservation_num = None
        self.menu = "Please input number to give command:\n" \
                    "   1-->add date searching filter\n" \
                    "   2-->change type searching filter\n" \
                    "   3-->delete data searching filter\n" \
                    "   4-->search rooms\n" \
                    "   5-->check reservation\n" \
                    "   6-->cancel reservation\n" \
                    "   7-->exit"

    def inputDateSearchCondition(self):
        year = input("Please input year: ").strip()
        if(self.util.check_int(year)):
            self.year = int(year)
            self.util.createCalendar(self.year)
        else:
            self.showWarning("format")
            return
        month = input("Please input month: ").strip()
        _continue = self.util.check_int(month) and int(month) in self.util.calendar_dict.keys()
        while(not _continue):
            if(not self.util.check_int(month)):
                self.showWarning("format")
            else:
                self.showWarning("date")
            month = input("Please input month: ").strip()
            _continue = self.util.check_int(month) and int(month) in self.util.calendar_dict.keys()
        self.month = int(month)
        day = input("Please input day: ").strip()
        _continue = self.util.check_int(day) and int(day) in self.util.calendar_dict[self.month]
        while (not _continue):
            if (not self.util.check_int(day)):
                self.showWarning("format")
            else:
                self.showWarning("date")
            day = input("Please input day: ").strip()
            _continue = self.util.check_int(day) and int(day) in self.util.calendar_dict[self.month]
        self.day = int(day)
        toAdd = str(self.year) + self.util.num2str(self.month) + self.util.num2str(self.day)
        self.date.append(toAdd)
        self.util.normalPrint("Setting of SearchDate: " + toAdd + " succeed!")
        return

    def inputTypeSearchCondition(self):
        type = input("Please input room type (D for Double and S for Single): ").strip()
        if (type == "D" or type == "Double"):
            self.type = "Double"
            self.util.normalPrint("Setting of SearchType: " + self.type + " succeed!")
            return
        elif (type == "S" or type == "Single"):
            self.type = "Single"
            self.util.normalPrint("Setting of SearchType: " + self.type + " succeed!")
            return
        else:
            self.showWarning("format")
            return

    def deleteDateSearchCondition(self):
        if(len(self.date) < 1):
            self.showWarning("missing", "date")
            return
        else:
            year = input("Please input year: ").strip()
            if (self.util.check_int(year)):
                self.year = int(year)
                self.util.createCalendar(year)
            else:
                self.showWarning("format")
                return
            month = input("Please input month: ").strip()
            _continue = self.util.check_int(month) and int(month) in self.util.calendar_dict.keys()
            while (not _continue):
                if (not self.util.check_int(month)):
                    self.showWarning("format")
                else:
                    self.showWarning("date")
                month = input("Please input month: ").strip()
                _continue = self.util.check_int(month) and int(month) in self.util.calendar_dict.keys()
            self.month = int(month)
            day = input("Please input day: ").strip()
            _continue = self.util.check_int(day) and int(day) in self.util.calendar_dict[self.month]
            while (not _continue):
                if (not self.util.check_int(day)):
                    self.showWarning("format")
                else:
                    self.showWarning("date")
                day = input("Please input day: ").strip()
                _continue = self.util.check_int(day) and int(day) in self.util.calendar_dict[self.month]
            self.day = int(day)
            toDelete = str(self.year) + self.util.num2str(self.month) + self.util.num2str(self.day)
            if toDelete in self.date:
                self.date.remove(toDelete)
                self.util.normalPrint("Remove of SearchDate: " + toDelete + " succeed!")
                return
            else:
                self.showWarning("date", "in search filter ")
                return

    def searchRoom(self):
        if len(self.date) < 1:
            self.showWarning("missing", "date ")
            return
        elif self.type == None:
            self.showWarning("missing", "type ")
            return
        else:
            results, self.reservation_num = self.util.add_reservation(self.date, self.type, self.client_num)
            self.util.normalPrint("Your reservation number for this time is " + str(self.reservation_num) + "\n"
                                  + "The searching result is as follows:\n" + str(results))
            self.showConfirmReservationMessage()
            return

    def checkReservation_base(self, reservation_num=None):
        if reservation_num is None:
            if self.reservation_num is None:
                self.showWarning("missing", "reservation number ")
                return
            else:
                reservation_client, reservation_detail, index_found, check_in = self.util.check_reservation_num(self.reservation_num)
                if index_found==-1 or self.client_num!=reservation_client:
                    self.showWarning("notfound", "reservation of reservation number: " + str(self.reservation_num) + " of your account")
                    return
                else:
                    toDisplay = ("Reservation number: " + str(reservation_num) + "\n" + "Reservation client: "
                                 + str(reservation_client) + "\n" + "Reservation details: "
                                 + str(reservation_detail) + "\n" + "Reservation state: " + str(check_in) +"\n")
                    self.util.normalPrint(toDisplay)
                    return
        else:
            reservation_client, reservation_detail, index_found, check_in = self.util.check_reservation_num(
                reservation_num)
            if index_found == -1:
                self.showWarning("notfound", "reservation of reservation number: " + str(reservation_num))
                return
            else:
                toDisplay = ("Reservation number: " + str(reservation_num) + "\n" + "Reservation client: "
                             + str(reservation_client) + "\n" + "Reservation details: "
                             + str(reservation_detail) + "\n" + "Reservation state: " + self.util.check_state(check_in) + "\n")
                self.util.normalPrint(toDisplay)
                return

    def cancelReservation_base(self, reservation_num=None):
        if reservation_num is None:
            if self.reservation_num is None:
                self.showWarning("missing", "reservation number ")
                return
            else:
                succeeded = self.util.cancel_reservation(self.reservation_num, self.client_num)
                if succeeded:
                    toDisplay = ("Reservation of reservation number: " + str(self.reservation_num) + " canceled!")
                    self.util.normalPrint(toDisplay)
                    return
                else:
                    self.showWarning("failure", "reservation canceling of reservation number: " + str(self.reservation_num))
                    return
        else:
            succeeded = self.util.cancel_reservation(reservation_num, self.client_num)
            if succeeded:
                toDisplay = ("Reservation of reservation number: " + str(reservation_num) + " canceled!")
                self.util.normalPrint(toDisplay)
                return
            else:
                self.showWarning("failure", "reservation canceling of reservation number: " + str(self.reservation_num))
                return

    def checkReservation(self):
        reservation_num = input("Please input reservation number: ").strip()
        if reservation_num == "":
            self.checkReservation_base()
        else:
            if self.util.check_int(reservation_num):
                self.checkReservation_base(int(reservation_num))
            else:
                self.showWarning("format")
        return

    def cancelReservation(self):
        reservation_num = input("Please input reservation number: ").strip()
        if reservation_num == "":
            self.cancelReservation_base()
        else:
            if self.util.check_int(reservation_num):
                self.cancelReservation_base(int(reservation_num))
            else:
                self.showWarning("format")
        return

    def showPrice(self):
        pass

    def showWarning(self, mode, addition = ""):
        self.util.warningPrint(self.warning[mode] + addition + "!")

    def showConfirmReservationMessage(self):
        confirmed = input("\nAre you sure to confirm the reservation above? (y for YES and n for NO)\n").strip()
        if(confirmed == 'y'):
            self.util.normalPrint("Reservation succeed!\nYour reservation number is : " + str(self.reservation_num) + " !")
            return
        elif(confirmed == 'n'):
            self.cancelReservation_base()
            self.util.normalPrint("Cancelation of reservation: " + str(self.reservation_num) + ' succeed!')
            return
        else:
            self.showWarning("format")
            # self.showConfirmReservationMessage()
            return

    def inputSignInInfo(self):
        client_num = input("Please sign in your client number: \n").strip()
        if(self.util.check_int(client_num)):
            client_level, client_name = self.util.check_client(int(client_num))
            if client_level == 0:
                self.showWarning("signin")
                sys.exit(0)
            else:
                # TODO self.client = client(client_num)
                # TODO self.util.normalPrint("Welcome " + client.name)
                self.util.normalPrint("Welcome " + client_name + " san!")
                self.client_num = int(client_num)
                self.mainMenu()
        else:
            self.showWarning("format")
            sys.exit(0)

    def showLevel(self):
        pass

    def mainMenu(self):
        while(True):
            self.util.normalPrint(self.menu)
            command = input("Input command: ").strip()
            if(self.util.check_int(command)):
                command = int(command)
                if(command == 1):
                    self.inputDateSearchCondition()
                elif(command == 2):
                    self.inputTypeSearchCondition()
                elif(command == 3):
                    self.deleteDateSearchCondition()
                elif(command == 4):
                    self.searchRoom()
                elif(command == 5):
                    self.checkReservation()
                elif(command == 6):
                    self.cancelReservation()
                elif(command == 7):
                    break
                else:
                    self.showWarning("format")
            else:
                self.showWarning("format")
        self.util.normalPrint("Thank you for using!")
        sys.exit(0)

if __name__ == '__main__':
    RoomReservationUI().inputSignInInfo()