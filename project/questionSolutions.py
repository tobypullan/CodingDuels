def Q4Ans(n):
    if len(n) == 0:
        return 0
    else:
        return n[0] + Q4Ans(n[1:])
    
def Q5Ans(n): #first n terms of fibonacci sequence
    terms = [1, 1]
    for i in range(2, n):
        terms.append(terms[i-1] + terms[i-2])
    return terms

def checkPrime(n):
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

def Q6Ans(n):
    return sum([x for x in n if checkPrime(x)])

def Q7Ans(n):
    return sum([int(x) for x in ''.join([str(x) for x in n])])

def Q8Ans(n):
    total = 0
    for i in range(len(n)):
        total += n[i][i]
    return total

def Q9Ans(n):
    return 0

def Q10Ans(n):
    total = n**2
    total *= 2**n
    return total



# class Solutions:
#     def __init__(self, playerid):
#         self.playerid = playerid
#     def GetSolution(self, questionId):
#         return questionSolutionFuncs[questionId]
#     def CheckAnswer(self, questionId, answer, input):
#         return questionSolutionFuncs[questionId](input) == answer