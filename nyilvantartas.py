import sqlite3
from datetime import date

con = sqlite3.connect("szamitogepesrendszerek.db")
cur = con.cursor()
cur.execute("PRAGMA foreign_keys = ON")

jelenlegi_felhasznalo = None
#általános----------------------------------------------------------
def belepes():
    global jelenlegi_felhasznalo
    felhasznalonev = str(input("Név: "))
    jelszo = str(input("Jelszó: "))

    res = cur.execute("""   SELECT nev, onkormanyzat_id, email, telefonszam, felhasznaloi_szint, bejelentkezesi_azonosito, id
                                FROM Felhasznalo
                                WHERE Felhasznalo.nev = ? AND Felhasznalo.bejelentkezesi_azonosito = ?""",
                      (felhasznalonev, jelszo))
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
#általános----------------------------------------------------------


#rendszergazda------------------------------------------------------
def onkormanyzatok_listaja():
    print()
    res = cur.execute("SELECT nev FROM Onkormanyzat")
    onkormanyzatok = res.fetchall()
    for onkormanyzat in onkormanyzatok:
        print(onkormanyzat[0])
def uj_felhasznalo_hozzaadasa():
    if jelenlegi_felhasznalo[4] == 2:
        onkormanyzat_id = jelenlegi_felhasznalo[1]
        if onkormanyzat_id is None:
            print("Nincs hozzárendelve önkormányzat a felhasználóhoz.")
            return
    else:
        onkormanyzatok_listaja()
        while True:
            keresett_onkormanyzat = input(
                "\nAdja meg az önkormányzat nevét, ahova a felhasználót rögzíteni szeretné: ").strip()
            res = cur.execute("SELECT id FROM Onkormanyzat WHERE nev = ?", (keresett_onkormanyzat,))
            talalat = res.fetchone()
            if talalat is not None:
                onkormanyzat_id = talalat[0]
                break
            else:
                print("Nem található ilyen nevű önkormányzat! Próbálja újra.")

    while True:
        keresett_onkormanyzat = input("\nAdja meg az önkormányzat nevét, ahova a felhasználót rögzíteni szeretné: ").strip()
        res = cur.execute("SELECT id FROM Onkormanyzat WHERE nev = ?", (keresett_onkormanyzat,))
        talalat = res.fetchone()

        if talalat is not None:
            onkormanyzat_id = talalat[0]
            break
        else:
            print("Nem található ilyen nevű önkormányzat! Próbálja újra.")

    while True:
        u_felhasznalo_neve = input("Felhasználó neve: ").strip()
        if u_felhasznalo_neve:
            break
        print("A felhasználó nevét kötelező megadni!")

    while True:
        try:
            u_felhasznalo_szintje = int(input("Felhasználó szintje (2/3): ").strip())
            if u_felhasznalo_szintje in (2, 3):
                break
            else:
                print("A felhasználói szint csak 2 vagy 3 lehet!")
        except ValueError:
            print("A felhasználói szintnek számnak kell lennie!")

    while True:
        u_felhasznalo_bejelentkezesi_azonositoja = input("Felhasználó bejelentkezési azonosítója: ").strip()
        if not u_felhasznalo_bejelentkezesi_azonositoja:
            print("A bejelentkezési azonosítót kötelező megadni!")
            continue

        res = cur.execute(
            "SELECT id FROM Felhasznalo WHERE bejelentkezesi_azonosito = ?",
            (u_felhasznalo_bejelentkezesi_azonositoja,)
        )
        if res.fetchone() is not None:
            print("Ez a bejelentkezési azonosító már foglalt! Adjon meg másikat.")
            continue
        break

    u_felhasznalo_email = input("Felhasználó e-mail címe: ").strip() or None
    u_felhasznalo_telefonszam = input("Felhasználó telefonszáma: ").strip() or None

    cur.execute(
        "INSERT INTO Felhasznalo (onkormanyzat_id, nev, email, telefonszam, felhasznaloi_szint, bejelentkezesi_azonosito) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (onkormanyzat_id, u_felhasznalo_neve, u_felhasznalo_email, u_felhasznalo_telefonszam,
         u_felhasznalo_szintje, u_felhasznalo_bejelentkezesi_azonositoja)
    )
    con.commit()
    print("\nFelhasználó sikeresen rögzítve!\n")
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


def onkormanyzatok_reszletes_listaja():
    res = cur.execute(
        "SELECT id, nev, email, telefonszam, cim, kapcsolattarto_neve FROM Onkormanyzat ORDER BY id"
    )
    onkormanyzatok = res.fetchall()

    print("\n-----------------------------------")
    print("Szerződött önkormányzatok:")
    print("-----------------------------------")
    for o in onkormanyzatok:
        print(f"ID: {o[0]} | Név: {o[1]} | E-mail: {o[2] or 'Nincs'} | Tel.: {o[3] or 'Nincs'} | Cím: {o[4] or 'Nincs'} | Kapcsolattartó: {o[5] or 'Nincs'}")
    print("-----------------------------------\n")
