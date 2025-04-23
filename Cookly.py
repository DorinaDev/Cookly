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
finaler_wochenplan = {}
einkaufsliste_list = {}

# Speicherfunktion
def bib_speichern():
    daten = {"rezepte": rezepte, "finaler_wochenplan": finaler_wochenplan, "wochenplan": wochenplan_list, "einkaufsliste": einkaufsliste_list}

    try:
        with open("bib.json", "w", encoding="utf-8") as datei:
            json.dump(daten, datei, indent=4)

        print("Deine Rezeptbibliothek wurde gespeichert.")

    except Exception as e:
        print(f"Fehler beim Speichern: {e}.")

# Bib Laden
def bib_laden():
    global rezepte, finaler_wochenplan, wochenplan_list, einkaufsliste_list
    
    try:
        with open("bib.json", "r", encoding="utf-8") as datei:
            daten = json.load(datei)

        rezepte = daten.get("rezepte", {})
        wochenplan_list = daten.get("wochenplan", [])
        einkaufsliste_list = daten.get("einkaufsliste", {})
        finaler_wochenplan = daten.get("finaler_wochenplan", {})

        print("\nDeine Rezeptbibliothek wurde geladen.")

    except FileNotFoundError:
        print("\nKein gespeicherter Speicherstand gefunden.")
    except json.JSONDecodeError:
        print("Fehler: Die Datei ist beschädigt oder ungültig.")

# Rezept-Ausgabe
def rezept_anzeigen():
    while True: 
        wahl = input("Welches Rezept möchtest du anzeigen lassen? \n> ").lower()
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
            else:
                print("Okay, dann vielleicht später!")
        else:
            print("Dieses Rezept befindet sich nicht in der Bibliothek. Überprüfe die Rechtschreibung.")

        print("Möchtest du ein weitere Rezept anzeigen lassen? (ja/nein)")
        while True:
            try:
                weiteres_rezept = input("> ").lower()
                if weiteres_rezept == "nein":
                    return
                if weiteres_rezept == "ja":
                    continue
                else:
                    print("Bitte gib 'ja' oder 'nein' ein.")
            except ValueError:
                print("Ungültige Eingabe. Bitte gib 'ja' oder 'nein' ein.")

# Sortierung für den Wochenplan
def sort_wochenplan(auswahl):
    sortierung_verderblichkeit = sorted(auswahl, key=lambda gericht: rezepte[gericht]["verderblichkeit"], reverse=True)

    finale_liste = sortierung_verderblichkeit[:]

    i = 0
    while len(finale_liste) < 7 and i < len(sortierung_verderblichkeit) - 1:
        pos = finale_liste.index(sortierung_verderblichkeit[i])
        finale_liste.insert(pos + 1, sortierung_verderblichkeit[i])
        i += 1

    while len(finale_liste) < 7:
        finale_liste.append(sortierung_verderblichkeit[-1])

    return finale_liste

# Wochenplan
def wochenplan():
    global finaler_wochenplan

    tage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    auswahl = []

    if not wochenplan_list:
        print("Deine Wochenplan-Liste ist noch leer.")
        return
    
    print(f"Auf deiner Wochenplan-Liste befinden sich die folgenden Rezepte:")
    wochenplan_dict = {i + 1: rezept for i, rezept in enumerate(wochenplan_list)}

    for key, value in wochenplan_dict.items():
        print(f"{key}. {value}")
    
    while len(auswahl) < 7:
        print("Wähle nun bis zu 7 Gerichte für deinen Wochenplan aus.")
        eingabe = input("Bitte gib die Nummer eines Gerichtes ein (oder 'fertig' wenn du genug Gerichte ausgewählt hast)\n> ")
            
        if eingabe.lower() == "fertig":
            if len(auswahl) == 0:
                print("Du musst mindestens ein Gericht eingeben.")
                continue
            break
            
        try:
            nummer = int(eingabe)
            if nummer in wochenplan_dict:
                gericht = wochenplan_dict[nummer]
                if gericht in auswahl:
                    print("Dieses Gericht hast du schon ausgewählt.")
                else:
                    auswahl.append(wochenplan_dict[nummer])
                    print(f"Du hast {wochenplan_dict[nummer]} erfolgreich hinzugefügt.")
            else:
                print("Diese Nummer gibt es nicht.")
        except ValueError: 
            print("Bitte gib eine Zahl ein.")

    finale_liste = sort_wochenplan(auswahl)

    for i, tag in enumerate(tage):
        finaler_wochenplan[tag] = finale_liste[i]

    bib_speichern()

    print("\n🗓️ Dein optimierter Wochenplan:\n")
    for tag, gericht in finaler_wochenplan.items():
        print(f"{tag:<10}: {gericht}")

