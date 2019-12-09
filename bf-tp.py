#! /usr/bin/python
import itertools
import argparse
import sys
import hashlib
import time
import threading

# you will see the 'bf' name use its the alias for brute force.

# all the type of Character we can use.
lowerCase = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
upperCase = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
number = ['0','1','2','3','4','5','6','7','8','9']
special = ['#','@','_']

# bfList is the list for all the Characters we will use.
bfList = []
typeCharacter = 0
nbCharacters = [6, 13]
defaultPathFile = "./hash.txt" # dont change it

 
# method used to read the hashes password file
def readFile(path):
    myFile = open(path, 'r+')
    result = []
    for line in myFile.readlines():
        result.append(line.rstrip())
    myFile.close()    
    return result

# method to encrypt in sha256 a string
def encryptString(hash_string):
    sha_signature = \
        hashlib.md5(hash_string.encode()).hexdigest()
    return sha_signature

# compare generated password to attempt hashed
def checkPass(attempt, myHash):
    passToCheck = "".join(attempt)
    hashToCheck = encryptString(passToCheck)
    if hashToCheck == myHash:
        return passToCheck
    return False

# method for generate hash and compare it
def crackersOneList(cList, nbCharacter, pathHash):
    input()
    doc = readFile(pathHash)
    result = []
    for d in doc:
        start = time.time()
        solution = ""
        i = nbCharacters[0]
        while i < nbCharacters[1]: 
            for attempt in itertools.product(cList, repeat=i):
                solution = checkPass(attempt, d)
                if solution != False:
                    realTime = time.time()-start
                    print ('Le mot de passe est "' + solution + '" .')
                    minutes, seconds = divmod(int(realTime), 60)
                    hours, minutes = divmod(minutes, 60)
                    days, hours = divmod(hours, 24)
                    years, days = divmod(days, 365)
                    print ('Temps pour le trouver : {:d} ans, {:02d} jours, {:02d} heures, {:02d} minutes et {:02d} secondes'.format(years, days, hours, minutes, seconds))                 
                    result.append(attempt)
                    i = nbCharacters[1]
                    break
            i +=1
    print(result)

# test time to crack
def testTimeToCrackTheoric(cList, nbCharacter, defaultPathFile):
    timeSpent = []
    stop = 1000000
    xtime = time.time()
    doc = readFile(defaultPathFile)
    timeSpent.append(time.time()-xtime)
    result = []
    for d in doc:
        start = time.time()
        solution = ""
        xtime = time.time() 
        for attempt in itertools.product(cList, repeat=6):
            solution = checkPass(attempt, d)
            if solution != False:
                realTime = time.time()-start
                print ('Le mot de passe est "' + solution + '" .')
                minutes, seconds = divmod(int(realTime), 60)
                hours, minutes = divmod(minutes, 60)
                days, hours = divmod(hours, 24)
                years, days = divmod(days, 365)
                print ('Temps pour le trouver : {:d} ans, {:02d} jours, {:02d} heures, {:02d} minutes et {:02d} secondes'.format(years, days, hours, minutes, seconds))                 
                result.append(attempt)
                i = nbCharacter[1]
                break
            if stop != 0:
                stop = stop-1
            else:
                break
        timeSpent.append(time.time()-xtime)
    realTimeSpent = timeSpent[0] + timeSpent[1]
    return realTimeSpent
 
def timeToCrackTheoric(nbCharacters, typeCharacter, cList, defaultPathFile):
    showTime = []
    print(typeCharacter)
    for i in range(nbCharacters[0], nbCharacters[1]):
        result = testTimeToCrackTheoric(cList, i, defaultPathFile)
        seconds = (typeCharacter**i)*(result/1000000)        
        minutes, seconds = divmod(int(seconds), 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        years, days = divmod(days, 365)
        showTime.append('Temps estime maximal pour trouver le mot de passe de {:d} caracteres : {:d} ans, {:02d} jours, {:02d} heures, {:02d} minutes et {:02d} secondes '.format(i, years, days, hours, minutes, seconds))
    for show in showTime:
        print(show)

# use the command parser
parser = argparse.ArgumentParser(description='CrackPass : command line brute force')
parser.add_argument('-t', '--type', help='Use to say witch type of character we use. You need to have l, u, n, or s option next to it.')
parser.add_argument('-f', '--file', help='Put the path to your hashes passwords file')
parser.add_argument('-T', '--test', help='This command is needeed to know what is the processing capacity of your machine')

# argument parser
for index, value in enumerate(sys.argv):
    # Get the user type of Character he wanna use.
    if value == '-t' or value == '--type':
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
            print("Erreur : l'option '-t' ou '--type' n'accepte comme argument que : l, u, n ou s (voir -help pour plus d'informations)")
            exit()
        typeCharacter = len(bfList)
    # Get the number of the password's Characters.
    elif value == '-c': 
        if int(sys.argv[index+1]):
            nbCharacter = int(sys.argv[index+1])
        else:
            print("Erreur : l'option '-c' n'accepte que des type 'int' et n'accepte pas 0")
            exit()
    # Get the file path of our hashe's passwords
    elif value == '-f' or value == '--file':
        if not sys.argv[index+1]:
            print("Erreur : l'option '-f' ou '--file' doit etre acompagne d'un chemin absolu")
            exit()
        else:
            pathFile = sys.argv[index+1]
    # Launch testing bruteforce script
    elif value == '-T' or value == '--test':
        testTimeToCrackTheoric(bfList, nbCharacters, defaultPathFile)
            
timeToCrackTheoric(nbCharacters, typeCharacter, bfList, defaultPathFile)
crackersOneList(bfList, nbCharacter, pathFile)

# threading.Thread(crackersOneList, bfList, nbCharacter, pathFile).start()