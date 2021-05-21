# This is a sample Python script.
import random
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
menu = []
new_menu = []
days = ['za: ','zo: ','ma: ','di: ','wo: ','do: ','vr: ']


def print_menu():
    eetlijst = open('eetlijst.txt','r')
    for line in eetlijst.readlines():
        menu_item = line.strip()
        if len(menu_item) != 0:
            if not menu_item in menu:
                menu.append(menu_item)

    while len(new_menu) < 7:
        new_item = random.choice(menu)
        if new_item not in new_menu:
            new_menu.append(new_item)

    for i in range(7):
        print(f'{days[i]}{new_menu[i]}')


if __name__ == '__main__':
    print_menu()
