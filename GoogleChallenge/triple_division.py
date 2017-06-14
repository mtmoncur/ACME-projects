def answer(l):
   	"""
	Args:
		l(list) - list of positive integers

	Description:
		Returns the number of triple combinations 
		where the order is the same as the list and
		each number divides the next in the triple.
   	"""
    length = len(l)
    doubles = [0]*length
    triples = [0]*length
    
    #work on the list in reverse order
    for j in range(length-1,0,-1):
        for i in range(j-1, -1, -1):
            if l[j]%l[i] == 0:
                print (i,j)
                doubles[i] += 1
                triples[i] += doubles[j]
    print doubles
    print triples
    return sum(triples)