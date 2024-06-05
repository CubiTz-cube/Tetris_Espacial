import globalVariables as gv
from library.encrypter import decrypt

def getAllUsers(file:str):
    allUsers = []
    with open(gv.fileUsers, "rb") as file:
        lines:list[str] = file.readlines()
        for line in lines:
            users = (line.decode().replace("\n", "").split("|"))
            users[4] = eval(users[4])
            allUsers.append(users)
    return allUsers