# Einkaufsliste (in Arbeit)
def einkaufsliste(finaler_wochenplan):
    global rezepte, einkaufsliste_list

    print("Hier kannst du eine Einkaufsliste für die geplanten Gerichte dieser Woche ausgeben lassen.")

    # Abfrage der Personenzahl
    print("Zuerst musst du entscheiden, wie viele Personen an welchen Tagen mitessen sollen.")
    print("Wie möchtest du deinen Plan erstellen? Wähle zwischen 1. und 2.")
    print("1. Für die gesamte Woche bleibt die Personenzahl gleich.")
    print("2. Ich möchte für jeden Tag eine andere Personenzahl angeben.")
    
    while True:
        try:
            wahl = input("> ")
            if wahl == "1":
                portionen_gesamt = int(input("Die Personenzahl für diese Woche lautet: "))
                # Faktorberechnung
                faktoren = {}
                for tag, gericht in finaler_wochenplan.items():
                    portionen_im_rezept = rezepte[gericht]["portionen"]
                    faktor = portionen_gesamt / portionen_im_rezept
                    faktoren[tag] = faktor

                # Zutatenmenge anhand der Portionenanzahl berechnen
                for tag, gericht in finaler_wochenplan.items():
                    rezept = rezepte[gericht]
                    faktor = faktoren[tag]

                    for zutat, (menge, einheit) in rezept["zutaten"].items():
                        angepasste_menge = round(menge * faktor, 1)

                        if zutat in einkaufsliste_list:
                            einkaufsliste_list[zutat][0] += angepasste_menge
                        else:
                            einkaufsliste_list[zutat] = [angepasste_menge, einheit]
                print("\nDeine Einkaufsliste für diese Woche:")
                for zutat, (menge, einheit) in einkaufsliste_list.items():
                    print(f"- {menge} {einheit} {zutat}")
                bib_speichern()
                break

            elif wahl == "2":
                portionen_unterschied = {}
                portionen_mo = int(input("Wie viele Personen essen am Montag mit? > "))
                portionen_unterschied["Montag"] = portionen_mo
                portionen_di = int(input("Wie viele Personen essen am Dienstag mit? > "))
                portionen_unterschied["Dienstag"] = portionen_di
                portionen_mi = int(input("Wie viele Personen essen am Mittwoch mit? > "))
                portionen_unterschied["Mittwoch"] = portionen_mi
                portionen_do = int(input("Wie viele Personen essen am Donnerstag mit? > "))
                portionen_unterschied["Donnerstag"] = portionen_do
                portionen_fr = int(input("Wie viele Personen essen am Freitag mit? > "))
                portionen_unterschied["Freitag"] = portionen_fr
                portionen_sa = int(input("Wie viele Personen essen am Samstag mit? > "))
                portionen_unterschied["Samstag"] = portionen_sa
                portionen_so = int(input("Wie viele Personen essen am Sonntag mit? > "))
                portionen_unterschied["Sonntag"] = portionen_so

                # Faktorberechnung
                faktoren = {}
                for tag, gericht in finaler_wochenplan.items():
                    portionen_im_rezept = rezepte[gericht]["portionen"]
                    faktor = portionen_unterschied[tag] / portionen_im_rezept
                    faktoren[tag] = faktor

                # Zutatenmenge anhand der Portionenanzahl berechnen
                for tag, gericht in finaler_wochenplan.items():
                    rezept = rezepte[gericht]
                    faktor = faktoren[tag]

                    for zutat, (menge, einheit) in rezept["zutaten"].items():
                        angepasste_menge = round(menge * faktor, 1)

                        if zutat in einkaufsliste_list:
                            einkaufsliste_list[zutat][0] += angepasste_menge
                        else:
                            einkaufsliste_list[zutat] = [angepasste_menge, einheit]
                print("\nDeine Einkaufsliste für diese Woche:")
                for zutat, (menge, einheit) in einkaufsliste_list.items():
                    print(f"- {menge} {einheit} {zutat}")
                bib_speichern()
                break
            else:
                print("Ungültige Eingabe. Bitte entscheide dich zwischen 1. und 2.")
        except ValueError: 
            print("Ungültige Eingabe. Bitte gib eine Zahl an.")

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
            try:
                menge = float(input(f"Gib die Menge für {zutat} ein: "))
            except ValueError:
                print("Ungültige Zahl, bitte erneut eingeben.")
                continue
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

        rezepte[name.lower()] = {"portionen": portionen, "zubereitungszeit": zubereitungszeit, "verderblichkeit": verderblichkeit, "zutaten": zutaten_dict, "zubereitung": zubereitungs_dict}
        
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

