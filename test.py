# from utils import utils
import random

def func1():
    return 1, 2, 3

def test1():
    with open('./locals/reservation.txt', mode='r+') as input:
        info = input.readlines()
    with open('./locals/reservation.txt', mode='w+') as output:
        output.write(''.join(info))

if __name__ == '__main__':
    # util = utils(2017)
    # print(util.check_hotel())
    # with open('./locals/test.txt', mode='r') as input:
    #     a = input.readline()
    # print(random.randint(100000, 999999))
    # print(random.randint(0, 2))
    # a = input("Input: ")
    # print(type(a))
    test1()