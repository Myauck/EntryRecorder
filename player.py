import keyboard
import mouse
import json
from os import path
from time import time


def move_mouse(position: tuple) -> None:
    mouse.move(position[0], position[1])
    mouse.press(button="left")
    mouse.release(button="left")


def do_command(command: str) -> None:
    keyboard.press(command)
    keyboard.release(command)


def write_text(text: str) -> None:
    keyboard.write(text)


class Player:

    __content: dict
    __record_length: int
    __file_path: str
    __looping: bool

    def __init__(self, file_name: str):
        self.__file_path: str = path.dirname(__file__) + "\\" + file_name
        self.load_json_configuration()
        self.__looping = True

    def load_json_configuration(self) -> None:
        if not path.exists(self.__file_path):
            print("Impossible de récupérer le contenu d'un fichier qui n'existe pas !")
            self.__record_length = 0
        else:
            with open(self.__file_path, "r") as f:
                self.__content = json.loads(f.read())
                self.__record_length = len(self.__content)
                print("Configuration chargée")

    def play(self) -> None:
        if self.__record_length == 0:
            print("Impossible de charger une configuration vide !")
        else:
            i: int = 0
            while self.__looping:
                rec: dict = self.__content[i]

                record_type: str = rec["event"]
                delay: float = rec["delay"]

                last_time: float = time()

                while True:
                    if time() - last_time > delay:
                        break
                    if keyboard.is_pressed("alt+s"):
                        self.__looping = False
                        break

                if record_type == "mouse":
                    move_mouse(rec["position"])
                elif record_type == "keyboard":
                    keyboard_type: str = rec["type"]
                    text_content: str = rec["text_content"]
                    if keyboard_type == "cmd":
                        do_command(text_content)
                    elif keyboard_type == "txt":
                        write_text(text_content)

                i += 1
                i %= self.__record_length
                continue
