import random
import json
import os

points = 0
difficulty = 1
inventory = []
name = None
gold = 0
level = 1
xp = 0

level_thresholds = {
    1: 0,
    2: 100,
    3: 250,
    4: 450,
    5: 700,
    6: 1000,
    7: 1400,
    8: 1900,
    9: 2500,
    10: 3200
}

monsters = {
    # DUNKLER WALD (Level 1-3)
    "Schleim": {
        "lifepoints": (5, 10),
        "damage": (1, 5),
        "lore": "Ein blauer Schleim kommt und versperrt dir den Weg. \nEr sieht aus als hätte er einen schlechten Tag."
    },
    "Goblin": {
        "lifepoints": (10, 15),
        "damage": (5, 10),
        "lore": "Ein Goblin springt aus dem Gebüsch!\nEr riecht nach alten Socken."
    },

    # VERFLUCHTE BERGE (Level 4-6)
    "Fledermaus": {
        "lifepoints": (15, 20),
        "damage": (10, 15),
        "lore": "Eine flattrige Fledermaus greift dich an.\nSie will wahrscheinlich dein Blut."
    },
    "Wolf": {
        "lifepoints": (15, 20),
        "damage": (8, 14),
        "lore": "Ein grauer Wolf knurrt dich an.\nSeine Augen leuchten im Dunkeln."
    },

    # WUESTE DER VERLORENEN (Level 7-9)
    "Skorpion": {
        "lifepoints": (20, 25),
        "damage": (12, 18),
        "lore": "Ein riesiger Skorpion kriecht aus dem Sand.\nSein Stachel tropft vor Gift."
    },
    "Drache": {
        "lifepoints": (20, 25),
        "damage": (15, 20),
        "lore": "Ein Drache bewacht den Eingang. Er ist müde und hat eigentlich keinen Bock!"
    },

    # GRUSELIGER FRIEDHOF (Level 5 - Einmalig)
    "Geist": {
        "lifepoints": (18, 22),
        "damage": (12, 18),
        "lore": "Ein blasser Geist schwebt durch die Grabsteine.\nEr murmelt unverständliche Worte..."
    },
    "Skelett": {
        "lifepoints": (15, 20),
        "damage": (10, 16),
        "lore": "Ein klapperndes Skelett erhebt sich aus dem Grab.\nDie Knochen rasseln bedrohlich."
    },
}


def remove_game():
    if os.path.exists("savegame.json"):
        os.remove("savegame.json")
        print("Spielstand gelöscht!")
    else:
        print("Kein Spielstand vorhanden.")


def save_game():
    global name, points, difficulty, inventory, level, xp, gold
    data = {
        "name": name,
        "points": points,
        "difficulty": difficulty,
        "inventory": inventory,
        "level": level,
        "xp": xp,
        "gold": gold,
    }
    with open("savegame.json", "w") as file:
        json.dump(data, file)
    print("Spiel gespeichert!")


def load_game():
    global name, points, difficulty, inventory, level, xp, gold
    try:
        with open("savegame.json", "r") as file:
            data = json.load(file)
        name = data["name"]
        points = data["points"]
        difficulty = data["difficulty"]
        inventory = data["inventory"]
        level = data["level"]
        xp = data["xp"]
        gold = data["gold"]
        print(f"Spiel geladen! Willkommen zurück, {name}")
    except FileNotFoundError:
        print("Kein Savegame gefunden.")


