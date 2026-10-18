from datetime import datetime
import json
from pathlib import Path

DATENORDNER = (
    Path.home()
    / "Library"
    / "Application Support"
    / "TaskManager"
)

DATENORDNER.mkdir(
    parents=True,
    exist_ok=True
)

DATEIPFAD = DATENORDNER / "tasks.json"

from datetime import datetime,date

def aufgaben_laden():
    try:
        with open(DATEIPFAD, "r", encoding="utf-8") as datei:
            daten = json.load(datei)

    except FileNotFoundError:
        return [], 1

    if isinstance(daten, list):
        aufgaben = daten
        next_id = max(
            (aufgabe.get("id", 0) for aufgabe in aufgaben),
            default=0
        ) + 1
    else:
        aufgaben = daten["aufgaben"]
        next_id = daten["next_id"]

    for aufgabe in aufgaben:
        if "id" not in aufgabe:
            aufgabe["id"] = next_id
            next_id += 1

    return aufgaben, next_id

aufgaben, next_id = aufgaben_laden()

naechste_id = max(
    (aufgabe.get("id", 0) for aufgabe in aufgaben),
    default=0
) + 1

for aufgabe in aufgaben:
    if "id" not in aufgabe:
        aufgabe["id"] = naechste_id
        naechste_id += 1





aufgaben, next_id = aufgaben_laden()

for aufgabe in aufgaben:

    if "id" not in aufgabe:

        aufgabe["id"] = next_id

        next_id += 1

def frist_einlesen():
    while True:
        frist = input("Frist (YYYY-MM-DD): ").strip()

        try:
            datetime.strptime(frist, "%Y-%m-%d")
            return frist

        except ValueError:
            print("Ungültiges Datum. Bitte verwenden Sie das Format YYYY-MM-DD.")



def neue_id_generieren():
    global next_id

    neue_id = next_id
    next_id += 1

    return neue_id


def aufgabe_nach_id_finden(aufgaben_id):
    for aufgabe in aufgaben:
        if aufgabe["id"] == aufgaben_id:
            return aufgabe

    return None

def aufgabe_erledigen():
    aufgaben_kurz_anzeigen()

    try:
        aufgaben_id = int(input("Welche Aufgaben-ID möchten Sie als erledigt markieren? "))
    except ValueError:
        print("Bitte geben Sie eine Zahl ein.")
        return

    aufgabe = aufgabe_nach_id_finden(aufgaben_id)

    if aufgabe is None:
        print("Aufgabe nicht gefunden.")
        return

    aufgabe["status"] = "erledigt"
    aufgaben_speichern(aufgaben, next_id)

    print("Aufgabe wurde als erledigt markiert.")


def aufgabe_loeschen():
    aufgaben_kurz_anzeigen()

    try:
        aufgaben_id = int(input("Welche Aufgaben-ID möchten Sie löschen? "))
    except ValueError:
        print("Bitte geben Sie eine Zahl ein.")
        return

    aufgabe = aufgabe_nach_id_finden(aufgaben_id)

    if aufgabe is None:
        print("Aufgabe nicht gefunden.")
        return

    aufgaben.remove(aufgabe)
    aufgaben_speichern(aufgaben, next_id)

    print("Aufgabe wurde gelöscht.")


def aufgaben_speichern(aufgaben, next_id):
    daten = {
        "next_id": next_id,
        "aufgaben": aufgaben
    }

    with open(DATEIPFAD, "w", encoding="utf-8") as datei:
        json.dump(
            daten,
            datei,
            indent=4,
            ensure_ascii=False
        )

def aufgaben_anzeigen():
    print("\n--- Aufgaben ---")

    if len(aufgaben) == 0:

        print("Keine Aufgaben vorhanden.")

    else:

        for nummer, aufgabe in enumerate(aufgaben, start=1):
            print("\nNummer:", nummer)

            print("Titel:", aufgabe["titel"])

            print("Beschreibung:", aufgabe["beschreibung"])

            print("Priorität:", aufgabe["prioritaet"])

            print("Status:", aufgabe["status"])

            print("Frist:", aufgabe.get("frist", "Keine Frist"))

