
def Q4Ans(n): # finds sum of list recursively
    if len(n) == 0:
        return 0
    else:
        return n[0] + Q4Ans(n[1:])
    
def Q5Ans(n): #first n terms of fibonacci sequence
    terms = ["1", "1"]
    for i in range(2, n):
        terms.append(str(int(terms[i-1]) + int(terms[i-2])))
    return ','.join(terms) # returns the answer as a string

def checkPrime(n):
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

def Q6Ans(n): # sum of all prime numbers in list
    return sum([x for x in n if checkPrime(x)]) # uses list comprehension to make a list of all prime numbers in n and then returns the sum of that list

def Q7Ans(n): # sum of all digits in list
    return sum([int(x) for x in ''.join([str(x) for x in n])]) # joins all the numbers in n into a single string and then sums the digits of that string

def Q8Ans(n): # sum along the diagonal of a 2D array
    total = 0
    for i in range(len(n)):
        total += n[i][i]
    return total

def isValid(screen, m, n, x, y, prevC, newC): # checking if a coordinate is valid for floodfill algorithm
	if x<0 or x>= m\
	or y<0 or y>= n or\
	screen[x][y]!= prevC\
	or screen[x][y]== newC:
		return False
	return True

def floodfill(screen, m, n, x, y, prevC, newC): # this function and isValid were taken from a geeksforgeeks article on floodfill algorithm - inlcuded in references
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


def Q9Ans(screen): # applies floodfill algorithm to every pixel in screen to find the largest area of 1s
    areas = []
    m = len(screen)
    n = len(screen[0])
    for i in range(m):
        for j in range(n):
            areas.append(floodfill(screen, m, n, i, j, 1, 4))
    return max(areas)

def Q10Ans(n):
    total = n**2
    total *= 2**n # this is the formula for the time complexity of the must efficient algorithm for solving the travelling salesman problem
    return total

def Q11Ans(n): # finds the longest palindromic substring in n - taken from a Neetcode video on youtube - included in references
    res = ""
    resLen = 0
    for i in range(len(n)):
        # odd length
        l,r = i,i # left and right pointers
        while l >= 0 and r < len(n) and n[l] == n[r]: # while the substring is a palindrome
            if r-l+1 > resLen: # update the result if the substring is longer than the current result
                res = n[l:r+1]
                resLen = r-l+1
            l -= 1 # move the pointers
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

def Q12Ans(n, target): # finds the indices of the two numbers in n that add up to target - taken from a Neetcode video - included in references
    prevMap = {} # dictionary to store the indices of the numbers, updated as move through the list
    for i, n in enumerate(n):
        diff = target - n
        if diff in prevMap:
            return [prevMap[diff], i]
        prevMap[n] = i

def Q13Ans(n): # finds the number of ways of getting up a set of stairs with n steps - taken from a Neetcode video - included in references
    one, two = 1,1
    for i in range(n - 1):
        temp = one # using temp variable to reduce the memory used by the algorithm
        one = one + two
        two = temp
    return one

def Q14Ans(n): # checks if a binary tree is a binary search tree - taken from a Neetcode video - included in references
    
    def valid(node, left, right):
        if not node:
            return True
        
        if not (node.val < right and node.val > left): # criteria for a binary search tree
            return False
        
        return (valid(node.left, left, node.val) and valid(node.right, node.val, right)) # recursively checks the left and right subtrees
    
    return valid(n, float('-inf'), float('inf')) # initial pointers are -infinity and infinity

def Q15Ans(n): # standard merge sort algorithm - used a tutorial from Nvidia developer blog - included in references
    list_length = len(n)
    if list_length == 1:
        return n
    mid_point = list_length // 2 # used to split the lists
    left = Q15Ans(n[:mid_point]) # recursively calls the function to split the list into smaller lists
    right = Q15Ans(n[mid_point:])
    return merge(left, right)

def merge(left, right):
    output = []
    i = j = 0
    while i < len(left) and j < len(right): # merges the lists back together in order
        if left[i] < right[j]:
            output.append(left[i])
            i += 1
        else:
            output.append(right[j])
            j += 1
    output.extend(left[i:]) # appends the rest of the list to the output
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
        
        