while True:
    print("\n==== Menü ====")
    print("\n1= Start")
    print("2= Schwierigkeitsgrad")
    print("3= Inventar")
    print("4= Punktestand")
    print("5= Spiel laden")
    print("6= Spiel speichern")
    print("7= Spielstand löschen")
    print("8= Beenden")

    number = input("\nWas willst du tun? ")

    match number:
        case "1":
            bonus_damage = 0
            keep_fighting = True

            if name is None:
                name = input("Wie heißt du? ")
                print(f"""\nIn der Welt von Zylon existieren viele Legenden.
Die meisten davon sind falsch.
Eine davon... vielleicht nicht.

Die Legende der Goldenen Milch.

Man sagt, wer sie trinkt, schnurrt für immer glücklich.
Man sagt, sie liegt verborgen in der Goldenen Zitadelle.

Du, {name}, ein junges Kätzchen aus Sonnenhain, hast
dich entschlossen dass du nun alt genug bist um danach zu suchen.
Voller Stolz hast du einen Beutel genommen und deine Lieblingsmaus,
einen Fisch und etwas Milch eingepackt und bist gegangen.

Sonnenhain liegt hinter dir.
Das große Abenteuer liegt vor dir.
Und irgendwo tief in Zylon warten Gefahren auf dich.

Viel Erfolg, {name}.
Du wirst es brauchen.
""")
            else:
                print(f"Willkommen zurück, {name}")

            while keep_fighting:
                bonus_damage = 0

                if level == 10:
                    print("""
Die Goldene Zitadelle liegt vor dir.
Du öffnest das schwere Tor und...

Ein RIESIGER oranger Kater blockiert den Weg.
Er liegt auf einem goldenen Kissen.
Neben ihm: Die Goldene Milch.

Er hebt langsam den Kopf.
Schaut dich an.
Gelangweilt, so als wärst du es nicht wert diese monströse Flauschigkeit anzusehen.

"Pathetic."
                    """)

                    monster_name = "Der Chonk"
                    monster_lifepoints = 100
                    monster_damage_range = (20, 30)
                    monster_strength = monster_lifepoints

                    print(f"\n{monster_name} erhebt sich majestätisch!")
                    print(f"Er hat {monster_lifepoints} Leben!")

                else:
                    # Gebiet basierend auf Level bestimmen
                    if level <= 3:
                        # DUNKLER WALD
                        print("\n=== Dunkler Wald ===")
                        print(""" Der dunkle Wald ist dafür bekannt das seine Bäume so hoch und dicht wachsen,
                         das es dort wie immer Nacht wirkt. In dem Wald gibt es kaum fröhliche Geräusche von 
                         Vögeln oder anderen friedlichen Waldtieren. In diesem Wald leben Schleime und Goblins.
                         Sei vorsichtig kleines Kätzchen.""")
                        available_monsters = ["Schleim", "Goblin"]

                    elif level == 4 or level == 6:
                        # VERFLUCHTE BERGE
                        print("\n=== Verfluchten Berge ===")
                        print(""" Dein Weg führt dich weiter zu den verfluchten Bergen. Aber warum trägt er diesen Namen?
                         Tief in der Berglandschaft versteckt liegt der gruselige Friedhof. Niemand traut sich mehr dorthin
                         und so konnten Fledermäuse und Wölfe sich frei vermehren und greifen jeden an der sich ihrem Gebiet nähert.""")
                        available_monsters = ["Fledermaus", "Wolf"]

                    elif level == 5:
                        # GRUSELIGER FRIEDHOF (Einmalig!)
                        print("\n=== Der gruseligen Friedhof ===")
                        print(""" Du hast die Mitte der Berge erreicht und vor dir liegt der Friedhof. Eine alte Hexe hat ihn damals verflucht,
                         Seitdem leben dort verlorene Seelen als Geister und erschrecken jeden der es wagt diesen Friedhof zu überqueren.
                         Manchmal erscheinen auch Skelette die auf der suche nach neuen Knochen die Reisenden angreifen.""")
                        available_monsters = ["Geist", "Skelett"]

                    elif 7 <= level <= 9:
                        # WUESTE DER VERLORENEN
                        print("\n=== die Wüste der Verlorenen ===")
                        print(""" Du bist nun kurz vor deinem Ziel. Vor dir erstreckt sich die Wüste der Verlorenen. Viele sind in der sengenden 
                         Hitze verloren gegangen und gestorben. Doch du, kleiner Held, scheinst mutig genug zu sein und 
                         wagst dich durch die Wüste. Hier werden dir Skorpione und Drachen begegnen. Achte auf deine
                         Lieblingsmaus und deine Milch. Bald bist du dem Ziel nahe.""")
                        available_monsters = ["Skorpion", "Drache"]

                    else:
                        # Fallback
                        available_monsters = ["Schleim", "Goblin"]

                    # Monster spawnen
                    monster_name = random.choice(available_monsters)
                    lp_min, lp_max = monsters[monster_name]["lifepoints"]

                    if monster_name != "Schleim":
                        lp_min += (level * 2)
                        lp_max += (level * 2)

                    monster_lifepoints = random.randint(lp_min, lp_max)

                    damage_min, damage_max = monsters[monster_name]["damage"]

                    if monster_name != "Schleim":
                        damage_min += level
                        damage_max += level

                    monster_damage_range = (damage_min, damage_max)
                    monster_strength = monster_lifepoints

                    print(monsters[monster_name]["lore"])
                    print(f"{monster_name} hat {monster_lifepoints} Leben!")

                player_lifepoints = 30 + (level * 5) - (difficulty * 3)
                print(f"{name} hat {player_lifepoints} Leben.")

                while monster_lifepoints > 0:
                    print("\nWas möchtest du machen?")
                    print("1= Angreifen")
                    print("2= Fliehen")
                    print("3= Inventar")
                    print("4= Beenden")

                    action = input("\nDeine Wahl: ")

                    match action:
                        case "1":
                            attack_points = random.randint(1 + level, 9 + level) + bonus_damage

                            if difficulty == 1:
                                crit_chance = random.randint(1, 5)
                            elif difficulty == 2:
                                crit_chance = random.randint(1, 10)
                            else:
                                crit_chance = random.randint(1, 15)

                            if crit_chance == 1:
                                attack_points *= 2
                                print("Kritischer Treffer!!")

                            bonus_damage = 0

                            if random.randint(1, 5) == 1:
                                print(f"{monster_name} weicht aus!")
                            else:
                                monster_lifepoints -= attack_points
                                print(f"Du machst {attack_points} Schaden!")

                                if monster_lifepoints <= 0:
                                    # BOSS BESIEGT = SPIEL GEWONNEN!
                                    if monster_name == "Der Chonk":
                                        print(f"""
{monster_name} seufzt und legt sich wieder hin.

"Du hast gewonnen... *gähn*
 Nimm die Milch und verschwinde.
 Ich will schlafen."

Du nimmst die Goldene Milch.
Sie funkelt in deinen Pfoten.
Du nippst daran...

...

{name} schnurrt.
Für immer glücklich.

ZYLON IST GERETTET!
Du hast das Spiel gewonnen!
                                        """)
                                        keep_fighting = False
                                        break

                                    # Normale Monster besiegt
                                    reward = monster_strength * 1.5 * difficulty
                                    points += reward
                                    xp += int(reward)
                                    print(f"Du bekommst {int(reward)} XP!")

                                    if level < 10 and xp >= level_thresholds[level + 1]:
                                        level += 1
                                        print(f"""
LEVEL UP! Du bist jetzt Level {level}!
{name} schnurrt stolz vor sich hin!
""")
                                        if level < 10:
                                            next_level_xp = level_thresholds[level + 1]
                                            xp_needed = next_level_xp - xp
                                            print(f"Bis Level {level + 1}: noch {xp_needed} XP")
                                        else:
                                            print("MAX LEVEL erreicht! Die Goldene Zitadelle wartet!")

                                    loot = random.choice(["Heiltrank", "Schwertsplitter"])
                                    inventory.append(loot)

                                    new_gold = random.randint(1, 10)
                                    gold += new_gold

                                    print(f"{monster_name} ist besiegt! Du bekommst {reward} Punkte!")
                                    print(f"Du hast {loot} gefunden!")
                                    print(f"Du hast {new_gold} Gold gefunden! (Gesamt: {gold})")
                                    print(f"\nAktueller Punktestand: {points}")
                                    print("\nWas möchtest du tun?")
                                    print("1= Weiter kämpfen")
                                    print("2= Shop besuchen")
                                    print("3= Zurück zum Menü")

                                    after_fight = input("\nDeine Wahl: ")
                                    match after_fight:
                                        case "1":
                                            break
                                        case "2":
                                            print("\n==== SHOP =====")
                                            print("\nHerzlich Willkommen beim fahrendem Händler")
                                            print(f"\nDein Gold: {gold}")
                                            print("==========================")
                                            print("1= Heiltrank (7 Gold)")
                                            print("2= Schwertsplitter (5 Gold)")
                                            buy = input("\nDeine Wahl: ")
                                            match buy:
                                                case "1":
                                                    if gold >= 7:
                                                        gold -= 7
                                                        inventory.append("Heiltrank")
                                                        print("Heiltrank gekauft!")
                                                    else:
                                                        print("Nicht genügend Gold")
                                                case "2":
                                                    if gold >= 5:
                                                        gold -= 5
                                                        inventory.append("Schwertsplitter")
                                                        print("Schwertsplitter gekauft!")
                                                    else:
                                                        print("Nicht genügend Gold.")
                                                case _:
                                                    print("Ungültige Eingabe")
                                            break
                                        case "3":
                                            keep_fighting = False
                                            break

                                print(f"{monster_name} hat noch {monster_lifepoints} Leben")
                                damage_min, damage_max = monster_damage_range
                                monster_attack = random.randint(damage_min, damage_max)
                                player_lifepoints -= monster_attack
                                print(f"{monster_name} greift {name} an und macht {monster_attack} Schaden!")
                                print(f"\n{name} hat noch {player_lifepoints} Leben")
                                if player_lifepoints <= 0:
                                    print(f"{name} ist besiegt. Game over!")
                                    keep_fighting = False
                                    break

                        case "2":
                            if random.randint(1, 2) == 1:
                                print("Du bist geflohen!")
                                break
                            else:
                                print(f"Flucht fehlgeschlagen! Das {monster_name} greift dich an!")
                                damage_min, damage_max = monster_damage_range
                                monster_attack = random.randint(damage_min, damage_max)
                                player_lifepoints -= monster_attack
                                print(f"{monster_name} macht {monster_attack} Schaden!")
                                print(f"Du hast noch {player_lifepoints} Leben!")
                                if player_lifepoints <= 0:
                                    print(f"{name} ist besiegt. Game over!")
                                    keep_fighting = False
                                    break

                        case "3":
                            print("\nWelches Item willst du benutzen?")
                            options = {}
                            if "Heiltrank" in inventory:
                                print("1= Heiltrank (5+ Leben)")
                                options["1"] = "Heiltrank"
                            if "Schwertsplitter" in inventory:
                                print("2= Schwertsplitter (+5 Schaden)")
                                options["2"] = "Schwertsplitter"
                            if not options:
                                print("Du hast keine Items!")
                                continue
                            item_choice = input("\nDeine Wahl: ")
                            if item_choice in options:
                                item = options[item_choice]
                                if item == "Heiltrank":
                                    old_hp = player_lifepoints
                                    max_hp = 30 + (level * 5) - (difficulty * 3)
                                    player_lifepoints = min(player_lifepoints + 5, max_hp)
                                    inventory.remove("Heiltrank")
                                    print(f"Heiltrank benutzt! {old_hp} -> {player_lifepoints} Leben")
                                elif item == "Schwertsplitter":
                                    bonus_damage += 5
                                    inventory.remove("Schwertsplitter")
                                    print("Schwertsplitter benutzt!")
                            else:
                                print("Ungültige Eingabe")

                        case "4":
                            print("Game Over")
                            keep_fighting = False
                            break

                        case _:
                            print("Ungültige Eingabe")

        case "2":
            print("\n1= leicht")
            print("2= normal")
            print("3= schwer")
            choice = input("\nSchwierigkeitsgrad: ")
            match choice:
                case "1":
                    difficulty = 1
                case "2":
                    difficulty = 2
                case "3":
                    difficulty = 3
                case _:
                    print("Ungültige Eingabe")

        case "3":
            print("\n====INVENTAR====")
            if len(inventory) == 0:
                print("Inventar ist leer")
            else:
                for item in inventory:
                    print(f"- {item}")

        case "4":
            if name is not None:
                print(f"\n==== SPIELER {name} STATUS====")
            else:
                print("\n==== SPIELER STATUS====")
            print(f"Aktueller Punktestand: {points}")
            print(f"Schwierigkeitsgrad: {difficulty}")
            print(f"Vermögen: {gold} Gold")
            print(f"Level: {level}")
            print(f"XP: {xp} XP")

            if level < 10:
                next_level_xp = level_thresholds[level + 1]
                xp_needed = next_level_xp - xp
                print(f"Bis Level {level + 1}: noch {xp_needed} XP")
            else:
                print("MAX LEVEL erreicht! Die Goldene Zitadelle wartet!")
            print("--------------------------\n")

        case "5":
            load_game()

        case "6":
            save_game()

        case "7":
            remove_game()

        case "8":
            print("Spiel wird beendet...")
            break

        case _:
            print("Ungültige Eingabe")