def aufgaben_kurz_anzeigen():
    for nummer, aufgabe in enumerate(aufgaben, start=1):
        print(nummer,aufgabe["titel"])

def text_einlesen(frage):
    while True:
        text = input(frage).strip()
        if text == "":
            print("Die Eingabe darf nicht leer sein.")
        else:
            return text

def aufgabennumer_einlesen(frage):
    try:
        nummer = int(input(frage))
        if nummer < 1 or nummer > len(aufgaben):
            print("Ungültige Aufgabennummer.")
            return None
        return nummer

    except ValueError:
        print("Bitte geben Sie eine Zahl ein.")
        return None


from datetime import datetime, date

def frist_einlesen():
    while True:
        frist = input("Frist (YYYY-MM-DD, leer = keine Frist): ").strip()

        if frist == "":
            return None

        try:
            frist_datum = datetime.strptime(frist, "%Y-%m-%d").date()

            if frist_datum < date.today():
                print("Die Frist darf nicht in der Vergangenheit liegen.")
            else:
                return frist_datum.isoformat()

        except ValueError:
            print("Ungültiges Datum. Bitte verwenden Sie das Format YYYY-MM-DD.")



def prioritaet_einlesen():
    while True:
        prioritaet = input("Priorität (hoch/mittel/niedrig): ").lower()

        if prioritaet in ["hoch", "mittel", "niedrig"]:
            return prioritaet
        else:
            print("Ungültige Priorität. Bitte wählen Sie hoch, mittel oder niedrig.")

def aufgaben_sortieren():
    return sorted(
        aufgaben,
        key=lambda aufgabe: aufgabe.get("frist") or "9999-12-31"
    )


def aufgabe_hinzufuegen():
    titel = text_einlesen("Titel:")
    beschreibung = text_einlesen("Beschreibung: ")
    prioritaet = prioritaet_einlesen()
    frist = frist_einlesen()

    aufgabe = {
        "id": neue_id_generieren(),
        "titel": titel,
        "beschreibung": beschreibung,
        "prioritaet": prioritaet,
        "status": "offen",
        "frist": frist
    }

    aufgaben.append(aufgabe)
    aufgaben_speichern(aufgaben, next_id)

    print("Aufgabe wurde hinzugefügt.")

def main():
    global aufgaben,next_id

    aufgaben, next_id = aufgaben_laden()
    while True:
        print("\n--- Task Manager ---")
        print("1 - Aufgabe hinzufügen")
        print("2 - Aufgaben anzeigen")
        print("3 - Aufgabe als erledigt markieren")
        print("4 - Aufgabe löschen")
        print("5 - Aufgaben nach Frist sortieren")
        print("0 - Programm beenden")

        befehl = input("Bitte wählen Sie einen Befehl: ")
        if befehl == "0":
            break
        elif befehl == "1":
            aufgabe_hinzufuegen()
        elif befehl == "2":
            aufgaben_anzeigen()
        elif befehl == "3":
            aufgaben_kurz_anzeigen()
            nummer = aufgabennumer_einlesen("Welche Aufgabe möchten Sie als erledigt markieren? ")
            if nummer is not None:
                aufgaben[nummer - 1]["status"] = "erledigt"
        elif befehl == "4":
            aufgaben_kurz_anzeigen()

            nummer = aufgabennumer_einlesen("Welche Aufgabe möchten Sie löschen? ")
            if nummer is not None:
                aufgaben.pop(nummer - 1)
                aufgaben_speichern(aufgaben, next_id)
                print("Aufgabe wurde gelöscht. ")


        elif befehl == "5":
            sortierte_aufgaben = aufgaben_sortieren()

            for aufgabe in sortierte_aufgaben:
                print("Titel:", aufgabe["titel"])
                print("Frist:", aufgabe.get("frist") or "Keine Frist")
                print("---")

if __name__ == "__main__":
    main()
