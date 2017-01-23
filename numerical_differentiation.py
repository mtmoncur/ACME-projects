# numerical_differentiation.py
"""Volume 1B: Numerical Differentiation.
Tyler Moncur
Blue
1/17/17
"""
import numpy as np
from itertools import product as prod
from matplotlib import pyplot as plt

# Problem 1
def centered_difference_quotient(f, pts, h=1e-5):
    """Compute the centered difference quotient for function (f)
    given points (pts).

    Inputs:
        f (function): the function for which the derivative will be
            approximated.
        pts (array): array of values to calculate the derivative.

    Returns:
        An array of the centered difference quotient.
    """
    return (f(pts+h) - f(pts-h))/(2.0*h)

# Problem 2
def calculate_errors(f,df,pts,h = 1e-5):
    """Compute the errors using the centered difference quotient approximation.

    Inputs:
        f (function): the function for which the derivative will be
            approximated.
        df (function): the function of the derivative
        pts (array): array of values to calculate the derivative

    Returns:
        an array of the errors for the centered difference quotient
            approximation.
    """
    return centered_difference_quotient(f, pts, h) - df(pts)

# Problem 3
def prob3():
    """Use the centered difference quotient to approximate the derivative of
    f(x)=(sin(x)+1)^x at x= pi/3, pi/4, and pi/6.
    Then compute the error of each approximation

    Returns:
        an array of the derivative approximations
        an array of the errors of the approximations
    """
    f = lambda x: (np.sin(x) + 1)**x
    df = lambda x: (np.sin(x)+1)**(x-1) * ((np.sin(x)+1) * np.log(np.sin(x)+1) + x * np.cos(x))
    pts = np.array([np.pi/3., np.pi/4., np.pi/6.])
    return centered_difference_quotient(f, pts), calculate_errors(f, df, pts)

# Problem 4
def prob4():
    """Use centered difference quotients to calculate the speed v of the plane
    at t = 10 s

    Returns:
        (float) speed v of plane
    """
    alpha = np.pi/180.*np.array([54.8, 54.06, 53.34])
    beta = np.pi/180*np.array([65.59, 64.59, 63.62])
    a = 500. #meters

    y = lambda al, be: a*np.tan(be)/(np.tan(be) - np.tan(al))
    x = lambda al, be: a*np.tan(al)*np.tan(be)/(np.tan(be) - np.tan(al))
    h = 1.0 #seconds
    dfy = (y(alpha[2],beta[2]) - y(alpha[0], beta[0]))/(2*h)
    dfx = (x(alpha[2],beta[2]) - x(alpha[0], beta[0]))/(2*h)

    return (dfy**2 + dfx**2)**0.5*3600/1000

# Problem 5
def jacobian(f, n, m, pt, h=1e-5):
    """Compute the approximate Jacobian matrix of f at pt using the centered
    difference quotient.

    Inputs:
        f (function): the multidimensional function for which the derivative
            will be approximated.
        n (int): dimension of the domain of f.
        m (int): dimension of the range of f.
        pt (array): an n-dimensional array representing a point in R^n.
        h (float): a float to use in the centered difference approximation.

    Returns:
        (ndarray) Jacobian matrix of f at pt using the centered difference
            quotient.
    """
    ans = np.zeros((m,n))

    fij = lambda i,j, x: f(np.hstack([ pt[:j],np.array([x]),pt[j+1:] ]))[i]

    for j in range(n):
        for i in range(m):
            ans[i,j] = centered_difference_quotient(lambda x:fij(i,j,x), pt[j], h)
    return ans

# Problem 6
def findError():
    """Compute the maximum error of jacobian() for the function
    f(x,y)=[(e^x)sin(y) + y^3, 3y - cos(x)] on the square [-1,1]x[-1,1].

    Returns:
        Maximum error of your jacobian function.
    """
    
    norm = np.linalg.norm
    f = lambda x: np.array([np.exp(x[0]) * np.sin(x[1]) + x[1]**3, 3*x[1] - np.cos(x[0])])
    J = lambda x: np.array([[np.exp(x[0]) * np.sin(x[1]) , np.exp(x[0]) * np.cos(x[1]) + 3.*x[1]**2], [np.sin(x[0]), 3.]])
    #return f, J
    x = np.linspace(-1, 1, 100)
    y = np.linspace(-1, 1, 100)
    
    max_err = 0
    for i, j in prod(x,y):
        v = np.array([i,j])
        J_approx = jacobian(f, 2, 2, v)
        err = norm(J_approx - J(v), ord='fro')
        max_err = max(max_err, err)

    return max_err