#! /usr/bin/python
import itertools
import argparse
import sys
import hashlib
import crackThread
import time

# you will see the 'bf' name use its the alias for brute force.

# all the type of caracter we can use.
lowerCase = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
upperCase = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
number = ['0','1','2','3','4','5','6','7','8','9']
special = ['!','#','$','%','&','(',')','*','+',',','-','.','/',':',';','<','=','>','?','@','[',']','^','_','`','{','|','}','~']

# bfList is the list for all the caracters we will use.
bfList = []
nbCaracter = 0
passFile = ""
typeCaracter = 0

# use the command parser
parser = argparse.ArgumentParser(description='CrackPass : command line brute force')
parser.add_argument('-t', '--type', help='Use to say witch type of character we use. You need to have l, u, n, or s option next to it.')
parser.add_argument('-c', '--caracter', help='Put the number of character of the password', type=int, default=8)
parser.add_argument('-f', '--file', help='Put the path to your hashes passwords file')

# argument parser
for index, value in enumerate(sys.argv):
    # Get the user type of caracter he wanna use.
    if value == '-t':
        if 'l' in sys.argv[index+1]:
            bfList += lowerCase
        if 'u' in sys.argv[index+1]:
            bfList += upperCase
        if 'n' in sys.argv[index+1]:
            bfList += number
        if 's' in sys.argv[index+1]:
            bfList += special
        # Error for an invalid argument after.
        if 'l' not in sys.argv[index+1] and 'u' not in sys.argv[index+1] and 'n' not in sys.argv[index+1] and 's' not in sys.argv[index+1]:
            print("Erreur : l'option '-t' n'accepte comme argument que : l, u, n ou s (voir -help pour plus d'informations)")
            exit()
        typeCaracter = len(bfList)
    # Get the number of the password's caracters.
    elif value == '-c': 
        if int(sys.argv[index+1]):
            nbCaracter = int(sys.argv[index+1])
        else:
            print("Erreur : l'option '-c' n'accepte que des type 'int' et n'accepte pas 0")
            exit()
    # Get the file path of our hashe's passwords
    elif value == '-f':
        if not sys.argv[index+1]:
            print("Erreur : l'option '-f' doit etre acompagne d'un chemin absolu")
            exit()
        else:
            passFile = sys.argv[index+1]
    
# method used to read the hashes password file
def readFile(path):
    myFile = open(path, 'r+')
    result = []
    with myFile as f:
        for line in f.readlines():
            result.append(line.rstrip())
    myFile.close()    
    return result

# method to encrypt in sha256 a string
def encryptString(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

# compare generated password to attempt hashed
def checkPass(attempt, myHash):
    passToCheck = "".join(attempt)
    print passToCheck
    hashToCheck = encryptString(passToCheck)
    if hashToCheck == myHash:
        return passToCheck
    return False

def timeToCrackTheoric(nbCaracter, typeCaracter):
    seconds = (nbCaracter**typeCaracter)/15000000
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    years, days = divmod(days, 365)
    print('Temps estime maximal pour trouver le mot de passe : {:d} ans, {:02d} jours, {:02d} heures, {:02d} minutes et {:02d} secondes '.format(years, days, hours, minutes, seconds))

# method for generate hash and compare it
def crackersOneList(cList, nbCaracter, pathHash):
    doc = readFile(pathHash)
    for d in doc:
        start = time.time()
        for attempt in itertools.product(cList, repeat=nbCaracter):
            solution = checkPass(attempt, d)
            if solution != False:
                realTime = time.time()-start
                print ('Le mot de passe est "' + solution + '" .')
                minutes, seconds = divmod(int(realTime), 60)
                hours, minutes = divmod(minutes, 60)
                days, hours = divmod(hours, 24)
                years, days = divmod(days, 365)
                print ('Temps pour le trouver : {:d} ans, {:02d} jours, {:02d} heures, {:02d} minutes et {:02d} secondes'.format(years, days, hours, minutes, seconds))                 
                break

timeToCrackTheoric(nbCaracter, typeCaracter)
crackersOneList(bfList, nbCaracter, passFile)