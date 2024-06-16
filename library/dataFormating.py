import globalVariables as gv
from library.encrypter import decrypt
from datetime import date, timedelta

def getAllUsers(file:str):
    allUsers = []
    with open(gv.fileUsers, "rb") as file:
        lines:list[str] = file.readlines()
        for line in lines:
            users = (line.decode().replace("\n", "").split("|"))
            if len(users) < 5: continue
            users[4] = eval(users[4])
            allUsers.append(users)
    return allUsers

def addUserScore(file:str, user:str):
    with open(file, "a") as file:
        file.write(user + "\n")

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
