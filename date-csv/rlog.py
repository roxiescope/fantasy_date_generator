

def createlog():
    f = open("log.txt", "w")
    f.write("Starting new log file\n")
    f.close()

def writelog(message):
    f = open("log.txt", "a")
    f.write(str(message) + "\n")
    f.close()

def readlog():
    f = open("log.txt", "r")
    return f.read()
