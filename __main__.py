import recorder
import player


def main():
    response: str = recorder.ask_question("Voulez-vous charger ou ajouter une nouvelle configuration ?", ["Charger", "Enregistrer", "Quitter"])
    if response in recorder.get_waited_values(["Enregistrer"]):
        rec: recorder.Recorder = recorder.Recorder()
        rec.record()
    elif response in recorder.get_waited_values(["Charger"]):
        file_name = input("Quel fichier voulez-vous charger ? ")
        pl: player.Player = player.Player(file_name)
        pl.play()
    elif response in recorder.get_waited_values(["Quitter"]):
        exit(0)


if __name__ == '__main__':
    main()
