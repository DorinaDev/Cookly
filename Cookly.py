# Rezept-Bibliothek
rezepte = {
    "Lasagne-Suppe": {
        "portionen": 4, # Standard Portionen
        "zubereitungszeit": "30 Min.",
        "verderblichkeit": "2", # Wert zwischen 1-3 (1 = Nur Konserven, 2 = Haltbares Gemüse, 3 = Leicht verderbliche Lebensmittel)
        "zutaten": {
            "Zwiebel": (1, ""),
            "Knoblauch": (1, ""),
            "Paprika": (1, ""),
            "Karotte": (1, ""),
            "Öl": (2, "EL"),
            "Hackfleisch": (400, "g"),
            "Passierte Tomaten": (400, "g"),
            "Gemüsebrühe": (500, "ml"),
            "Lasagneblätter": (6, ""),
            "Paprikapulver": (2, "TL"),
            "Creme fraiche": (1, "EL"),
            "Parmesan, gerieben": (30, "g")
        },
        "zubereitung": {
            1: "Zwiebel und Knoblauch abziehen und klein hacken. Paprika und Karotte waschen, Paprika entkernen und Karotte schälen. Beiden würfeln.",
            2: "Zwiebeln, Knoblauch und Hackfleisch in etwas Öl anbraten. Karotte, Paprika und passierte Tomaten dazugeben und mit Gemüsebrühe aufgießen - alles gut würzen.",
            3: "Die Lasagneblätter in Stücke brechen, einrühren und für ca. 10-15 Min. zugedeckt köcheln lassen.",
            4: "Sobald die Lasagneblätter gar sind, die Suppe mit Creme fraiche und Parmesan verfeinern und genießen."
        }
    }
}

Wochenplan = {} 
Einkaufsliste = {}

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
                # Hier fehlt noch die Funktion, um es dem Wochenplan hinzuzufügen.
            else:
                print("Okay, dann vielleicht später!")

        else:
            print("Dieses Rezept befindet sich nicht in der Bibliothek. Überprüfe die Rechtschreibung.")

# Wochenplan erstellen
def wochenplan():
    print("") # Verderblichkeit der Lebensmittel sollte berücksichtigt werden.

# Einkaufsliste erstellen
def einkaufsliste():
    print("")
    print("Möchtest du deine Einkaufsliste an bring! übergeben?") # Ist das möglich?

# Neues Rezept hinzufügen
def neues_rezept(rezepte):
    zutaten_liste = []
    zubereitungs_liste = []
    zubereitungs_dict = {}
    zutaten_dict = {}

    while True: 
        print("Welches Rezept möchtest du hinzufügen?")
        name = input("Name: ")
        print("Für wie viele Portionen ist das Rezept ausgelegt?")
        while True: 
            try:
                portionen = int(input("Portionen: "))
                if portionen > 0:
                    break
                else:
                    print("Bitte gib eine Zahl ein.")
            except ValueError: 
                print("Ungültige Eingabe. Bitte gib eine Zahl ein, die größer als 0 ist.")

        print("Wie lange dauert es das Rezept zuzubereiten?")
        zubereitungszeit = input("Zubereitungszeit: ")
        print("Wie verderblich sind die Zutaten für das Rezept?")
        print("Bitte gib an: 1 = Nur Konserven, 2 = Haltbares Gemüse, 3 = Leicht verderbliche Lebensmittel")
        print("Das hilft deiner App dabei besser zu kalkukulieren, wenn du einen Wochenplan erstellen möchtest.")
        verderblichkeit = input("Verderblichkeit: ")
        print("Nun kannst du die Zutaten hinzufügen.")
        
        while True: 
            zutat = input("Bitte gib eine Zutat ein (oder 'fertig', um abzuschließen): ")
            if zutat.lower() == "fertig":
                break
            else:
                menge = input(f"Gib die Menge für {zutat} ein: ")
                einheit = input(f"Gib die Einheit für {zutat} ein (z.B. g, ml, EL): ")
                zutaten_liste.append((zutat, menge, einheit))

        for zutat, menge, einheit in zutaten_liste:
            zutaten_dict[zutat] = (menge, einheit)

        print("Nun kannst du die Verarbeitungsschritte eingeben.")
        while True: 
            zubereitung = input("Bitte gib die Verarbeitungsschritte der Reihe nach ein (oder 'fertig', um abzuschließen): ")
            if zubereitung.lower() == "fertig":
                break
            zubereitungs_liste.append(zubereitung)

        for nummer, schritt in enumerate(zubereitungs_liste, start=1):
            zubereitungs_dict[nummer] = schritt

        rezepte[name] = {"portionen": portionen, "zubereitungszeit": zubereitungszeit, "verderblichkeit": verderblichkeit, "zutaten": zutaten_dict, "zubereitung": zubereitungs_dict}
        
        # An dieser Stelle sollte gespeichert werden.

        while True:
            print("Möchtest du ein weitere Rezept eingeben?")
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
            except ValueError: 
                print("Bitte gib eine Zahl ein.")

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
rezept_anzeigen()