# Wochenplan und Einkaufsliste PDF erstellen
from fpdf import FPDF
from datetime import datetime

def pdf_wochenplan():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    datum = datetime.now().strftime("%d.%m.%Y")

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"Wochenplan ab {datum}", ln=True)

    pdf.set_font("Arial", size=12)
    for tag, gericht in finaler_wochenplan.items():
        pdf.cell(0, 10, f"{tag}: {gericht}", ln=True)

    pdf.output("Wochenplan.pdf")
    print("PDF für den Wochenplan wurde erstellt.")

def pdf_einkaufsliste():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    datum = datetime.now().strftime("%d.%m.%Y")

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"Einkaufsliste ab {datum}", ln=True)

    pdf.set_font("Arial", size=12)
    for zutat, (menge, einheit) in einkaufsliste_list.items():
        pdf.cell(0, 10, f"{menge} {einheit} {zutat}", ln=True)

    pdf.output("einkaufsliste.pdf")
    print("PDF für die Einkaufsliste wurde erstellt.")

# Check: Schon wieder Montag?
def wochen_check():
    import os

    # Datei mit Datum bereits vorhanden?
    letzte_woche_datei = "letzte_woche.txt"
    heute = datetime.now()
    aktuelle_kw = heute.isocalender()[1]

    letzte_kw = None
    if os.path.exists(letzte_woche_datei):
        with open(letzte_woche_datei, "r") as f:
            letzte_kw = int(f.read().strip())
    if letzte_kw != aktuelle_kw:
        print(f"\nEine neue Woche ist gestartet! (KW {aktuelle_kw})")
        print("Möchtest du den alten Wochenplan und die Einkaufsliste als PDF speichern, bevor alles zurückgesetzt wird? (ja/nein)")
        if input("> ").lower() == "ja":
            pdf_wochenplan()
            pdf_einkaufsliste()

        # Wochenplan und Einkaufsliste zurücksetzen
        wochenplan_list.clear()
        finaler_wochenplan.clear()
        einkaufsliste_list.clear()

        bib_speichern()

        # Neues Datum wird gespeichert
        with open(letzte_woche_datei, "w") as f:
            f.write(str(aktuelle_kw))

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
                neues_rezept(rezepte)
            elif wahl == 3:
                wochenplan()
            elif wahl == 4:
                einkaufsliste(finaler_wochenplan)
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
    wochen_check()
    bib_laden()
    hauptmenu()
