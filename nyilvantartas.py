import sqlite3

con = sqlite3.connect("szamitogepesrendszerek.db")
cur = con.cursor()

data2 = []         # Az utoljára listázott dalok tárolása a lejátszáshoz
current_user = None  # A bejelentkezett felhasználó adatai


def login():
    global current_user
    felhasznalonev = str(input("Név: "))
    jelszo = str(input("Jelszó: "))

    sql = """SELECT nev, onkormanyzat_id, email, telefonszam, felhasznaloi_szint, bejelentkezesi_azonosito
             FROM Felhasznalo
             WHERE Felhasznalo.nev = ? AND Felhasznalo.bejelentkezesi_azonosito = ?"""


    res = cur.execute(sql, (felhasznalonev, jelszo))
    loginData = res.fetchall()

    if len(loginData) > 0:
        current_user = loginData[0]
        print(f"\nSikeres bejelentkezés: {current_user[0]}")
        print("=================================\n")
        return True
    else:
        print("Helytelen belépési adatok")
        return False

def fomenu():
    print("Belépés")
    if not login():  # Ha sikertelen a belépés, azonnal kilép a programból
        con.close()
        return

    menu_actions = {
        1: 'asd',
    }

    running = True
    while running:
        if current_user[4] == 1:
            print("1. Új önkormányzat rögzítése")
            print("2. Új eszköz rögzítése")
            print("3. Új felhasználó hozzáadása")
            print("4. Meglévő felhasználók adatainak szerkesztése")
            print("5. Tervezett karbantartások kezelése")
            print("6. Bejelentett hibák kezelése")

            menu1 = {
                1: 'asd',
            }

        elif current_user[4] == 2:
            print("1. Önkormányzat dolgozóinak megtekintése")
            print("2. Önkormányzat eszközeinek megtekintése")
            print("3. Hibabejelentés")
            print("4. Új felhasználó felvétele az önkormányzathoz")
            print("5. Bejelentett hibák állapotának megtekintése")


        elif current_user[4] == 3:
            print("1. Önkormányzat dolgozóinak megtekintése")
            print("2. Önkormányzat eszközeinek megtekintése")

        try:
            choice = int(input("Válasszon a megadott menüpontok közül: "))
        except ValueError:
            print("Kérjük egy számot adjon meg!")
            print("=================================\n")
            continue

        print("=================================\n")

        action = menu_actions.get(choice)
        if action:
            if action() is False:
                running = False
        else:
            print("\n///////////////////////////")
            print("Nem létező menüpont!")
            print("///////////////////////////\n")

fomenu()

con.close()


