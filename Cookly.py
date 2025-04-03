import json

# Rezept-Bibliothek
rezepte = {
    "Shepherd's Pie": {
        "portionen": 4, # Standard Portionen
        "zubereitungszeit": "45 Min.",
        "verderblichkeit": "2", # Wert zwischen 1-3 (1 = Nur Konserven, 2 = Haltbares Gemüse, 3 = Leicht verderbliche Lebensmittel)
        "zutaten": {
            "Kartoffeln": (7, "Stk."),
            "Milch": (150, "ml"),
            "Butter": (30, "g"),
            "Pizzatomaten": (200, "g"),
            "Bohnen": (200, "g"),
            "Mais": (100, "g"),
            "Reibekäse": (100,"g"),
            "Salz+Pfeffer": (1, "Prise"),
            "Muskat": (1, "Prise")
        },
        "zubereitung": {
            1: "Aus Kartoffeln, Milch, Butter, Salz+Pfeffer und Muskat Kartoffelbrei herstellen.",
            2: "Die Pizzatomaten, Bohnen und Mais in eine Auflaufform geben.",
            3: "Den Kartoffelbrei über den Tomatenmix geben und mit Käse bestreuen.",
            4: "Die Auflaufform in den Ofen stellen und bei 180 °C Umluft für etwa 15 Min. backen, bis der Käse goldbraun ist."
        }
    }
}

wochenplan_list = [] 
einkaufsliste_list = []

# Speicherfunktion
def bib_speichern():
    daten = {"rezepte": rezepte, "wochenplan": wochenplan, "einkaufsliste": einkaufsliste}

    try:
        with open("bib.json", "w", encoding="utf-8") as datei:
            json.dump(daten, datei, indent=4)

        print("Deine Rezeptbibliothek wurde gespeichert.")

    except Exception as e:
        print(f"Fehler beim Speichern: {e}.")

# Bib Laden
def bib_laden():
    global rezepte, wochenplan, einkaufsliste
    
    try:
        with open("bib.json", "r", encoding="utf-8") as datei:
            daten = json.load(datei)

        rezepte = daten.get("rezepte", {})
        wochenplan = daten.get("wochenplan", {})
        einkaufsliste = daten.get("einkaufsliste", {})

        print("\nDeine Rezeptbibliothek wurde geladen.")

    except FileNotFoundError:
        print("\nKein gespeicherter Speicherstand gefunden.")
    except json.JSONDecodeError:
        print("Fehler: Die Datei ist beschädigt oder ungültig.")

# Rezept-Ausgabe
def rezept_anzeigen():
    while True: 
        wahl = input("Welches Rezept möchtest du anzeigen lassen? \n> ").lower
        while True:
            try:
                portionen = int(input("Wie viele Portionen möchtest du kochen? \n> "))
                if portionen <= 0:
                    print("Bitte gib mindestens '1' ein.")
                else:
                    break
            except ValueError:
                print("Ungültige Eingabe, bitte gib eine Zahl ein.")

        if wahl in rezepte:
            gewähltes_rezept = rezepte[wahl]

            # Mengenberechnung
            faktor = portionen / gewähltes_rezept["portionen"]
            
            print(f"\n🌟 {wahl} 🌟\n")
            print(f"Portionen: {portionen}")
            print(f"Zubereitungszeit: {gewähltes_rezept['zubereitungszeit']}\n")

            print("📝 Zutaten:")
            for zutat, (menge, einheit) in gewähltes_rezept["zutaten"].items():
                neue_menge = round(menge * faktor, 2)
                print(f"- {neue_menge} {einheit} {zutat}" if einheit else f" {neue_menge} {zutat}")
            
            print("\n👨‍🍳 Zubereitung:")
            for schritt, text in gewähltes_rezept["zubereitung"].items():
                print(f"{schritt}. {text}")

            print("\nSoll das Rezept auf den Wochenplan? (ja/nein)")
            entscheidung = input("> ").strip().lower()
            if entscheidung == "ja":
                print(f"{wahl} wurde zum Wochenplan hinzugefügt!")
                wochenplan_list.append(wahl)

                print("Möchtest du ein weitere Rezept anzeigen lassen? (ja/nein)")
                while True:
                    try:
                        weiteres_rezept = input("> ").lower
                        if weiteres_rezept == "nein":
                            break
                        if weiteres_rezept == "ja":
                            continue
                        else:
                            print("Bitte gib 'ja' oder 'nein' ein.")
                    except ValueError:
                        print("Ungültige Eingabe. Bitte gib 'ja' oder 'nein' ein.")
            else:
                print("Okay, dann vielleicht später!")

                print("Möchtest du ein weitere Rezept anzeigen lassen? (ja/nein)")
                while True:
                    try:
                        weiteres_rezept = input("> ").lower
                        if weiteres_rezept == "nein":
                            break
                        if weiteres_rezept == "ja":
                            continue
                        else:
                            print("Bitte gib 'ja' oder 'nein' ein.")
                    except ValueError:
                        print("Ungültige Eingabe. Bitte gib 'ja' oder 'nein' ein.")
        else:
            print("Dieses Rezept befindet sich nicht in der Bibliothek. Überprüfe die Rechtschreibung.")

