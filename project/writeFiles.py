import random
from .questionSolutions import Q4Ans, Q5Ans, Q6Ans, Q7Ans, Q8Ans, Q9Ans, Q10Ans
def write(playerid, questionId, data):
    path = "project/static/" + str(playerid) + str(questionId) + ".txt"
    with open(path, 'w') as file:
        file.write(data)

def appendLine(playerid, questionId, data):
    path = "project/static/" + str(playerid) + str(questionId) + ".txt"
    with open(path, 'a') as file:
        file.writelines(data + '\n')

def clearFile(playerid, questionId):
    path = "project/static/" + str(playerid) + str(questionId) + ".txt"
    with open(path, 'w') as file:
        file.write('')

def Q4(playerid):
    data = [random.randint(1,9) for x in range(100)]
    strData = ' '.join([str(x) for x in data])
    write(playerid, 4, strData)
    return Q4Ans(data)

def Q5(playerid):
    data = random.randint(10,20)
    strData = str(data)
    write(playerid, 5, strData)
    return Q5Ans(data)

def Q6(playerid):
    data = [random.randint(1,99) for x in range(100)]
    strData = ' '.join([str(x) for x in data])
    write(playerid, 6, strData)
    return Q6Ans(data)

def Q7(playerid):
    data = [random.randint(1,99) for x in range(100)]
    strData = ' '.join([str(x) for x in data])
    write(playerid, 7, strData)
    return Q7Ans(data)

def Q8(playerid):
    clearFile(playerid, 8)
    data = []
    for i in range(10):
        line = [random.randint(1,9) for x in range(10)]
        strLine = ' '.join([str(x) for x in line])
        data.append(line)
        appendLine(playerid, 8, strLine)
    return Q8Ans(data)

def Q9(playerid):
    clearFile(playerid, 9)
    for i in range(10):
        appendLine(playerid, 9, ' '.join([str(random.randint(0,1)) for x in range(10)]))
    return Q9Ans(0)

def Q10(playerid):
    data = random.randint(1,50)
    write(playerid, 10, str(data))
    return Q10Ans(data)