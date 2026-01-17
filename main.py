from core.game import start_game
from utils.save_load import load_game

def main_menu():
    while True:
        print("\n=== Black Hole Co. ===")
        print("1. Новая игра")
        print("2. Загрузить игру")
        print("3. Выход")

        choice = input("> ")

        if choice == "1":
            start_game()
        elif choice == "2":
            load_game()
        elif choice == "3":
            print("Выход из игры.")
            break
        else:
            print("Неверный ввод.")

if __name__ == "__main__":
    main_menu()
