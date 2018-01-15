from utils import utils
import sys

class HotelManagerUI():

    def __init__(self):
        # self.password = "awesome"
        self.util = utils()
        self.warning = {}
        self.warning['format'] = "Wrong input format "
        self.warning['date'] = "Date input doesn't exist "
        self.warning['missing'] = "Missing search filter of "
        self.warning['signin'] = "You don't have the permission of manager, please check clientUI instead "
        # self.warning['password'] = "Wrong password for manager-sign-in "
        self.menu = "Please input number to give command\n" \
                    "1-->show all rooms\n" \
                    "2-->show rooms by date\n" \
                    "3-->show all clients\n" \
                    "4-->show client by client number\n" \
                    "5-->register a user to the system\n" \
                    "6-->input reservation number to check-in\n" \
                    "7-->input reservation number to check-out\n" \
                    "8-->exit"

    def showAllRoom(self):
        # TODO
        return

    def showAllRoomByDate(self):
        # TODO
        return

    def showAllClient(self):
        # TODO
        return

    def showClientByClientNumber(self):
        # TODO
        return

    def userRegister(self):
        name = input("Please input name for registration: \n")
        level = input("Please input level for registration: \n")
        _continue = self.util.check_int(level) and int(level)<4
        while(not _continue):
            self.showWarning("format")
            level = input("Please input level for registration: \n")
            _continue = self.util.check_int(level) and int(level)<4
        # TODO register(name, level)
        self.util.normalPrint("Registration for " + name + " san succeed!")
        return

    def inputSignInInfo(self):
        manager_num = input("Please sign in your manager number: \n").strip()
        if (self.util.check_int(manager_num)):
            client_level = self.util.check_client(int(manager_num))[0]
            if client_level == 3:
                # TODO self.client = client(client_num)
                # TODO self.util.normalPrint("Welcome " + manager.name)
                self.mainMenu()
            else:
                self.showWarning("signin")
                sys.exit(0)
        else:
            self.showWarning("format")
            sys.exit(0)

    def inputReservationNumberForCheckIn(self):
        reservation_num = input("Please input reservation number: \n").strip()
        if(self.util.check_int(reservation_num)):
            # TODO checkin(reservation_num)
            return
        else:
            self.showWarning("format")
            return

    def inputReservationNumberForCheckOut(self):
        reservation_num = input("Please input reservation number: \n").strip()
        if (self.util.check_int(reservation_num)):
            # TODO checkout(reservation_num)
            return
        else:
            self.showWarning("format")

    def showPrice(self):
        pass

    def showWarning(self, mode, addition = ""):
        self.util.warningPrint(self.warning[mode] + addition + "!")

    def mainMenu(self):
        while(True):
            self.util.normalPrint(self.menu)
            command = input("Input: ")
            if (self.util.check_int(command)):
                command = int(command)
                if (command == 1):
                    self.showAllRoom()
                elif (command == 2):
                    self.showAllRoomByDate()
                elif (command == 3):
                    self.showAllClient()
                elif (command == 4):
                    self.showClientByClientNumber()
                elif (command == 5):
                    self.userRegister()
                elif (command == 6):
                    self.inputReservationNumberForCheckIn()
                elif (command == 7):
                    self.inputReservationNumberForCheckOut()
                elif (command == 8):
                    break
                else:
                    self.showWarning("format")
            else:
                self.showWarning("format")
        self.util.normalPrint("Thank you for using!")
        sys.exit(0)

if __name__ == '__main__':
    HotelManagerUI().inputSignInInfo()
