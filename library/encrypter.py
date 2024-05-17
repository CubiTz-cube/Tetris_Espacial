def encrypt(text:str):
    encoded = ""
    for char in text:
        encoded += chr(ord(char)+1)
    return encoded

def decrypt(encodeText:str):
    decoded = ""
    for char in encodeText:
        decoded += chr(ord(char)-1)
    return decoded