def onkormanyzat_modositasa():
    onkormanyzatok_reszletes_listaja()

    while True:
        try:
            o_id = int(input("Adja meg a módosítandó önkormányzat ID-ját (0 = mégse): ").strip())
            if o_id == 0:
                return
            res = cur.execute(
                "SELECT id, nev, email, telefonszam, cim, kapcsolattarto_neve FROM Onkormanyzat WHERE id = ?",
                (o_id,)
            )
            onk = res.fetchone()
            if onk is not None:
                break
            print("Nem található ilyen ID-jú önkormányzat!")
        except ValueError:
            print("Kérjük egy egész számot adjon meg!")

    print("\nNyomjon Entert a jelenlegi érték megtartásához:")
    while True:
        uj_nev = input(f"Önkormányzat neve [{onk[1]}]: ").strip() or onk[1]
        res = cur.execute("SELECT id FROM Onkormanyzat WHERE nev = ? AND id != ?", (uj_nev, o_id))
        if res.fetchone() is not None:
            print("Már létezik másik önkormányzat ezen a néven!")
            continue
        break

    uj_email = input(f"E-mail [{onk[2] or 'Nincs'}]: ").strip() or onk[2]
    uj_tel = input(f"Telefonszám [{onk[3] or 'Nincs'}]: ").strip() or onk[3]
    uj_cim = input(f"Cím [{onk[4] or 'Nincs'}]: ").strip() or onk[4]
    uj_kapcsolattarto = input(f"Kapcsolattartó [{onk[5] or 'Nincs'}]: ").strip() or onk[5]

    cur.execute(
        """UPDATE Onkormanyzat
           SET nev = ?, email = ?, telefonszam = ?, cim = ?, kapcsolattarto_neve = ?
           WHERE id = ?""",
        (uj_nev, uj_email, uj_tel, uj_cim, uj_kapcsolattarto, o_id)
    )
    con.commit()
    print("\nÖnkormányzat adatai sikeresen frissítve!\n")
def onkormanyzat_torlese():
    onkormanyzatok_reszletes_listaja()

    while True:
        try:
            o_id = int(input("Adja meg a törölni kívánt önkormányzat ID-ját (0 = mégse): ").strip())
            if o_id == 0:
                return
            res = cur.execute("SELECT nev FROM Onkormanyzat WHERE id = ?", (o_id,))
            onk = res.fetchone()
            if onk is not None:
                break
            print("Nem található ilyen ID-jú önkormányzat!")
        except ValueError:
            print("Kérjük egy egész számot adjon meg!")

    megerosites = input(f"Biztosan törli a(z) '{onk[0]}' önkormányzatot? (i/n): ").strip().lower()
    if megerosites == "i":
        try:
            cur.execute("DELETE FROM Onkormanyzat WHERE id = ?", (o_id,))
            con.commit()
            print("\nÖnkormányzat sikeresen törölve!\n")
        except sqlite3.IntegrityError:
            print("\nHiba: Az önkormányzat nem törölhető, mert még tartoznak hozzá felhasználók vagy eszközök!\n")
    else:
        print("\nTörlés megszakítva.\n")
def onkormanyzatok_kezelese():
    while True:
        print("\n--- Önkormányzatok kezelése ---")
        print("1. Új önkormányzat rögzítése")
        print("2. Meglévő önkormányzat módosítása")
        print("3. Önkormányzat törlése")
        print("4. Vissza a főmenübe")

        valasztas = input("Válasszon menüpontot (1-4): ").strip()
        if valasztas == "1":
            uj_onkormanyzat_rogzitese()
        elif valasztas == "2":
            onkormanyzat_modositasa()
        elif valasztas == "3":
            onkormanyzat_torlese()
        elif valasztas == "4":
            break
        else:
            print("Érvénytelen választás!")


def felhasznalok_listaja_admin():
    sql = """SELECT Felhasznalo.id, Felhasznalo.nev, Onkormanyzat.nev, Felhasznalo.felhasznaloi_szint,
                    Felhasznalo.bejelentkezesi_azonosito, Felhasznalo.email, Felhasznalo.telefonszam
             FROM Felhasznalo
             LEFT JOIN Onkormanyzat ON Felhasznalo.onkormanyzat_id = Onkormanyzat.id
             ORDER BY Felhasznalo.id"""
    res = cur.execute(sql)
    felhasznalok = res.fetchall()

    print("\n-----------------------------------")
    print("Rögzített felhasználók:")
    print("-----------------------------------")
    for f in felhasznalok:
        onk_nev = f[2] if f[2] else "Nincs (Rendszergazda)"
        email = f[5] if f[5] else "Nincs megadva"
        tel = f[6] if f[6] else "Nincs megadva"
        print(f"ID: {f[0]} | Név: {f[1]} | Önkormányzat: {onk_nev} | Szint: {f[3]} | Azonosító: {f[4]} | E-mail: {email} | Tel.: {tel}")
    print("-----------------------------------\n")
