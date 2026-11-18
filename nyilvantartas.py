import sqlite3

con = sqlite3.connect("szamitogepesrendszerek.db")
cur = con.cursor()

data2 = []         # Az utoljára listázott dalok tárolása a lejátszáshoz
jelenlegi_felhasznalo = None  # A bejelentkezett felhasználó adatai


def belepes():
    global jelenlegi_felhasznalo
    felhasznalonev = str(input("Név: "))
    jelszo = str(input("Jelszó: "))

    sql = """SELECT nev, onkormanyzat_id, email, telefonszam, felhasznaloi_szint, bejelentkezesi_azonosito
             FROM Felhasznalo
             WHERE Felhasznalo.nev = ? AND Felhasznalo.bejelentkezesi_azonosito = ?"""


    res = cur.execute(sql, (felhasznalonev, jelszo))
    loginData = res.fetchall()

    if len(loginData) > 0:
        jelenlegi_felhasznalo = loginData[0]
        print(f"\nSikeresen bejelentkezve mint: {jelenlegi_felhasznalo[0]} \n")
        return True
    else:
        print("Helytelen belépési adatok")
        return False

def kilepes():
    print("Kilépés...")
    return False

def uj_onkormanyzat_rogzitese():
    print("-----------------------------------")
    print("Adja meg az új önkormányzat adatait")
    print("-----------------------------------")

    while True:
        u_onkormanyzat_nev = input("Adja meg az önkormányzat nevét: ").strip()

        if not u_onkormanyzat_nev:
            print("\nMeg kell adni az önkormányzat nevét! Próbálja újra.\n")
            continue

        res = cur.execute("SELECT id FROM Onkormanyzat WHERE nev = ?", (u_onkormanyzat_nev,))
        if res.fetchone() is not None:
            print("\nMár létezik ilyen nevű önkormányzat! Adjon meg másikat.\n")
            continue

        break

    u_onkormanyzat_email = input("Adja meg az önkormányzat e-mail címét: ").strip() or None
    u_onkormanyzat_telefonszam = input("Adja meg az önkormányzat telefonszámát: ").strip() or None
    u_onkormanyzat_cim = input("Adja meg az önkormányzat címét: ").strip() or None
    u_onkormanyzat_kapcsolattarto = input("Adja meg az önkormányzat kapcsolattartójának nevét: ").strip() or None

    cur.execute(
        "INSERT INTO Onkormanyzat (nev, email, telefonszam, cim, kapcsolattarto_neve) "
        "VALUES (?, ?, ?, ?, ?)",
        (u_onkormanyzat_nev, u_onkormanyzat_email, u_onkormanyzat_telefonszam, u_onkormanyzat_cim,
         u_onkormanyzat_kapcsolattarto))
    con.commit()
    print("\nSikeresen felvette az új önkormányzatot!\n")

def onkormanyzatok_listaja():
    print()
    res = cur.execute("SELECT nev FROM Onkormanyzat")
    onkormanyzatok = res.fetchall()
    for onkormanyzat in onkormanyzatok:
        print(onkormanyzat[0])

def uj_eszkoz_rogzitese():
    onkormanyzatok_listaja()

    while True:
        keresett_onkormanyzat = input("\nAdja meg az önkormányzat nevét, ahol az eszköz található: ").strip()
        res = cur.execute("SELECT id FROM Onkormanyzat WHERE nev = ?", (keresett_onkormanyzat,))
        talalat = res.fetchone()

        if talalat is not None:
            onkormanyzat_id = talalat[0]
            break
        else:
            print("Nem található ilyen nevű önkormányzat! Próbálja újra.")



    while True:
        u_eszkoz_neve = input("Eszköz neve: ").strip()
        if u_eszkoz_neve:
            break
        print("Az eszköz nevét kötelező megadni!")


    while True:
        try:
            u_leltari_szam = int(input("Leltári szám: ").strip())
            break
        except ValueError:
            print("A leltári számnak egész számnak kell lennie!")

    u_beszerzes_datuma = input("Eszköz beszerzésének dátuma (ÉÉÉÉ-HH-NN): ").strip() or None
    u_eszkoz_leirasa = input("Eszköz leírása: ").strip() or None
    u_tipus = input("Eszköz típus: ").strip() or None

    cur.execute(
        "INSERT INTO Eszkoz (onkormanyzat_id, eszkoz_neve, leltari_szam, beszerzes_datuma, eszkoz_leirasa, tipus) "
        "VALUES (?, ?, ?, ?, ?, ?)",
    (onkormanyzat_id, u_eszkoz_neve, u_leltari_szam, u_beszerzes_datuma, u_eszkoz_leirasa, u_tipus)
    )
    con.commit()
    print("\nEszköz sikeresen rögzítve!\n")

def uj_felhasznalo_hozzaadasa():
    onkormanyzatok_listaja()

    while True:
        keresett_onkormanyzat = input("\nAdja meg az önkormányzat nevét, ahol az eszköz található: ").strip()
        res = cur.execute("SELECT id FROM Onkormanyzat WHERE nev = ?", (keresett_onkormanyzat,))
        talalat = res.fetchone()

        if talalat is not None:
            onkormanyzat_id = talalat[0]
            break
        else:
            print("Nem található ilyen nevű önkormányzat! Próbálja újra.")

#----------------------------------------

