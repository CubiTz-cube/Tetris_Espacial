import globalVariables as gv
from library.encrypter import decrypt
import datetime
from datetime import date, timedelta

def getAllUsers():
    """Devuelve una lista de usuarios. Cada usuario tiene la siguiente estructura:
    [mail, name, password, state, [scores]]"""
    allUsers = []
    with open(gv.fileUsers, "rb") as file:
        lines:list[str] = file.readlines()
        for line in lines:
            users = (line.decode("utf-8").replace("\n", "").split("|"))
            if len(users) < 5: continue
            users[4] = eval(users[4])
            allUsers.append(users)
    return allUsers

def addUserScore(userMail:str, score:int):
    """Guarda el score de un usario especifico en el archivo de usuarios."""
    date = datetime.datetime.now()
    allUsers = getAllUsers()
    with open(gv.fileUsers, "w", encoding='utf-8') as file:
        for users in allUsers:
            if users[0] == userMail:
                users[4].append([score,date.day,date.month,date.year,date.hour,date.minute])
            file.write("|".join(map(str, users)) + "\n")

def timeDateCompare(dateList:list[int]):
    compareTime = date(*dateList)

    today = date.today()
    day = today - timedelta(days=1)
    week = today - timedelta(weeks=1)
    mounth = today - timedelta(weeks=4)
    year = today - timedelta(days=365)

    if day <= compareTime <= today:
        return "day"
    elif week <= compareTime <= today:
        return "week"
    elif mounth <= compareTime <= today:
        return "mounth"
    elif year <= compareTime <= today:
        return "year"