def felhasznalo_modositasa():
    felhasznalok_listaja_admin()

    while True:
        try:
            f_id = int(input("Adja meg a módosítandó felhasználó ID-ját (0 = mégse): ").strip())
            if f_id == 0:
                return
            res = cur.execute(
                "SELECT id, onkormanyzat_id, nev, email, telefonszam, felhasznaloi_szint, bejelentkezesi_azonosito "
                "FROM Felhasznalo WHERE id = ?", (f_id,)
            )
            felhasznalo = res.fetchone()
            if felhasznalo is not None:
                break
            print("Nem található ilyen ID-jú felhasználó! Próbálja újra.")
        except ValueError:
            print("Kérjük egy egész számot adjon meg!")

    print("\nNyomjon Entert a jelenlegi érték megtartásához:")
    uj_nev = input(f"Név [{felhasznalo[2]}]: ").strip() or felhasznalo[2]
    uj_email = input(f"E-mail [{felhasznalo[3] or 'Nincs'}]: ").strip() or felhasznalo[3]
    uj_tel = input(f"Telefonszám [{felhasznalo[4] or 'Nincs'}]: ").strip() or felhasznalo[4]

    # Jogosultsági szint módosítása (rendszergazda szintje marad 1, többieké 2 vagy 3)
    if felhasznalo[5] == 1:
        uj_szint = 1
    else:
        while True:
            szint_input = input(f"Felhasználói szint (2/3) [{felhasznalo[5]}]: ").strip()
            if not szint_input:
                uj_szint = felhasznalo[5]
                break
            try:
                szint_szam = int(szint_input)
                if szint_szam in (2, 3):
                    uj_szint = szint_szam
                    break
                print("A felhasználói szint csak 2 vagy 3 lehet!")
            except ValueError:
                print("A felhasználói szintnek számnak kell lennie!")

    # Bejelentkezési azonosító módosítása egyediség-ellenőrzéssel
    while True:
        uj_azonosito = input(f"Bejelentkezési azonosító [{felhasznalo[6]}]: ").strip() or felhasznalo[6]
        res = cur.execute(
            "SELECT id FROM Felhasznalo WHERE bejelentkezesi_azonosito = ? AND id != ?",
            (uj_azonosito, f_id)
        )
        if res.fetchone() is not None:
            print("Ez a bejelentkezési azonosító már foglalt! Adjon meg másikat.")
            continue
        break

    # Önkormányzat módosítása (ha nem rendszergazda)
    uj_onk_id = felhasznalo[1]
    if felhasznalo[5] != 1:
        valtoztat_onk = input("Módosítja a hozzárendelt önkormányzatot? (i/n) [n]: ").strip().lower()
        if valtoztat_onk == "i":
            onkormanyzatok_listaja()
            while True:
                keresett_onk = input("Új önkormányzat neve: ").strip()
                res = cur.execute("SELECT id FROM Onkormanyzat WHERE nev = ?", (keresett_onk,))
                talalat = res.fetchone()
                if talalat is not None:
                    uj_onk_id = talalat[0]
                    break
                print("Nem található ilyen nevű önkormányzat! Próbálja újra.")

    cur.execute(
        """UPDATE Felhasznalo
           SET onkormanyzat_id = ?, nev = ?, email = ?, telefonszam = ?,
               felhasznaloi_szint = ?, bejelentkezesi_azonosito = ?
           WHERE id = ?""",
        (uj_onk_id, uj_nev, uj_email, uj_tel, uj_szint, uj_azonosito, f_id)
    )
    con.commit()
    print("\nFelhasználó adatai sikeresen frissítve!\n")
def felhasznalo_torlese():
    felhasznalok_listaja_admin()

    while True:
        try:
            f_id = int(input("Adja meg a törölni kívánt felhasználó ID-ját (0 = mégse): ").strip())
            if f_id == 0:
                return
            res = cur.execute("SELECT nev, felhasznaloi_szint FROM Felhasznalo WHERE id = ?", (f_id,))
            felhasznalo = res.fetchone()
            if felhasznalo is None:
                print("Nem található ilyen ID-jú felhasználó!")
                continue
            if felhasznalo[1] == 1:
                print("A rendszergazdai fiók nem törölhető!")
                continue
            break
        except ValueError:
            print("Kérjük egy egész számot adjon meg!")

    megerosites = input(f"Biztosan törli '{felhasznalo[0]}' felhasználót? (i/n): ").strip().lower()
    if megerosites == "i":
        try:
            cur.execute("DELETE FROM Felhasznalo WHERE id = ?", (f_id,))
            con.commit()
            print("\nFelhasználó sikeresen törölve!\n")
        except sqlite3.IntegrityError:
            print("\nHiba: A felhasználó nem törölhető, mert már tartozik hozzá hibabejelentés!\n")
    else:
        print("\nTörlés megszakítva.\n")
def felhasznalok_kezelese():
    while True:
        print("\n--- Felhasználók kezelése ---")
        print("1. Új felhasználó hozzáadása")
        print("2. Meglévő felhasználó módosítása")
        print("3. Felhasználó törlése")
        print("4. Vissza a főmenübe")

        valasztas = input("Válasszon menüpontot (1-4): ").strip()
        if valasztas == "1":
            uj_felhasznalo_hozzaadasa()
        elif valasztas == "2":
            felhasznalo_modositasa()
        elif valasztas == "3":
            felhasznalo_torlese()
        elif valasztas == "4":
            break
        else:
            print("Érvénytelen választás!")


