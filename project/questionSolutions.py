def Q4Ans(n):
    if len(n) == 0:
        return 0
    else:
        return n[0] + Q4Ans(n[1:])
    
def Q5Ans(n):
    if n == 0:
        return []
    elif n == 1:
        return [1]
    else:
        return Q5Ans(n-1) + [Q5Ans(n-1)[-1] + Q5Ans(n-1)[-2]]




# class Solutions:
#     def __init__(self, playerid):
#         self.playerid = playerid
#     def GetSolution(self, questionId):
#         return questionSolutionFuncs[questionId]
#     def CheckAnswer(self, questionId, answer, input):
#         return questionSolutionFuncs[questionId](input) == answer