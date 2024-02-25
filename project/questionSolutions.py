
def Q4Ans(n):
    if len(n) == 0:
        return 0
    else:
        return n[0] + Q4Ans(n[1:])
    
def Q5Ans(n): #first n terms of fibonacci sequence
    terms = ["1", "1"]
    for i in range(2, n):
        terms.append(str(int(terms[i-1]) + int(terms[i-2])))
    return ','.join(terms)

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

def isValid(screen, m, n, x, y, prevC, newC):
	if x<0 or x>= m\
	or y<0 or y>= n or\
	screen[x][y]!= prevC\
	or screen[x][y]== newC:
		return False
	return True

def floodfill(screen, m, n, x, y, prevC, newC):
    queue = []

	
	# Append the position of starting 
	# pixel of the component
    queue.append([x, y])

	# Color the pixel with the new color
    screen[x][y] = newC
    counter = 0

	# While the queue is not empty i.e. the 
	# whole component having prevC color 
	# is not colored with newC color
    while queue:
		
		# Dequeue the front node
        currPixel = queue.pop()
		
        posX = currPixel[0]
        posY = currPixel[1]
		
		# Check if the adjacent
		# pixels are valid
        if isValid(screen, m, n, posX + 1, posY, prevC, newC):
			
			# Color with newC
			# if valid and enqueue
            screen[posX + 1][posY] = newC
            queue.append([posX + 1, posY])
            counter += 1

        if isValid(screen, m, n, posX-1, posY, prevC, newC):
            screen[posX-1][posY]= newC
            queue.append([posX-1, posY])
            counter += 1

        if isValid(screen, m, n, posX, posY + 1, prevC, newC):
            screen[posX][posY + 1]= newC
            queue.append([posX, posY + 1])
            counter += 1

        if isValid(screen, m, n, posX, posY-1, prevC, newC):
            screen[posX][posY-1]= newC
            queue.append([posX, posY-1])
            counter += 1
            
    return counter


def Q9Ans(screen):
    areas = []
    m = len(screen)
    n = len(screen[0])
    for i in range(m):
        for j in range(n):
            areas.append(floodfill(screen, m, n, i, j, 1, 4))
    return max(areas)

def Q10Ans(n):
    total = n**2
    total *= 2**n
    return total

def Q11Ans(n):
    res = ""
    resLen = 0
    for i in range(len(n)):
        # odd length
        l,r = i,i
        while l >= 0 and r < len(n) and n[l] == n[r]:
            if r-l+1 > resLen:
                res = n[l:r+1]
                resLen = r-l+1
            l -= 1
            r += 1
        # even length
        l,r = i,i+1
        while l >= 0 and r < len(n) and n[l] == n[r]:
            if r-l+1 > resLen:
                res = n[l:r+1]
                resLen = r-l+1
            l -= 1
            r += 1
    return resLen

def Q12Ans(n, target):
    prevMap = {}
    for i, n in enumerate(n):
        diff = target - n
        if diff in prevMap:
            return [prevMap[diff], i]
        prevMap[n] = i

def Q13Ans(n):
    one, two = 1,1
    for i in range(n - 1):
        temp = one
        one = one + two
        two = temp
    return one

def Q14Ans(n):
    
    def valid(node, left, right):
        if not node:
            return True
        
        if not (node.val < right and node.val > left):
            return False
        
        return (valid(node.left, left, node.val) and valid(node.right, node.val, right))
    
    return valid(n, float('-inf'), float('inf'))

def Q15Ans(n):
    list_length = len(n)
    if list_length == 1:
        return n
    mid_point = list_length // 2
    left = Q15Ans(n[:mid_point])
    right = Q15Ans(n[mid_point:])
    return merge(left, right)

def merge(left, right):
    output = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            output.append(left[i])
            i += 1
        else:
            output.append(right[j])
            j += 1
    output.extend(left[i:])
    output.extend(right[j:])

    return output

# def Q16Ans(list1, list2): This is the code to solve the linked list question, however does not fit with the game format so leaving it out

#     dummy = ListNode()
#     tail = dummy
#     sortedList = []
    
#     while list1 and list2:
#         if list1.val < list2.val:
#             tail.next = list1
#             list1 = list1.next
#             sortedList.append(tail.val)
#         else:
#             tail.next = list2
#             list2 = list2.next
#             sortedList.append(tail.val)
#         tail = tail.next
#     print(sortedList)
#     return sortedList
        
        