def eszkozok_listaja_admin():
    sql = """SELECT Eszkoz.id, Onkormanyzat.nev, Eszkoz.eszkoz_neve, Eszkoz.leltari_szam,
                    Eszkoz.beszerzes_datuma, Eszkoz.tipus, Eszkoz.eszkoz_leirasa
             FROM Eszkoz
             INNER JOIN Onkormanyzat ON Eszkoz.onkormanyzat_id = Onkormanyzat.id
             ORDER BY Onkormanyzat.nev, Eszkoz.eszkoz_neve"""
    res = cur.execute(sql)
    eszkozok = res.fetchall()

    print("\n-----------------------------------")
    print("Rögzített eszközök:")
    print("-----------------------------------")
    for e in eszkozok:
        datum = e[4] if e[4] else "Nincs"
        tipus = e[5] if e[5] else "Nincs"
        leiras = e[6] if e[6] else "Nincs"
        print(f"ID: {e[0]} | Önkormányzat: {e[1]} | Eszköz: {e[2]} | Leltári sz.: {e[3]} | Típus: {tipus} | Beszerzés: {datum} | Leírás: {leiras}")
    print("-----------------------------------\n")
def eszkoz_modositasa():
    eszkozok_listaja_admin()

    while True:
        try:
            e_id = int(input("Adja meg a módosítandó eszköz ID-ját (0 = mégse): ").strip())
            if e_id == 0:
                return
            res = cur.execute(
                "SELECT id, onkormanyzat_id, eszkoz_neve, leltari_szam, beszerzes_datuma, eszkoz_leirasa, tipus "
                "FROM Eszkoz WHERE id = ?", (e_id,)
            )
            eszkoz = res.fetchone()
            if eszkoz is not None:
                break
            print("Nem található ilyen ID-jú eszköz!")
        except ValueError:
            print("Kérjük egy egész számot adjon meg!")

    print("\nNyomjon Entert a jelenlegi érték megtartásához:")
    uj_nev = input(f"Eszköz neve [{eszkoz[2]}]: ").strip() or eszkoz[2]

    while True:
        leltari_input = input(f"Leltári szám [{eszkoz[3]}]: ").strip()
        if not leltari_input:
            uj_leltari = eszkoz[3]
            break
        try:
            uj_leltari = int(leltari_input)
            break
        except ValueError:
            print("A leltári számnak egész számnak kell lennie!")

    uj_datum = input(f"Beszerzés dátuma [{eszkoz[4] or 'Nincs'}]: ").strip() or eszkoz[4]
    uj_leiras = input(f"Leírás [{eszkoz[5] or 'Nincs'}]: ").strip() or eszkoz[5]
    uj_tipus = input(f"Típus [{eszkoz[6] or 'Nincs'}]: ").strip() or eszkoz[6]

    uj_onk_id = eszkoz[1]
    valtoztat_onk = input("Áthelyezi az eszközt másik önkormányzathoz? (i/n) [n]: ").strip().lower()
    if valtoztat_onk == "i":
        onkormanyzatok_listaja()
        while True:
            keresett_onk = input("Új önkormányzat neve: ").strip()
            res = cur.execute("SELECT id FROM Onkormanyzat WHERE nev = ?", (keresett_onk,))
            talalat = res.fetchone()
            if talalat is not None:
                uj_onk_id = talalat[0]
                break
            print("Nem található ilyen nevű önkormányzat! Próbálja újra.")

    cur.execute(
        """UPDATE Eszkoz
           SET onkormanyzat_id = ?, eszkoz_neve = ?, leltari_szam = ?,
               beszerzes_datuma = ?, eszkoz_leirasa = ?, tipus = ?
           WHERE id = ?""",
        (uj_onk_id, uj_nev, uj_leltari, uj_datum, uj_leiras, uj_tipus, e_id)
    )
    con.commit()
    print("\nEszköz adatai sikeresen frissítve!\n")
def eszkoz_torlese():
    eszkozok_listaja_admin()

    while True:
        try:
            e_id = int(input("Adja meg a törölni kívánt eszköz ID-ját (0 = mégse): ").strip())
            if e_id == 0:
                return
            res = cur.execute("SELECT eszkoz_neve, leltari_szam FROM Eszkoz WHERE id = ?", (e_id,))
            eszkoz = res.fetchone()
            if eszkoz is not None:
                break
            print("Nem található ilyen ID-jú eszköz!")
        except ValueError:
            print("Kérjük egy egész számot adjon meg!")

    megerosites = input(f"Biztosan törli a(z) '{eszkoz[0]}' (leltári sz.: {eszkoz[1]}) eszközt? (i/n): ").strip().lower()
    if megerosites == "i":
        try:
            cur.execute("DELETE FROM Eszkoz WHERE id = ?", (e_id,))
            con.commit()
            print("\nEszköz sikeresen törölve!\n")
        except sqlite3.IntegrityError:
            print("\nHiba: Az eszköz nem törölhető, mert kapcsolódik hozzá belépési azonosító, karbantartás vagy hibabejelentés!\n")
    else:
        print("\nTörlés megszakítva.\n")
