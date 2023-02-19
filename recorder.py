from os import path
import json

import mouse


def get_waited_values(waited_values: list) -> list:
    all_waited_values: list = []
    for waited_value in waited_values:
        all_waited_values.append(waited_value.lower()[0])
        all_waited_values.append(waited_value.lower())
    return all_waited_values


def ask_question(question: str, possible_answers: list) -> str:
    print(question)
    answers: list = get_waited_values(possible_answers)
    responses: str = "Réponses possibles : " + " | ".join(answers) + " --> "
    answer: str = input(responses).lower()
    while answer not in answers:
        answer = input("! Réponse invalide ! " + responses).lower()
    return answer


def ask_for_delay() -> float:
    answer: str = input("Veuillez définir un délai avant que cet enregistrement s'exécute --> ")
    while not answer.isnumeric():
        answer = input("! Délai invalide ! Veuillez définir un délai avant que cet enregistrement s'exécute --> ")
    return float(answer)


def add_mouse(click_position: tuple, delay: float) -> dict:
    return {"event": "mouse", "delay": delay, "position": click_position}


def add_keyboard(keyboard_type: str, text_content: str, delay: float) -> dict:
    return {"event": "keyboard", "delay": delay, "type": keyboard_type, "text_content": text_content}


class Recorder:
    __content: list
    __record_length: int

    def __init__(self):
        self.__content = []
        self.__record_length = 0

    def save_json_configuration(self, record_file: str) -> bool:
        file_path: str = path.dirname(__file__) + "\\" + record_file
        with open(file_path, 'w') as f:
            f.write(json.dumps(self.__content, indent=4))
            return True

    def add_record(self, record_content: dict) -> None:
        self.__content.append(record_content)
        self.__record_length += 1

    def record(self) -> None:
        record_type: str = ask_question("Quel type d'enregistrement voulez-vous faire ?",
                                        ["Clavier", "Souris", "Aucun"])
        if record_type in get_waited_values(["Clavier"]):
            command_type: str = ask_question("Quel type de entrée de clavier ?", ["Commande", "Texte"])

            if command_type in get_waited_values(["Commande"]):
                content = input("Veuillez saisir la commande : ")
                self.add_record(add_keyboard("cmd", content, ask_for_delay()))
            elif command_type in get_waited_values(["Texte"]):
                content = input("Veuillez saisir le texte : ")
                self.add_record(add_keyboard("txt", content, ask_for_delay()))
            self.record()

        elif record_type in get_waited_values(["Souris"]):
            click_position: tuple

            while True:
                if mouse.is_pressed(button="left"):
                    click_position = mouse.get_position()
                    correct = ask_question(f"Nouvelle position enregistrée : {click_position}. Valider ?",
                                           ["Oui", "Non"])
                    if correct in get_waited_values(["Oui"]):
                        break

            self.add_record(add_mouse(click_position, ask_for_delay()))
            self.record()

        elif record_type in get_waited_values(["Aucun"]):
            file_name: str = input("Spécifiez le nom du fichier")
            self.save_json_configuration(file_name)
            print(f"Votre configuration ({self.__record_length} enregistrement) a été enregistré dans {file_name}")
