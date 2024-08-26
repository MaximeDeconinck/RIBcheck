import hashlib

def RIBsignature(username, adress, country, iban, salt):
    return hashlib.sha512((username + adress + country + iban + salt).encode('UTF-8')).hexdigest()