def eszkozok_kezelese():
    while True:
        print("\n--- Eszközök kezelése ---")
        print("1. Új eszköz rögzítése")
        print("2. Meglévő eszköz módosítása")
        print("3. Eszköz törlése")
        print("4. Vissza a főmenübe")

        valasztas = input("Válasszon menüpontot (1-4): ").strip()
        if valasztas == "1":
            uj_eszkoz_rogzitese()
        elif valasztas == "2":
            eszkoz_modositasa()
        elif valasztas == "3":
            eszkoz_torlese()
        elif valasztas == "4":
            break
        else:
            print("Érvénytelen választás!")


def hibabejelentesek_listazasa(csak_nyitott=False):
    feltetel = "WHERE Hibabejelentes.allapot != 'Lezárt'" if csak_nyitott else ""
    sql = f"""SELECT Hibabejelentes.id, Onkormanyzat.nev, Eszkoz.eszkoz_neve, Eszkoz.leltari_szam,
                     Felhasznalo.nev, Hibatipus.megnevezes, Hibabejelentes.egyedi_komment,
                     Hibabejelentes.bejelentes_datuma, Hibabejelentes.allapot, Hibabejelentes.elharitas_datuma
              FROM Hibabejelentes
              INNER JOIN Eszkoz ON Hibabejelentes.eszkoz_id = Eszkoz.id
              INNER JOIN Onkormanyzat ON Eszkoz.onkormanyzat_id = Onkormanyzat.id
              INNER JOIN Felhasznalo ON Hibabejelentes.felhasznalo_id = Felhasznalo.id
              LEFT JOIN Hibatipus ON Hibabejelentes.hibatipus_id = Hibatipus.id
              {feltetel}
              ORDER BY Hibabejelentes.bejelentes_datuma DESC"""
    res = cur.execute(sql)
    hibak = res.fetchall()

    print("\n-----------------------------------")
    print("Bejelentett hibák:")
    print("-----------------------------------")
    if not hibak:
        print("Nincs megjeleníthető hibabejelentés.")
    for h in hibak:
        tipus = h[5] if h[5] else "Egyedi hiba"
        elharitva = h[9] if h[9] else "Folyamatban / Nyitott"
        print(f"ID: {h[0]} | Állapot: [{h[8]}] | Önkormányzat: {h[1]} | Eszköz: {h[2]} ({h[3]})")
        print(f"   Bejelentő: {h[4]} | Dátum: {h[7]} | Típus: {tipus} | Elhárítva: {elharitva}")
        print(f"   Leírás: {h[6]}")
    print("-----------------------------------\n")
def hiba_reszletek_es_kezeles():
    hibabejelentesek_listazasa(csak_nyitott=False)

    while True:
        try:
            h_id = int(input("Adja meg a kezelendő hibabejelentés ID-ját (0 = mégse): ").strip())
            if h_id == 0:
                return
            res = cur.execute("SELECT id, allapot, elharitas_datuma FROM Hibabejelentes WHERE id = ?", (h_id,))
            hiba = res.fetchone()
            if hiba is not None:
                break
            print("Nem található ilyen ID-jú hibabejelentés!")
        except ValueError:
            print("Kérjük egy egész számot adjon meg!")

    # Korábbi hibakezelési lépések kiírása a Hibakezeles táblából
    res_lepesek = cur.execute(
        "SELECT datum, lepes_leirasa FROM Hibakezeles WHERE hibabejelentes_id = ? ORDER BY id",
        (h_id,)
    )
    lepesek = res_lepesek.fetchall()
    print(f"\n--- #{h_id} hiba eddigi kezelési lépései ---")
    if lepesek:
        for datum, leiras in lepesek:
            print(f"[{datum}] {leiras}")
    else:
        print("Még nincs rögzített hibakezelési lépés.")

    # Új lépés rögzítése
    uj_lepes = input("\nÚj elhárítási lépés leírása (Enter = kihagyás): ").strip()
    if uj_lepes:
        mai_datum = date.today().isoformat()
        lepes_datum = input(f"Lépés dátuma [{mai_datum}]: ").strip() or mai_datum
        cur.execute(
            "INSERT INTO Hibakezeles (hibabejelentes_id, datum, lepes_leirasa) VALUES (?, ?, ?)",
            (h_id, lepes_datum, uj_lepes)
        )

    # Állapot frissítése
    print(f"\nJelenlegi állapot: {hiba[1]}")
    print("Választható új állapot: 1 = Nyitott | 2 = Folyamatban | 3 = Lezárt | Enter = változatlan")
    allapot_valasztas = input("Új állapot: ").strip()

    allapot_map = {"1": "Nyitott", "2": "Folyamatban", "3": "Lezárt"}
    uj_allapot = allapot_map.get(allapot_valasztas, hiba[1])
    uj_elharitas_datuma = hiba[2]

    if uj_allapot == "Lezárt":
        mai_datum = date.today().isoformat()
        uj_elharitas_datuma = input(f"Elhárítás dátuma [{mai_datum}]: ").strip() or mai_datum
    elif uj_allapot in ("Nyitott", "Folyamatban"):
        uj_elharitas_datuma = None

    cur.execute(
        "UPDATE Hibabejelentes SET allapot = ?, elharitas_datuma = ? WHERE id = ?",
        (uj_allapot, uj_elharitas_datuma, h_id)
    )
    con.commit()
    print("\nHibabejelentés állapota és kezelési naplója frissítve!\n")