def onkormanyzat_dolgozoi():
    onkormanyzat_id = jelenlegi_felhasznalo[1]

    if onkormanyzat_id is None:
        print("Nincs hozzárendelve önkormányzat a felhasználóhoz.")
        return

    sql = """SELECT Onkormanyzat.nev, Felhasznalo.nev, Felhasznalo.email, 
                Felhasznalo.telefonszam, Felhasznalo.felhasznaloi_szint
                FROM Felhasznalo
                INNER JOIN Onkormanyzat ON Felhasznalo.onkormanyzat_id = Onkormanyzat.id
                WHERE Felhasznalo.onkormanyzat_id = ?
                ORDER BY Felhasznalo.nev"""

    res = cur.execute(sql, (onkormanyzat_id,))
    dolgozok_listaja = res.fetchall()

    print("\n-----------------------------------")
    if len(dolgozok_listaja) > 0:
        print(f"{dolgozok_listaja[0][0]} dolgozói:")
        print("-----------------------------------")
        for dolgozo in dolgozok_listaja:
            email = dolgozo[2] if dolgozo[2] else "Nincs megadva"
            tel = dolgozo[3] if dolgozo[3] else "Nincs megadva"
            print(f"Név: {dolgozo[1]} | E-mail: {email} | Tel.: {tel}")
    else:
        print("Nincsenek rögzített dolgozók ehhez az önkormányzathoz.")
    print("-----------------------------------\n")

def onkormanyzat_eszkozei():
    onkormanyzat_id = jelenlegi_felhasznalo[1]

    if onkormanyzat_id is None:
        print("Nincs hozzárendelve önkormányzat a felhasználóhoz.")
        return

    sql = """SELECT Onkormanyzat.nev, Eszkoz.eszkoz_neve, Eszkoz.leltari_szam, 
                Eszkoz.beszerzes_datuma, Eszkoz.eszkoz_leirasa, Eszkoz.tipus
                FROM Eszkoz
                INNER JOIN Onkormanyzat ON Eszkoz.onkormanyzat_id = Onkormanyzat.id
                WHERE Eszkoz.onkormanyzat_id = ?
                ORDER BY Eszkoz.eszkoz_neve"""

    res = cur.execute(sql, (onkormanyzat_id,))
    eszkozok_listaja = res.fetchall()

    print("\n-----------------------------------")
    if len(eszkozok_listaja) > 0:
        print(f"{eszkozok_listaja[0][0]} eszközei:")
        print("-----------------------------------")
        for eszkoz in eszkozok_listaja:
            beszerzes_datuma = eszkoz[3] if eszkoz[3] else "Nincs megadva"
            leiras = eszkoz[4] if eszkoz[4] else "Nincs megadva"
            tipus = eszkoz[5] if eszkoz[5] else "Nincs megadva"
            print(f"Eszköz neve: {eszkoz[1]} | Leltári szám: {eszkoz[2]} | Beszerzés dátuma: {beszerzes_datuma} | Leírás: {leiras} | Típus: {tipus}")
    else:
        print("Nincsenek rögzített eszközök ehhez az önkormányzathoz.")
    print("-----------------------------------\n")

def fomenu():
    print("Belépés")
    if not belepes():
        con.close()
        return

    felhasznaloi_szinthez_tartozo_lehetosegek = 0
    adott_felhasznalohoz_tartozo_menu = {}
    fut = True
    while fut:
        if jelenlegi_felhasznalo[4] == 1:
            print("1. Új önkormányzat rögzítése")
            print("2. Új eszköz rögzítése")
            print("3. Új felhasználó hozzáadása")
            print("4. Meglévő felhasználók adatainak szerkesztése")
            print("5. Tervezett karbantartások kezelése")
            print("6. Bejelentett hibák kezelése")
            print("7. Kilépés")
            felhasznaloi_szinthez_tartozo_lehetosegek = 7

            adott_felhasznalohoz_tartozo_menu = {
                1: uj_onkormanyzat_rogzitese,
                2: uj_eszkoz_rogzitese,
                3: uj_felhasznalo_hozzaadasa,
                # 4: meglevo_felhasznalok_szerkesztese,
                # 5: tervezett_karbantartasok_kezelese,
                # 6: bejelentett_hibak_kezelese,
                7: kilepes,
            }

        elif jelenlegi_felhasznalo[4] == 2:
            print("1. Önkormányzat dolgozóinak megtekintése")
            print("2. Önkormányzat eszközeinek megtekintése")
            print("3. Hibabejelentés")
            print("4. Új felhasználó felvétele az önkormányzathoz")
            print("5. Bejelentett hibák állapotának megtekintése")
            print("6. Kilépés")
            felhasznaloi_szinthez_tartozo_lehetosegek = 6

            adott_felhasznalohoz_tartozo_menu = {
                1: onkormanyzat_dolgozoi,
                2: onkormanyzat_eszkozei,
                # 3: ,
                4: uj_felhasznalo_hozzaadasa,
                # 5: ,
                6: kilepes,
            }

        elif jelenlegi_felhasznalo[4] == 3:
            print("1. Önkormányzat dolgozóinak megtekintése")
            print("2. Önkormányzat eszközeinek megtekintése")
            print("3. Kilépés")
            felhasznaloi_szinthez_tartozo_lehetosegek = 3

            adott_felhasznalohoz_tartozo_menu = {
                1: onkormanyzat_dolgozoi,
                2: onkormanyzat_eszkozei,
                3: kilepes,
            }

        try:
            valasztas = int(input(f"\nVálasszon a megadott menüpontok közül (1-{felhasznaloi_szinthez_tartozo_lehetosegek}): "))
        except ValueError:
            print("\n****************************")
            print("Kérjük egy számot adjon meg!")
            print("****************************\n")
            continue

        milyen_felhasznalo = adott_felhasznalohoz_tartozo_menu.get(valasztas)
        if milyen_felhasznalo:
            if milyen_felhasznalo() is False:
                fut = False
        else:
            print("\n********************")
            print("Nem létező menüpont!")
            print("********************\n")

fomenu()

con.close()




