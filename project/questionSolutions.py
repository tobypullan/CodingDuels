def SumOfList(n):
    if len(n) == 0:
        return 0
    else:
        return n[0] + SumOfList(n[1:])
    
def FibSeqGen(n):
    if n == 0:
        return []
    elif n == 1:
        return [1]
    else:
        return FibSeqGen(n-1) + [FibSeqGen(n-1)[-1] + FibSeqGen(n-1)[-2]]

  
questionSolutionFuncs = {4: SumOfList}

class Solutions:
    def __init__(self, playerid):
        self.playerid = playerid
    def GetSolution(self, questionId):
        return questionSolutionFuncs[questionId]
    def CheckAnswer(self, questionId, answer, input):
        return questionSolutionFuncs[questionId](input) == answer