def bejelentett_hibak_kezelese():
    while True:
        print("\n--- Bejelentett hibák kezelése ---")
        print("1. Összes hibabejelentés megtekintése")
        print("2. Csak a nyitott / folyamatban lévő hibák megtekintése")
        print("3. Hiba kezelése (lépés naplózása / állapot módosítása)")
        print("4. Vissza a főmenübe")

        valasztas = input("Válasszon menüpontot (1-4): ").strip()
        if valasztas == "1":
            hibabejelentesek_listazasa(csak_nyitott=False)
        elif valasztas == "2":
            hibabejelentesek_listazasa(csak_nyitott=True)
        elif valasztas == "3":
            hiba_reszletek_es_kezeles()
        elif valasztas == "4":
            break
        else:
            print("Érvénytelen választás!")


def karbantartasok_listazasa():
    sql = """SELECT Karbantartas.id, Onkormanyzat.nev, Eszkoz.eszkoz_neve, Eszkoz.leltari_szam,
                    Karbantartas.tervezett_datum, Karbantartas.vegrehajtas_datuma, Karbantartas.leiras
             FROM Karbantartas
             INNER JOIN Eszkoz ON Karbantartas.eszkoz_id = Eszkoz.id
             INNER JOIN Onkormanyzat ON Eszkoz.onkormanyzat_id = Onkormanyzat.id
             ORDER BY Karbantartas.tervezett_datum"""
    res = cur.execute(sql)
    karbantartasok = res.fetchall()

    print("\n-----------------------------------")
    print("Tervezett és végrehajtott karbantartások:")
    print("-----------------------------------")
    for k in karbantartasok:
        allapot = f"Elvégezve: {k[5]}" if k[5] else "Tervezett (függőben)"
        print(f"ID: {k[0]} | Önkormányzat: {k[1]} | Eszköz: {k[2]} ({k[3]})")
        print(f"   Tervezett dátum: {k[4]} | Státusz: {allapot} | Leírás: {k[6] or 'Nincs'}")
    print("-----------------------------------\n")
def uj_karbantartas_rogzitese():
    eszkozok_listaja_admin()

    while True:
        try:
            e_id = int(input("Adja meg az eszköz ID-ját, amelyhez karbantartást rögzít (0 = mégse): ").strip())
            if e_id == 0:
                return
            res = cur.execute("SELECT id FROM Eszkoz WHERE id = ?", (e_id,))
            if res.fetchone() is not None:
                break
            print("Nem található ilyen ID-jú eszköz!")
        except ValueError:
            print("Kérjük egy egész számot adjon meg!")

    while True:
        tervezett_datum = input("Tervezett dátum (ÉÉÉÉ-HH-NN): ").strip()
        if tervezett_datum:
            break
        print("A tervezett dátumot kötelező megadni!")

    leiras = input("Karbantartás leírása: ").strip() or None

    cur.execute(
        "INSERT INTO Karbantartas (eszkoz_id, tervezett_datum, vegrehajtas_datuma, leiras) "
        "VALUES (?, ?, NULL, ?)",
        (e_id, tervezett_datum, leiras)
    )
    con.commit()
    print("\nTervezett karbantartás sikeresen rögzítve!\n")
def karbantartas_teljesitese_modositasa():
    karbantartasok_listazasa()

    while True:
        try:
            k_id = int(input("Adja meg a módosítandó karbantartás ID-ját (0 = mégse): ").strip())
            if k_id == 0:
                return
            res = cur.execute(
                "SELECT id, tervezett_datum, vegrehajtas_datuma, leiras FROM Karbantartas WHERE id = ?",
                (k_id,)
            )
            karb = res.fetchone()
            if karb is not None:
                break
            print("Nem található ilyen ID-jú karbantartás!")
        except ValueError:
            print("Kérjük egy egész számot adjon meg!")

    print("\nNyomjon Entert a jelenlegi érték megtartásához:")
    uj_tervezett = input(f"Tervezett dátum [{karb[1]}]: ").strip() or karb[1]

    mai_datum = date.today().isoformat()
    jelenlegi_vegrehajtas = karb[2] if karb[2] else f"Nincs (Enter után írd be: {mai_datum})"
    vegrehajtas_input = input(f"Végrehajtás dátuma [{jelenlegi_vegrehajtas}]: ").strip()
    uj_vegrehajtas = vegrehajtas_input if vegrehajtas_input else karb[2]

    uj_leiras = input(f"Leírás [{karb[3] or 'Nincs'}]: ").strip() or karb[3]

    cur.execute(
        """UPDATE Karbantartas
           SET tervezett_datum = ?, vegrehajtas_datuma = ?, leiras = ?
           WHERE id = ?""",
        (uj_tervezett, uj_vegrehajtas, uj_leiras, k_id)
    )
    con.commit()
    print("\nKarbantartás adatai sikeresen frissítve!\n")
