import random
from .questionSolutions import Q4Ans, Q5Ans
def write(questionId, data):
    path = "project/static/" + str(questionId) + ".txt"
    with open(path, 'w') as file:
        file.write(data)

def appendLine(questionId, data):
    path = "project/static/" + str(questionId) + ".txt"
    with open(path, 'a') as file:
        file.writelines(data + '\n')

def clearFile(questionId):
    path = "project/static/" + str(questionId) + ".txt"
    with open(path, 'w') as file:
        file.write('')

def Q4():
    data = [random.randint(1,9) for x in range(100)]
    strData = ' '.join([str(x) for x in data])
    write(4, strData)
    return Q4Ans(data)

def Q5():
    data = str(random.randint(10,20))
    write(5, data)

def Q6():
    write(6, ' '.join([str(random.randint(1,9)) for x in range(100)]))

def Q7():
    write(7, ' '.join([str(random.randint(1,99)) for x in range(100)]))

def Q8():
    clearFile(8)
    for i in range(10):
        appendLine(8, ' '.join([str(random.randint(1,9)) for x in range(10)]))

def Q9():
    clearFile(9)
    for i in range(10):
        appendLine(9, ' '.join([str(random.randint(0,1)) for x in range(10)]))

def Q10():
    write(10, str(random.randint(1,50)))