# markov_chains.py
"""Volume II: Markov Chains.
<Tyler>
<Blue>
<10/19/16>
"""

import numpy as np


# Problem 1
def random_markov(n):
    """Create and return a transition matrix for a random Markov chain with
    'n' states. This should be stored as an nxn NumPy array.
    """
    trm = np.random.random(size=(n,n))
    col_sum = np.sum(trm, axis=0)
    trm = trm/col_sum
    return trm
    raise NotImplementedError("Problem 1 Incomplete")


# Problem 2
def forecast(days):
    """Forecast tomorrow's weather given that today is hot."""
    transition = np.array([[0.7, 0.6], [0.3, 0.4]])

    # Sample from a binomial distribution to choose a new state.
    dw = [0]
    for i in range(days):
        dw.append(np.random.binomial(1, transition[1, dw[-1]]))

    return dw[1:]


# Problem 3
def four_state_forecast(days):
    """Run a simulation for the weather over the specified number of days,
    with mild as the starting state, using the four-state Markov chain.
    Return a list containing the day-by-day results, not including the
    starting day.

    Examples:
        >>> four_state_forecast(3)
        [0, 1, 3]
        >>> four_state_forecast(5)
        [2, 1, 2, 1, 1]
    """
    trm = np.array([[0.5, 0.3, 0.1, 0], [0.3, 0.3, 0.3, 0.3], [0.2, 0.3, 0.4, 0.5], [0, 0.1, 0.2, 0.2]])
    dw = [1]
    for i in range(days):
        outcome = np.random.multinomial(1, trm[:, dw[-1]])
        dw.append(outcome.argmax())
    return dw[1:]
    raise NotImplementedError("Problem 3 Incomplete")


# Problem 4
def steady_state(A, tol=1e-12, N=40):
    """Compute the steady state of the transition matrix A.

    Inputs:
        A ((n,n) ndarray): A column-stochastic transition matrix.
        tol (float): The convergence tolerance.
        N (int): The maximum number of iterations to compute.

    Raises:
        ValueError: if the iteration does not converge within N steps.

    Returns:
        x ((n,) ndarray): The steady state distribution vector of A.
    """
    
    counter = 0
    eps = 10*tol
    m,n = A.shape
    x_old = np.random.random(m)
    x = x_old
    
    while eps > tol and counter < N:
        x = A.dot(x_old)
        eps = np.linalg.norm(x-x_old)
        counter += 1
        x_old = x

    if counter == N:
        raise ValueError("Failure to converge.")

    return x
    raise NotImplementedError("Problem 4 Incomplete")


# Problems 5 and 6
class SentenceGenerator(object):
    """Markov chain creator for simulating bad English.

    Attributes:
        (what attributes do you need to keep track of?)

    Example:
        >>> yoda = SentenceGenerator("Yoda.txt")
        >>> print yoda.babble()
        The dark side of loss is a path as one with you.
    """

    def __init__(self, filename):
        """Read the specified file and build a transition matrix from its
        contents. You may assume that the file has one complete sentence
        written on each line.
        """
        with open(filename,'r') as target:
            training_set = target.read()
        target.close()
        
        lines = training_set.splitlines()
        line_cnt = len(lines)
        for i in range(line_cnt):
            lines[i] = lines[i].split(" ")

        words = set()
        for sentence in lines:
            for w in sentence:
                words.add(w.strip())

        self.words = ['$tart'] + list(words) + ['$top']
        self.num = {}
        for i,n in enumerate(self.words):
            self.num.update({n:i})  #create a dictionary mapping words to their number

        n = len(self.words)
        tran = np.zeros((n,n))
        i = self.num['$top']
        tran[i,i] = 1 #set $top goes to $top

        for sentence in lines:
            prev = '$tart'
            for w in sentence:
                i = self.num[w]
                j = self.num[prev]
                tran[i,j] += 1
                prev = w
            i = self.num['$top']
            j = self.num[prev]
            tran[i,j]+=1

        self.t = tran/np.sum(tran,axis=0)

        #raise NotImplementedError("Problem 5 Incomplete")

    def babble(self):
        """Begin at the start state and use the strategy from
        four_state_forecast() to transition through the Markov chain.
        Keep track of the path through the chain and the corresponding words.
        When the stop state is reached, stop transitioning and terminate the
        sentence. Return the resulting sentence as a single string.
        """
        s = ['$tart']
        while s[-1] != '$top':
            col = self.num[s[-1]]
            outcome = np.random.multinomial(1, self.t[:, col])
            k = outcome.argmax()
            s.append(self.words[k])

        return "".join([i + " " for i in s[1:-1]])[:-1]
        #raise NotImplementedError("Problem 6 Incomplete")
