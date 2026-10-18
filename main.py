import tkinter as tk
from tkinter import ttk
import json
from pathlib import Path
from datetime import datetime
from datetime import datetime,date
from task_manager import aufgaben_laden, aufgaben_speichern




def ausgewaehlte_aufgabe_finden():
    auswahl = tabelle.selection()

    if not auswahl:
        messagebox.showwarning(
            "Keine Auswahl",
            "Bitte wählen Sie zuerst eine Aufgabe aus."
        )
        return None

    aufgaben_id = int(auswahl[0])

    for aufgabe in aufgaben:
        if aufgabe["id"] == aufgaben_id:
            return aufgabe

    return None


def aufgabe_erledigen():
    aufgabe = ausgewaehlte_aufgabe_finden()

    if aufgabe is None:
        return

    aufgabe["status"] = "erledigt"
    aufgaben_speichern(aufgaben,next_id)

    tabelle.set(
        str(aufgabe["id"]),
        "status",
        "erledigt"
    )



def aufgabe_loeschen():
    aufgabe = ausgewaehlte_aufgabe_finden()

    if aufgabe is None:
        return

    bestaetigung = messagebox.askyesno(
        "Aufgabe löschen",
        "Möchten Sie diese Aufgabe wirklich löschen?"
    )

    if not bestaetigung:
        return

    aufgaben.remove(aufgabe)
    aufgaben_speichern(aufgaben, next_id)

    tabelle.delete(str(aufgabe["id"]))




def aufgabe_hinzufuegen():
    dialog = tk.Toplevel(fenster)
    dialog.title("Neue Aufgabe")
    dialog.geometry("400x350")

    ttk.Label(dialog, text="Titel:").pack(pady=5)
    titel_entry = ttk.Entry(dialog, width=40)
    titel_entry.pack()

    ttk.Label(dialog, text="Beschreibung:").pack(pady=5)
    beschreibung_entry = ttk.Entry(dialog, width=40)
    beschreibung_entry.pack()

    ttk.Label(dialog, text="Priorität:").pack(pady=5)
    prioritaet_box = ttk.Combobox(
        dialog,
        values=["hoch", "mittel", "niedrig"],
        state="readonly"
    )
    prioritaet_box.set("mittel")
    prioritaet_box.pack()

    ttk.Label(dialog, text="Frist (YYYY-MM-DD, optional):").pack(pady=5)
    frist_entry = ttk.Entry(dialog, width=40)
    frist_entry.pack()


    def speichern():
        global next_id

        titel = titel_entry.get().strip()
        beschreibung = beschreibung_entry.get().strip()
        prioritaet = prioritaet_box.get()
        frist = frist_entry.get().strip()

        if not titel or not beschreibung:
            messagebox.showwarning(
                "Ungültige Eingabe",
                "Titel und Beschreibung dürfen nicht leer sein.",
                parent=dialog
            )
            return

        if frist:
            try:
                frist_datum = datetime.strptime(
                    frist, "%Y-%m-%d"
                ).date()

                if frist_datum < date.today():
                    messagebox.showwarning(
                        "Ungültige Frist",
                        "Die Frist darf nicht in der Vergangenheit liegen.",
                        parent=dialog
                    )
                    return

                frist = frist_datum.isoformat()

            except ValueError:
                messagebox.showwarning(
                    "Ungültiges Datum",
                    "Bitte verwenden Sie das Format YYYY-MM-DD.",
                    parent=dialog
                )
                return
        else:
            frist = None

        neue_aufgabe = {
            "id": next_id,
            "titel": titel,
            "beschreibung": beschreibung,
            "prioritaet": prioritaet,
            "status": "offen",
            "frist": frist
        }

        aufgaben.append(neue_aufgabe)
        next_id += 1

        try:
            aufgaben_speichern(aufgaben, next_id)

        except Exception as fehler:
            aufgaben.remove(neue_aufgabe)
            next_id -= 1

            messagebox.showerror(
                "Fehler beim Speichern",
                f"{type(fehler).__name__}: {fehler}",
                parent=dialog
            )
            return


        tabelle.insert(
            "",
            "end",
            iid=str(neue_aufgabe["id"]),
            values=(
                neue_aufgabe["id"],
                titel,
                prioritaet,
                "offen",
                frist or "Keine Frist"
            )
        )

        dialog.destroy()



    speichern_button = ttk.Button(
        dialog,
        text="Speichern",
        command=speichern
    )
    speichern_button.pack(pady=20)


fenster = tk.Tk()
fenster.title("Mein Task Manager")
fenster.geometry("900x500")

titel = ttk.Label(
    fenster,
    text="Meine Aufgaben",
    font=("Arial", 20)
)
titel.pack(pady=20)

spalten = ("id", "titel", "prioritaet", "status", "frist")

tabelle = ttk.Treeview(
    fenster,
    columns=spalten,
    show="headings"
)

tabelle.heading("id", text="ID")
tabelle.heading("titel", text="Titel")
tabelle.heading("prioritaet", text="Priorität")
tabelle.heading("status", text="Status")
tabelle.heading("frist", text="Frist")

tabelle.column("id", width=50, anchor="center")
tabelle.column("titel", width=250)
tabelle.column("prioritaet", width=100)
tabelle.column("status", width=100)
tabelle.column("frist", width=120)

tabelle.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)

aufgaben, next_id = aufgaben_laden()

for aufgabe in aufgaben:
    tabelle.insert(
        "",
        "end",
        iid=str(aufgabe["id"]),
        values=(
            aufgabe["id"],
            aufgabe["titel"],
            aufgabe["prioritaet"],
            aufgabe["status"],
            aufgabe.get("frist") or "Keine Frist"
        )
    )

from tkinter import messagebox


button_frame = ttk.Frame(fenster)
button_frame.pack(pady=10)

erledigen_button = ttk.Button(
    button_frame,
    text="Erledigen",
    command=aufgabe_erledigen
)
erledigen_button.pack(side="left", padx=10)

loeschen_button = ttk.Button(
    button_frame,
    text="Löschen",
    command=aufgabe_loeschen
)
loeschen_button.pack(side="left", padx=10)

hinzufuegen_button = ttk.Button(
    button_frame,
    text="Hinzufügen",
    command=aufgabe_hinzufuegen
)

hinzufuegen_button.pack(side="left", padx=10)

fenster.mainloop()