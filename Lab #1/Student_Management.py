from Classes.Menu import Menu
from Classes.University import University
if __name__ == "__main__":
    university = University()
    menu = Menu(university)
    menu.run()