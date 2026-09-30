import tkinter as tk
from PIL import Image, ImageTk
import json
import psutil
import datetime

try:
    with open("zeiten.json", "r") as datei:
        zeiten = json.load(datei)
except FileNotFoundError:
    zeiten = {}

try:
    with open("verlauf.json", "r") as datei:
        verlauf = json.load(datei)
except FileNotFoundError:
    verlauf = []

if zeiten:
    verlauf.append({"datum": str(datetime.date.today()), "zeiten": zeiten})
    zeiten = {}

erlaubt = ["Spotify.exe", "Discord.exe", "firefox.exe", "voicemeeter.exe", "WhatsApp.Root.exe", "javaw.exe", "NoRiskClient.exe", "Steam.exe", "Among Us.exe", "CapCut.exe"]

max_sekunden = 10 * 60 * 60

def logo_pfad(parameter):
    ergebnis = "logos/" + parameter.replace(".exe", ".png")
    return ergebnis

def berechne_highscores():
    highscores = {}

    for eintrag in verlauf:
        datum = eintrag["datum"]
        for programm, sekunden in eintrag["zeiten"].items():
            if programm not in highscores or sekunden > highscores[programm]["sekunden"]:
                highscores[programm] = {"sekunden": sekunden, "datum": datum}

    return highscores

def zeige_highscores():
    highscores = berechne_highscores()

    highscore_fenster = tk.Toplevel(fenster)
    highscore_fenster.title("Highscores")
    highscore_fenster.geometry("400x300")

    for programm, daten in highscores.items():
        text = f"{programm}: {daten['sekunden']} Sekunden (am {daten['datum']})"
        label = tk.Label(highscore_fenster, text=text)
        label.pack()

fenster = tk.Tk()
fenster.title("App Nutzungs Tracker")
fenster.geometry("600x400")

knopf = tk.Button(fenster, text="Highscores anzeigen", command=zeige_highscores)
knopf.pack(pady=10)

widgets = {}

def erstelle_widget(programm):
    bild = Image.open(logo_pfad(programm))
    bild_tk = ImageTk.PhotoImage(bild)

    frame = tk.Frame(fenster)
    frame.pack(pady=10)

    name_label = tk.Label(frame, text=programm)
    name_label.pack()

    zeit_label = tk.Label(frame, text="0h 0m 0s")
    zeit_label.pack()

    unter_frame = tk.Frame(frame)
    unter_frame.pack()

    logo_label = tk.Label(unter_frame, image=bild_tk)
    logo_label.image = bild_tk
    logo_label.pack(side="left")

    canvas = tk.Canvas(unter_frame, width=300, height=30)
    canvas.pack(side="left")

    widgets[programm] = {"zeit_label": zeit_label, "canvas": canvas}

def update():
    bereits_gezaehlt = set()
    for prozess in psutil.process_iter(['name']):
        programm = prozess.info['name']

        if programm in erlaubt and programm not in bereits_gezaehlt:
            bereits_gezaehlt.add(programm)

            if programm not in widgets:
                erstelle_widget(programm)

            zeiten[programm] = zeiten.get(programm, 0) + 1
            sekunden = zeiten[programm]

            stunden = sekunden // 3600
            minuten = (sekunden % 3600) // 60
            rest_sekunden = sekunden % 60

            widgets[programm]["zeit_label"].config(text=f"{stunden}h {minuten}m {rest_sekunden}s")

            canvas = widgets[programm]["canvas"]
            canvas.delete("all")
            balken_breite = (sekunden / max_sekunden) * 300
            canvas.create_rectangle(0, 0, balken_breite, 30, fill="green")

    with open("zeiten.json", "w") as datei:
        json.dump(zeiten, datei)

    fenster.after(1000, update)

update()

fenster.mainloop()
input("Drück Enter zum Beenden...")