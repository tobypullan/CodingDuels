import random
class writeFiles:
    def __init__(self, questionId):
        self.path = "project/static/" + str(questionId) + ".txt"

    def write(self, data):
        with open(self.path, 'w') as file:
            file.write(data)

    def appendLine(self, data):
        with open(self.path, 'a') as file:
            file.writelines(data + '\n')

    def clearFile(self):
        with open(self.path, 'w') as file:
            file.write('')
    
    def Q4(self):
        self.write([x.random.randint(1,9) for x in range(100)])

    def Q5(self):
        self.write(random.randint(10,20))

    def Q6(self):
        self.write([x.random.randint(1,9) for x in range(100)])

    def Q7(self):
        self.write([x.random.randint(1,99) for x in range(100)])

    def Q8(self):
        self.clearFile()
        for i in range(10):
            self.appendLine([x.random.randint(1,9) for x in range(10)])
    
    def Q9(self):
        self.clearFile()
        for i in range(10):
            self.appendLine([x.random.randint(0,1) for x in range(10)])

    def Q10(self):
        self.write(random.randint(1,50))