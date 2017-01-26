# simplex.py
"""Volume 2B: Simplex.
Tyler Moncur
Blue
1/19/17

Problems 1-6 give instructions on how to build the SimplexSolver class.
The grader will test your class by solving various linear optimization
problems and will only call the constructor and the solve() methods directly.
Write good docstrings for each of your class methods and comment your code.

prob7() will also be tested directly.
"""

import numpy as np

# Problems 1-6
class SimplexSolver(object):
    """Class for solving the standard linear optimization problem

                        maximize        c^Tx
                        subject to      Ax <= b
                                         x >= 0
    via the Simplex algorithm.
    """

    def __init__(self, c, A, b):
        """

        Parameters:
            c (1xn ndarray): The coefficients of the linear objective function.
            A (mxn ndarray): The constraint coefficients matrix.
            b (1xm ndarray): The constraint vector.

        Raises:
            ValueError: if the given system is infeasible at the origin.
        """
        #if any( b<0 ):
        #    raise ValueError("System is infeasible at the origin")
        self.A = A
        self.b = b
        self.c = c
        self.x = np.zeros_like(c)
        self.make_tableau()
        self.num_basic = len(b)

    def make_tableau(self):
        s = self
        m,n = s.A.shape
        topRow = np.hstack( [-s.c, np.zeros(m), 0] )
        middle = np.column_stack( [s.A, np.eye(m), s.b] )
        s.tab = np.vstack([topRow, middle])
        s.L = np.array(range(n,n+m) + range(n))

    def next_pivot_row(self, col):
        #temp is the column to divide by
        temp = self.tab[1:,col].copy()
        temp[temp==0] = -1  #remove any zeros
        temp = self.tab[1:,-1]/temp
        
        #check if there is a restricted row
        if all(temp < 0):
            raise ValueError("No optimal solution. The feasible set is unbounded.")
        #eliminate negatives as a possible answer by setting them to 1+the largest value
        M = np.max(temp)
        temp[temp<0] = M + 1
        r = np.argmin(temp)
        
        return r + 1
        

    def next_pivot_col(self):
        for i in range(self.num_basic,len(self.L)):
            c = self.L[i]
            if self.tab[0,c] < 0:
                c = self.L[i]
                return c

        #we have reached the optimal solution, so there are no more pivot columns
        return False

    def pivot(self, r, c):
        #r is the index of row of the dictionary, and c is the index of the variable. So we could swap row with its own 
        #variable index and the dictionary would remain unchanged
        s = self
        temp = sum((s.L==c)*np.arange(len(s.L))) #get the index of the column in L
        s.L[r-1], s.L[temp] = c, s.L[r-1]
        
        s.tab[r] /= s.tab[r,c]
        for i,val in enumerate(self.tab[:,c]):
            if i==r: continue
            self.tab[i] -= val*self.tab[r]
        print self

    def __str__(self):
        mat = np.round(np.column_stack([self.tab[:,-1],-self.tab[:,self.L[self.num_basic:]]]),3)
        return str(mat)

    def solve(self):
        """Solve the linear optimization problem.

        Returns:
            (float) The maximum value of the objective function.
            (dict): The basic variables and their values.
            (dict): The nonbasic variables and their values.
        """
        while True:
            c = self.next_pivot_col()
            if c is False:
                temp = self.tab[:,-1]
                opt_val = temp[0]
                vals = temp[1:]
                basic = self.L[:self.num_basic].tolist()
                non_basic = self.L[self.num_basic:].tolist()
                basic_dct = {}
                non_basic_dct = {}

                for i in self.L:
                    if i not in basic:
                        non_basic_dct[i] = 0
                    else:
                        basic_dct[i] = vals[basic.index(i)]

                return opt_val, basic_dct, non_basic_dct

            r = self.next_pivot_row(c)
            self.pivot(r,c)


# Problem 7
def prob7(filename='productMix.npz'):
    """Solve the product mix problem for the data in 'productMix.npz'.

    Parameters:
        filename (str): the path to the data file.

    Returns:
        The minimizer of the problem (as an array).
    """
    data = np.load(filename)
    m, n = data['A'].shape 
    A = np.vstack([data['A'], np.eye(n)])
    b = np.hstack([data['m'] , data['d']])
    SS = SimplexSolver(data['p'], A, b)

    profit, basic_var, non_basic_var = SS.solve()

    x = [0] * n
    for i in range(n):
        if i in basic_var:
            x[i] = basic_var[i]
    return x