def tervezett_karbantartasok_kezelese():
    while True:
        print("\n--- Tervezett karbantartások kezelése ---")
        print("1. Karbantartások megtekintése")
        print("2. Új tervezett karbantartás rögzítése")
        print("3. Karbantartás teljesítése / módosítása")
        print("4. Vissza a főmenübe")

        valasztas = input("Válasszon menüpontot (1-4): ").strip()
        if valasztas == "1":
            karbantartasok_listazasa()
        elif valasztas == "2":
            uj_karbantartas_rogzitese()
        elif valasztas == "3":
            karbantartas_teljesitese_modositasa()
        elif valasztas == "4":
            break
        else:
            print("Érvénytelen választás!")


def belepesi_azonositok_listazasa():
    sql = """SELECT Belepesi_azonosito.id, Onkormanyzat.nev, Eszkoz.eszkoz_neve, Eszkoz.leltari_szam,
                    Belepesi_azonosito.rendszer_neve, Belepesi_azonosito.belepesi_azonosito,
                    Belepesi_azonosito.jelszo
             FROM Belepesi_azonosito
             INNER JOIN Eszkoz ON Belepesi_azonosito.eszkoz_id = Eszkoz.id
             INNER JOIN Onkormanyzat ON Eszkoz.onkormanyzat_id = Onkormanyzat.id
             ORDER BY Onkormanyzat.nev, Eszkoz.eszkoz_neve"""
    res = cur.execute(sql)
    azonositok = res.fetchall()

    print("\n-----------------------------------")
    print("Eszközökhöz tartozó belépési azonosítók és jelszavak:")
    print("-----------------------------------")
    if not azonositok:
        print("Nincs rögzített belépési azonosító.")
    for a in azonositok:
        print(f"ID: {a[0]} | Önkormányzat: {a[1]} | Eszköz: {a[2]} ({a[3]})")
        print(f"   Rendszer: {a[4]} | Felhasználónév/Azonosító: {a[5]} | Jelszó: {a[6]}")
    print("-----------------------------------\n")
def uj_belepesi_azonosito_rogzitese():
    eszkozok_listaja_admin()

    while True:
        try:
            e_id = int(input("Adja meg az eszköz ID-ját, amelyhez belépési adatot rögzít (0 = mégse): ").strip())
            if e_id == 0:
                return
            res = cur.execute("SELECT id FROM Eszkoz WHERE id = ?", (e_id,))
            if res.fetchone() is not None:
                break
            print("Nem található ilyen ID-jú eszköz!")
        except ValueError:
            print("Kérjük egy egész számot adjon meg!")

    while True:
        rendszer_neve = input("Rendszer / szolgáltatás neve (pl. Windows Admin, RouterOS): ").strip()
        if rendszer_neve:
            break
        print("A rendszer nevét kötelező megadni!")

    while True:
        azonosito = input("Belépési azonosító / felhasználónév: ").strip()
        if azonosito:
            break
        print("A belépési azonosítót kötelező megadni!")

    while True:
        jelszo = input("Jelszó: ").strip()
        if jelszo:
            break
        print("A jelszót kötelező megadni!")

    cur.execute(
        "INSERT INTO Belepesi_azonosito (eszkoz_id, rendszer_neve, belepesi_azonosito, jelszo) "
        "VALUES (?, ?, ?, ?)",
        (e_id, rendszer_neve, azonosito, jelszo)
    )
    con.commit()
    print("\nBelépési azonosító és jelszó sikeresen rögzítve!\n")
def belepesi_azonosito_modositasa():
    belepesi_azonositok_listazasa()

    while True:
        try:
            b_id = int(input("Adja meg a módosítandó belépési azonosító ID-ját (0 = mégse): ").strip())
            if b_id == 0:
                return
            res = cur.execute(
                "SELECT id, rendszer_neve, belepesi_azonosito, jelszo FROM Belepesi_azonosito WHERE id = ?",
                (b_id,)
            )
            adat = res.fetchone()
            if adat is not None:
                break
            print("Nem található ilyen ID-jú rekord!")
        except ValueError:
            print("Kérjük egy egész számot adjon meg!")

    print("\nNyomjon Entert a jelenlegi érték megtartásához:")
    uj_rendszer = input(f"Rendszer neve [{adat[1]}]: ").strip() or adat[1]
    uj_azonosito = input(f"Belépési azonosító [{adat[2]}]: ").strip() or adat[2]
    uj_jelszo = input(f"Új jelszó [{adat[3]}]: ").strip() or adat[3]

    cur.execute(
        """UPDATE Belepesi_azonosito
           SET rendszer_neve = ?, belepesi_azonosito = ?, jelszo = ?
           WHERE id = ?""",
        (uj_rendszer, uj_azonosito, uj_jelszo, b_id)
    )
    con.commit()
    print("\nBelépési adatok sikeresen frissítve!\n")
def belepesi_azonosito_torlese():
    belepesi_azonositok_listazasa()

    while True:
        try:
            b_id = int(input("Adja meg a törölni kívánt belépési azonosító ID-ját (0 = mégse): ").strip())
            if b_id == 0:
                return
            res = cur.execute(
                "SELECT rendszer_neve, belepesi_azonosito FROM Belepesi_azonosito WHERE id = ?",
                (b_id,)
            )
            adat = res.fetchone()
            if adat is not None:
                break
            print("Nem található ilyen ID-jú rekord!")
        except ValueError:
            print("Kérjük egy egész számot adjon meg!")

    megerosites = input(f"Biztosan törli a(z) '{adat[0]}' ({adat[1]}) belépési adatot? (i/n): ").strip().lower()
    if megerosites == "i":
        cur.execute("DELETE FROM Belepesi_azonosito WHERE id = ?", (b_id,))
        con.commit()
        print("\nBelépési azonosító sikeresen törölve!\n")
    else:
        print("\nTörlés megszakítva.\n")
