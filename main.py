import psutil
import time
import json

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
    verlauf.append(zeiten)
    zeiten = {}

erlaubt = ["Spotify.exe", "Discord.exe", "firefox.exe", "voicemeeter.exe", "WhatsApp.Root.exe", "javaw.exe", "noriskclient-launcher-v3.exe", "steam.exe", "Among Us.exe", "CapCut.exe"]


while True:
    for prozess in psutil.process_iter(['name']):
        if prozess.info['name'] in erlaubt:
            zeiten[prozess.info['name']] = zeiten.get(prozess.info['name'], 0) + 1

    with open("zeiten.json", "w") as datei:
        json.dump(zeiten, datei)

    with open("verlauf.json", "w") as datei:
        json.dump(verlauf, datei)

    print(zeiten)
    time.sleep(10)