# Wochenplan
def wochenplan():
    tage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    auswahl = []

    if not wochenplan_list:
        print("Deine Wochenplan-Liste ist noch leer.")
        return
    
    print(f"Auf deiner Wochenplan-Liste befinden sich die folgenden Rezepte:")
    wochenplan_dict = {i + 1: rezept for i, rezept in enumerate(wochenplan_list)}

    for key, value in wochenplan_dict.items():
        print(f"{key}. {value}")

    print("Wähle nun bis zu 7 Gerichte für deinen Wochenplan aus.")
    while len(auswahl < 7):
        eingabe = input("Bitte gib die Nummer eines Gerichtes ein (oder 'fertig' wenn du genug Gerichte ausgewählt hast)\n> ")
            
        if eingabe.lower() == "fertig":
            if len(auswahl) == 0:
                print("Du musst mindestens ein Gericht eingeben.")
                continue
            break
            
        try:
            nummer = int(eingabe)
            if nummer in wochenplan_dict and wochenplan_dict[nummer] not in auswahl:
                auswahl.append(wochenplan_dict[nummer])
                print(f"Du hast {wochenplan_dict[nummer]} erfolgreich hinzugefügt.")
            else:
                print("Ungültige Eingabe oder Gericht bereits ausgewählt.")
        except ValueError: 
            print("Bitte gib eine Zahl ein.")

    index = 0
    while len(auswahl) < 7:
        auswahl.append(auswahl[index])
        index += 1

    auswahl.sort(key=lambda gericht: rezepte[gericht]["verderblichkeit"], reverse=True)

    finaler_wochenplan = {}
    for i , tag in enumerate(tage):
        finaler_wochenplan[tag] = auswahl[i]

    bib_speichern()

    print("\nDein optimierter Wochenplan wurde erstellt:")
    for tag, gericht in finaler_wochenplan.items():
        print(f"{tag}: {gericht}")

# Einkaufsliste
def einkaufsliste():
    print("")
    print("Möchtest du deine Einkaufsliste an bring! übergeben?") # Ist das möglich?

# Neues Rezept hinzufügen
def neues_rezept(rezepte):
    while True: 
        zubereitungs_dict = {}
        zutaten_dict = {}

        print("Welches Rezept möchtest du hinzufügen?")
        name = input("Name: ")
        
        print("Für wie viele Portionen ist das Rezept ausgelegt?")
        while True: 
            try:
                portionen = int(input("Portionen: "))
                if portionen > 0:
                    break
                else:
                    print("Bitte gib eine Zahl, größer als 0 ein.")
            except ValueError: 
                print("Ungültige Eingabe. Bitte gib eine Zahl ein.")

        print("Wie lange dauert es das Rezept zuzubereiten?")
        zubereitungszeit = input("Zubereitungszeit: ")

        print("Wie verderblich sind die Zutaten für das Rezept?")
        print("Bitte gib an: 1 = Nur Konserven, 2 = Haltbares Gemüse, 3 = Leicht verderbliche Lebensmittel")
        print("Das hilft deiner App dabei, besser zu kalkukulieren, wenn du einen Wochenplan erstellen möchtest.")
        verderblichkeit = input("Verderblichkeit: ")

        print("Nun kannst du die Zutaten hinzufügen.")
        while True: 
            zutat = input("Bitte gib eine Zutat ein (oder 'fertig', um abzuschließen): ")
            if zutat.lower() == "fertig":
                break
            menge = input(f"Gib die Menge für {zutat} ein: ")
            einheit = input(f"Gib die Einheit für {zutat} ein (z.B. g, ml, EL): ")
            zutaten_dict[zutat] = (menge, einheit)

        print("Nun kannst du die Verarbeitungsschritte eingeben.")
        nummer = 1
        while True: 
            schritt = input(f"Schritt {nummer} (oder 'fertig', um abzuschließen): ")
            if schritt.lower() == "fertig":
                break
            zubereitungs_dict[nummer] = schritt
            nummer += 1

        rezepte[name] = {"portionen": portionen, "zubereitungszeit": zubereitungszeit, "verderblichkeit": verderblichkeit, "zutaten": zutaten_dict, "zubereitung": zubereitungs_dict}
        
        bib_speichern()

        while True:
            print("Möchtest du ein weiteres Rezept eingeben?")
            print("1. Ja.")
            print("2. Nein.")
            
            try:
                wahl_nächste = int(input("> "))
                if wahl_nächste == 1:
                    print("Beginnen wir mit deinem nächsten Rezept.")
                    break
                elif wahl_nächste == 2:
                    print("Du kehrst zurück ins Hauptmenu.")
                    hauptmenu()
                    return rezepte
                else:
                    print("Bitte gib 1 oder 2 an.")
            except ValueError: 
                print("Ungültige Eingabe. Bitte gib eine Zahl ein.")

# Hauptmenü
def hauptmenu():
    while True:
        print("\n🌟 Willkommen zu deiner Rezept-Bibliothek! 🌟")
        print("\nWas möchtest du gerne tun?")
        print("1️⃣ Ein Rezept anzeigen lassen")
        print("2️⃣ Ein neues Rezept hinzufügen")
        print("3️⃣ Meinen Wochenplan öffnen")
        print("4️⃣ Meine Einkaufsliste öffnen")
        print("5️⃣ Die App beenden")

        try:
            wahl = int(input("\nDeine Auswahl > "))

            if wahl == 1:
                rezept_anzeigen()
            elif wahl == 2:
                neues_rezept()
            elif wahl == 3:
                wochenplan()
            elif wahl == 4:
                einkaufsliste()
            elif wahl == 5:
                print("\n👋 Du beendest die App. Bis zum nächsten Mal!")
                break
            else:
                print("\n⚠ Ungültige Eingabe. Bitte wähle eine Zahl zwischen 1 und 5.")

        except ValueError:
            print("\n⚠ Fehler: Bitte gib eine gültige Zahl ein.")

        input("\n🔄 Drücke ENTER, um zurück ins Hauptmenü zu gelangen...")

# App starten
if __name__ == "__main__":
    bib_laden()
    hauptmenu()
