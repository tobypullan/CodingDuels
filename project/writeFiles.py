import random
from .questionSolutions import Q4Ans, Q5Ans, Q6Ans, Q7Ans, Q8Ans, Q9Ans, Q10Ans, Q11Ans, Q12Ans, Q13Ans, Q14Ans, Q15Ans
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
    data = []
    for i in range(10):
        line = [random.randint(0,1) for x in range(10)]
        strLine = ' '.join([str(x) for x in line])
        data.append(line)
        appendLine(playerid, 9, strLine)
    return Q9Ans(data)

def Q10(playerid):
    data = random.randint(1,50)
    write(playerid, 10, str(data))
    return Q10Ans(data)

def Q11(playerid):
    data = [chr(random.randint(ord('a'), ord('c'))) for x in range(7)]
    strData = ''.join([str(x) for x in data])
    write(playerid, 11, strData)
    return Q11Ans(data)

def Q12(playerid):
    target = random.randint(1,20)
    data = [random.randint(1,20) for x in range(100)]
    data.append(target)
    data.append(0)
    strData = ' '.join([str(x) for x in data])
    clearFile(playerid, 12)
    appendLine(playerid, 12, strData)
    appendLine(playerid, 12, "target: " + str(target))
    return Q12Ans(data, target)

def Q13(playerid):
    data = random.randint(1,20)
    write(playerid, 13, str(data))
    return Q13Ans(data)

def Q14(playerid):
    class TreeNode:
        def __init__(self, key):
            self.val = key
            self.left = None
            self.right = None
    
    rootVal = random.randint(1,20)
    root = TreeNode(rootVal)
    leftVal = random.randint(1,20)
    root.left = TreeNode(leftVal)
    rightVal = random.randint(1,20)
    root.right = TreeNode(rightVal)
    leftLeftVal = random.randint(1,20)
    root.left.left = TreeNode(leftLeftVal)
    leftRightVal = random.randint(1,20)
    root.left.right = TreeNode(leftRightVal)
    rightLeftVal = random.randint(1,20)
    root.right.left = TreeNode(rightLeftVal)

    write(playerid, 14, str(rootVal) + ' ' + str(leftVal) + ' ' + str(rightVal) + ' ' + str(leftLeftVal) + ' ' + str(leftRightVal) + ' ' + str(rightLeftVal))
    return Q14Ans(root)

def Q15(playerid):
    data = [random.randint(1,99) for x in range(25)]
    strData = ' '.join([str(x) for x in data])
    write(playerid, 15, strData)
    return Q15Ans(data)
        
def Q16(playerid):
    class ListNode:
        def __init__(self, val=0, next=None):
            self.val = val
            self.next = next

    initialVal1 = random.randint(1,20)
    initialVal2 = random.randint(1,20)
    list1 = ListNode(initialVal1)
    list2 = ListNode(initialVal2)
    list1str = [str(initialVal1)]
    list2str = [str(initialVal2)]

    for i in range(10):
        nodeVal = random.randint(1,20)
        list1.next = ListNode(nodeVal)
        list1str.append(str(nodeVal))
    appendLine(playerid, 16, ' '.join(list1str))

    for i in range(10):
        nodeVal = random.randint(1,20)
        list2.next = ListNode(nodeVal)
        list2str.append(str(nodeVal))
    appendLine(playerid, 16, ' '.join(list2str))

    return 0 # question doesn't fit with the format of my game. However, still tried to make it work so am leaving the class here for future reference.