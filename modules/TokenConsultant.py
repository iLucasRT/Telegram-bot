import sqlite3

def search(token, myCursor):
    try:
        tokenn = myCursor.execute("SELECT * FROM tokens WHERE ID=:token", {'token': token}).fetchall()
        return tokenn[0][0], tokenn[0][2]
    except IndexError:
        try:
            tokenn = myCursor.execute("SELECT * FROM tokens WHERE Symbol=:token", {'token': token}).fetchall()
            return tokenn[0][0], tokenn[0][2]
        except IndexError:
            return False, False
