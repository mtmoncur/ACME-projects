from fractions import Fraction, gcd

class matrix(object):
    def __init__(self, l):
        self.mat = l
        n = 0
        m = len(l)
        if m>0:
            n = len(l[0])
        else:
            n = m
            m = 1
        self.dim = (m,n)
    
    #transpose
    def T(self):
        m, n = self.dim
        
        if m == 1:
            return matrix([[i] for i in self.mat])
        new_list = []
        for j in range(n):
            new_list.append([0]*m)
            for i in range(m):
                new_list[j][i] = self.mat[i][j]
        return matrix(new_list)
    
    #matrix multiplication
    def __mult__(self, other):
        m,n = self.dim
        n,k = other.dim
        new_list = []
        for i in range(m):
            new_list.append([0]*k)
            for j in range(k):
                total = 0
                for x in range(n):
                    total+=self.l[i][x]*other.l[x][j]
                new_list[i][j] = total
        return matrix(new_list)
    
    #reduce row eschelon form    
    def rref(self):
        lead = 0
        rows, cols = self.dim
        for r in range(rows):
            if lead >= cols:
                break
            i = r
            while self.mat[i][lead] == 0:
                i+=1
                if rows == i:
                    i = r
                    lead += 1
                    if cols == lead:
                        break
            temp = self.mat[i]
            self.mat[i] = self.mat[r]
            self.mat[r] = temp
            
            if self.mat[r][lead] != 0:
                k = self.mat[r][lead]
                for x in range(cols):
                    self.mat[r][x] /= k
            
            for i in range(rows):
                if i != r:
                    k = self.mat[i][lead]
                    for x in range(cols):
                        self.mat[i][x] -= self.mat[r][x]*k
            lead += 1

def answer(m):
    """
    Args:
        m(list) - a nested list matrix showing transitions ratios between states

    Description:
        Finds the exact probability for the material to end in each terminating
        state using matrix operations. Returns in the format of
        (numerator1, numerator2, ..., denominator)
    """
    n = len(m)
    term = []   #list of terminating states
    not_term = []   #list of non-terminating states
    

    if n != len(m[0]):
        raise Exception("The input matrix must be square.")

    for i,row in enumerate(m):
        total = sum(row)
        if total != 0:
            for x in range(n):
                #normalize each row to add to 1, making probabilities
                m[i][x] = Fraction(m[i][x],total)

            not_term.append(i)

        else:
            term.append(i)

    #remove the rows of terminating states
    for i in term[::-1]:
        m.pop(i)

    m = matrix(m)
    m = m.T()
    A = []
    B = []
    
    x, y = m.dim()
    if x!=n:
        raise Exception("The new matrix has unexpected dimensions.")
    
    for i in not_term:
        A.append(m.mat[i] + [Fraction(0,1)])
    for i in term:
        B.append(m.mat[i])
    A[0][-1] = Fraction(1,1)
    A = matrix(A)
    B = matrix(B)
    n,k = A.dim
    p,q = B.dim
    
    #get A - I
    for i in range(n):
        A.mat[i][i] = A.mat[i][i] - 1
    
    #solve in place, the last column of A is the
    #first column of A^-1
    A.rref()
    sol = []

    #print A.mat
    #print "B", B.mat
    for i in range(p):
        total = 0
        for j in range(q):
            total += A.mat[j][-1]*B.mat[i][j]
        sol.append(total)
    
    #print sol
    lcm  = 1
    numers = []
    denoms = []
    for i in sol:
        d = i.denominator
        numers.append(i.numerator)
        denoms.append(d)
        lcm = lcm*d/gcd(lcm,d)

    for i in range(len(numers)):
        numers[i] = -1*numers[i]*lcm/denoms[i]
        
    return numers + [lcm]