def belepesi_azonositok_kezelese():
    while True:
        print("\n--- Belépési azonosítók és jelszavak kezelése ---")
        print("1. Belépési azonosítók megtekintése")
        print("2. Új belépési azonosító rögzítése eszközhöz")
        print("3. Meglévő belépési azonosító / jelszó módosítása")
        print("4. Belépési azonosító törlése")
        print("5. Vissza a főmenübe")

        valasztas = input("Válasszon menüpontot (1-5): ").strip()
        if valasztas == "1":
            belepesi_azonositok_listazasa()
        elif valasztas == "2":
            uj_belepesi_azonosito_rogzitese()
        elif valasztas == "3":
            belepesi_azonosito_modositasa()
        elif valasztas == "4":
            belepesi_azonosito_torlese()
        elif valasztas == "5":
            break
        else:
            print("Érvénytelen választás!")
#rendszergazda------------------------------------------------------


#2/3.szint------------------------------------------------------------
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

def onkormanyzat_karbantartasai():
    onkormanyzat_id = jelenlegi_felhasznalo[1]
    if onkormanyzat_id is None:
        print("Nincs hozzárendelve önkormányzat a felhasználóhoz.")
        return

    sql = """SELECT Eszkoz.eszkoz_neve, Eszkoz.leltari_szam,
                    Karbantartas.tervezett_datum, Karbantartas.vegrehajtas_datuma, Karbantartas.leiras
             FROM Karbantartas
             INNER JOIN Eszkoz ON Karbantartas.eszkoz_id = Eszkoz.id
             WHERE Eszkoz.onkormanyzat_id = ?
             ORDER BY Karbantartas.tervezett_datum DESC"""
    res = cur.execute(sql, (onkormanyzat_id,))
    karbantartasok = res.fetchall()

    print("\n-----------------------------------")
    print("Önkormányzat eszközeinek karbantartásai:")
    print("-----------------------------------")
    if not karbantartasok:
        print("Nincs rögzített karbantartás ehhez az önkormányzathoz.")
    for k in karbantartasok:
        statusz = f"Elvégezve: {k[3]}" if k[3] else "Tervezett (függőben)"
        print(f"Eszköz: {k[0]} ({k[1]}) | Tervezett: {k[2]} | Státusz: {statusz}")
        print(f"   Leírás: {k[4] or 'Nincs megadva'}")
    print("-----------------------------------\n")
#2/3.szint------------------------------------------------------------
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
            print("1. Önkormányzatok kezelése (hozzáadás / módosítás / törlés)")
            print("2. Eszközök kezelése (hozzáadás / módosítás / törlés)")
            print("3. Felhasználók kezelése (hozzáadás / módosítás / törlés)")
            print("4. Belépési azonosítók és jelszavak kezelése")
            print("5. Tervezett karbantartások kezelése")
            print("6. Bejelentett hibák kezelése")
            print("7. Kilépés")
            felhasznaloi_szinthez_tartozo_lehetosegek = 7

            adott_felhasznalohoz_tartozo_menu = {
                1: onkormanyzatok_kezelese,
                2: eszkozok_kezelese,
                3: felhasznalok_kezelese,
                4: belepesi_azonositok_kezelese,
                5: tervezett_karbantartasok_kezelese,
                6: bejelentett_hibak_kezelese,
                7: kilepes,
            }

        elif jelenlegi_felhasznalo[4] == 2:
            print("1. Önkormányzat dolgozóinak megtekintése")
            print("2. Önkormányzat eszközeinek megtekintése")
            print("3. Hibabejelentés")
            print("4. Új felhasználó felvétele az önkormányzathoz")
            print("5. Bejelentett hibák állapotának megtekintése")
            print("6. Tervezett karbantartások megtekintése")
            print("7. Kilépés")
            felhasznaloi_szinthez_tartozo_lehetosegek = 7

            adott_felhasznalohoz_tartozo_menu = {
                1: onkormanyzat_dolgozoi,
                2: onkormanyzat_eszkozei,
                # 3: ,
                4: uj_felhasznalo_hozzaadasa,
                # 5: ,
                6: onkormanyzat_karbantartasai,
                7: kilepes,
            }

        elif jelenlegi_felhasznalo[4] == 3:
            print("1. Önkormányzat dolgozóinak megtekintése")
            print("2. Önkormányzat eszközeinek megtekintése")
            print("3. Bejelentett hibák megtekintése")
            print("4. Tervezett karbantartások megtekintése")
            print("5. Kilépés")
            felhasznaloi_szinthez_tartozo_lehetosegek = 5

            adott_felhasznalohoz_tartozo_menu = {
                1: onkormanyzat_dolgozoi,
                2: onkormanyzat_eszkozei,
                3: onkormanyzat_karbantartasai,
                4: kilepes,
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
