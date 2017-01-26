# gaussian_quadrature.py
"""Volume 2 Lab 12: Gaussian Quadrature.
Tyler Moncur
Math 321
12/1/16
"""

import numpy as np
from scipy import sparse as sp
from scipy.stats import norm
import matplotlib.pyplot as plt

# Problem 1
def shift(f, a, b, plot=False):
    """Shift the function f on [a, b] to a new function g on [-1, 1] such that
    the integral of f from a to b is equal to the integral of g from -1 to 1.

    Inputs:
        f (function): a scalar-valued function on the reals.
        a (int): the left endpoint of the interval of integration.
        b (int): the right endpoint of the interval of integration.
        plot (bool): if True, plot f over [a,b] and g over [-1,1] in separate
            subplots.

    Returns:
        The new, shifted function.
    """

    avg = (a+b)/2.0
    m = (b-a)/2.0
    new_f = lambda x: f(m*x+avg)

    if plot:
        plt.subplot(121)
        x = np.linspace(a,b,300)
        y = f(x)
        plt.subplot(121)
        plt.plot(x,y)

        x = np.linspace(-1,1,300)
        y = new_f(x)
        plt.subplot(122)
        plt.plot(x,y)

        plt.show()

    return new_f

# Problem 2
def estimate_integral(f, a, b, points, weights):
    """Estimate the value of the integral of the function f over [a,b].

    Inputs:
        f (function): a scalar-valued function on the reals.
        a (int): the left endpoint of the interval of integration.
        b (int): the right endpoint of the interval of integration.
        points ((n,) ndarray): an array of n sample points.
        weights ((n,) ndarray): an array of n weights.

    Returns:
        The approximate integral of f over [a,b].
    """
    g = shift(f,a,b)
    return (b-a)/2.0*np.sum(weights*g(points))


# Problem 3
def construct_jacobi(gamma, alpha, beta):
    """Construct the Jacobi matrix."""
    a = -beta/alpha
    b = ((gamma[1:])/(alpha[:-1]*alpha[1:]))**0.5
    return sp.diags([b, a, b], [-1, 0, 1]).toarray()

# Problem 4
def points_and_weights(n):
    """Calculate the points and weights for a quadrature over [a,b] with n
    points.

    Returns:
        points ((n,) ndarray): an array of n sample points.
        weights ((n,) ndarray): an array of n weights.
    """
    gamma = np.zeros(n)
    alpha = np.zeros(n)
    beta = np.zeros(n)

    for i in range(1,n+1):
        gamma[i-1] = float(i-1)/i
        alpha[i-1] = (2.0*i-1)/i

    A = construct_jacobi(gamma, alpha, beta)
    #print A
    eigval, eigvect = np.linalg.eig(A)
    order = np.argsort(eigval)
    points = np.real(eigval[order])
    weights = 2*np.real(eigvect[0,order])**2
    return points, weights

# Problem 5
def gaussian_quadrature(f, a, b, n):
    """Using the functions from the previous problems, integrate the function
    'f' over the domain [a,b] using 'n' points in the quadrature.
    """
    pts, wts = points_and_weights(n)
    return estimate_integral(f, a, b, pts, wts)


# Problem 6
def normal_cdf(x):
    """Use scipy.integrate.quad() to compute the CDF of the standard normal
    distribution at the point 'x'. That is, compute P(X <= x), where X is a
    normally distributed random variable with mean = 0 and std deviation = 1.
    """
    f = lambda t: np.exp(-t**2/2)/np.sqrt(2*np.pi)

    if x<-4:
        return gaussian_quadrature(f, x-5, x, 20)
    else:
        return gaussian_quadrature(f, -5, x, 20)