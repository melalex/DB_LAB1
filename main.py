import pickle

from os.path import isfile

FILE_NAME = "cinemas.meldb"

if isfile(FILE_NAME):
    dataBaseFile = open(FILE_NAME, 'rb')
    dataBase = pickle.load(dataBaseFile)
    dataBaseFile.close()
else:
    dataBase = {}

run = True


dataBaseFile = open(FILE_NAME, 'wb')
pickle.dump(dataBase, dataBaseFile)
dataBaseFile.close()
