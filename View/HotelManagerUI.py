import sys
from Controller.HotelManagementProcessor import HotelManagementProcessor

class HotelManagerUI():

    def __init__(self):
        # self.password = "awesome"
        self.hmp = HotelManagementProcessor()
        self.warning = {}
        self.warning['format'] = "Wrong input format "
        self.warning['date'] = "Date input doesn't exist "
        self.warning['missing'] = "Missing search filter of "
        self.warning['signin'] = "You don't have the permission of manager, please check clientUI instead "
        # self.warning['password'] = "Wrong password for manager-sign-in "
        self.menu = "Please input number to give command\n"  \
                    "1-->register a user to the system\n" \
                    "2-->input reservation number to check-in\n" \
                    "3-->input reservation number to check-out\n" \
                    "4-->exit"

    def userRegister(self):
        name = input("Please input name for registration: \n")
        level = input("Please input level for registration: \n")
        _continue = self.hmp.check_int(level) and int(level)<4
        while(not _continue):
            self.showWarning("format")
            level = input("Please input level for registration: \n")
            _continue = self.hmp.check_int(level) and int(level)<4
            self.hmp.add_client(level, name)
        self.hmp.normalPrint("Registration for " + name + " san succeed!")
        return

    def inputSignInInfo(self):
        manager_num = input("Please sign in your manager number: \n").strip()
        if (self.hmp.check_int(manager_num)):
            client_level = self.hmp.check_client(int(manager_num))[0]
            if client_level == 3:
                self.mainMenu()
            else:
                self.showWarning("signin")
                sys.exit(0)
        else:
            self.showWarning("format")
            sys.exit(0)

    def inputReservationNumberForCheckIn(self):
        reservation_num = input("Please input reservation number: \n").strip()
        if(self.hmp.check_int(reservation_num)):
            self.hmp.checkin_by_reservation(int(reservation_num))
            return
        else:
            self.showWarning("format")
            return

    def inputReservationNumberForCheckOut(self):
        reservation_num = input("Please input reservation number: \n").strip()
        if (self.hmp.check_int(reservation_num)):
            self.hmp.checkout_by_reservation(int(reservation_num))
            return
        else:
            self.showWarning("format")

    def showPrice(self):
        pass

    def showWarning(self, mode, addition = ""):
        self.hmp.warningPrint(self.warning[mode] + addition + "!")

    def mainMenu(self):
        while(True):
            self.hmp.normalPrint(self.menu)
            command = input("Input: ")
            if (self.hmp.check_int(command)):
                command = int(command)
                if (command == 1):
                    self.userRegister()
                elif (command == 2):
                    self.inputReservationNumberForCheckIn()
                elif (command == 3):
                    self.inputReservationNumberForCheckOut()
                elif (command == 4):
                    break
                else:
                    self.showWarning("format")
            else:
                self.showWarning("format")
        self.hmp.normalPrint("Thank you for using!")
        sys.exit(0)

if __name__ == '__main__':
    HotelManagerUI().inputSignInInfo()
