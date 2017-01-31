# svd_image_compression.py
"""Volume 1A: SVD and Image Compression.
<Tyler>
<Blue>
<10/25/16>
"""

from scipy import linalg as la
import numpy as np
from matplotlib import pyplot as plt
from numpy import ndarray

class myarray(ndarray):
    #use code below to implement
    #V = V.view(myarray)
    @property
    def H(self):
        return self.conj().T

# Problem 1
def truncated_svd(A,k=None):
    """Computes the truncated SVD of A. If r is None or equals the number
        of nonzero singular values, it is the compact SVD.
    Parameters:
        A: the matrix
        k: the number of singular values to use
    Returns:
        U - the matrix U in the SVD
        s - the diagonals of Sigma in the SVD
        Vh - the matrix V^H in the SVD
    """
    
    A = A.view(myarray).astype(np.float64)
    m,n = A.shape

    eigs, vect = la.eig(A.H.dot(A))
    eigs = np.sqrt(eigs)

    #print "here", vect
    #first, place eigenvalues with their vectors into dictionary
    #np.argsort()
    dct = {}
    for i,e in enumerate(eigs):
        dct[e] = vect[:,i]

    #eliminate zero valued eigenvalues
    length = len(dct)
    for i in range(length):
        if np.abs(eigs[i]) < 1e-10:
            dct.pop(eigs[i])

    #sort eigenvalues in descending order, and make V and sigma
    order = np.asarray(sorted(dct, reverse=True))
    eig_cnt = len(order)
    sigma = np.diag(order)
    
    V = np.zeros((n, eig_cnt))
    for col,eigval in enumerate(order):
        V[:,col] = dct[eigval]

    #make truncated V and sigma, if necessary
    if k is not None and k < eig_cnt:
        sigma = sigma[:k,:k]
        V = V[:,k]

    #calculate U matrix
    U = A.dot(V)/order

    return U, np.diag(sigma), V.conj().T

# Problem 2
def visualize_svd():
    """Plot each transformation associated with the SVD of A."""
    A = np.array([[3,1],[1,3]])
    U, sigma, Vh = map(np.real, truncated_svd(A))
    sigma = np.diag(sigma)
    theta = np.linspace(0,2*np.pi, 100)
    x = np.cos(theta)
    y = np.sin(theta)
    S = np.vstack([x,y])

    e1 = np.array([[0,1],[0,0]])
    e2 = np.array([[0,0],[0,1]])

    #plot original circle
    plt.subplot(221)
    plt.title('Original', fontsize=18)
    plt.axis('equal')
    plt.plot(S[0,:], S[1,:])
    plt.plot(e1[0,:], e1[1,:], "g")
    plt.plot(e2[0,:], e2[1,:], "g")
    
    #apply Vh
    S = Vh.dot(S)
    e1 = Vh.dot(e1)
    e2 = Vh.dot(e2)
    plt.subplot(222)
    plt.title('Apply $V^{H}$', fontsize=18)
    plt.axis('equal')
    plt.plot(S[0,:], S[1,:])
    plt.plot(e1[0,:], e1[1,:], "g")
    plt.plot(e2[0,:], e2[1,:], "g")
    
    #apply Sigma
    S = sigma.dot(S)
    e1 = sigma.dot(e1)
    e2 = sigma.dot(e2)
    plt.subplot(223)
    plt.title('Apply $\Sigma V^{H}$', fontsize=18)
    plt.axis('equal')
    plt.plot(S[0,:], S[1,:])
    plt.plot(e1[0,:], e1[1,:], "g")
    plt.plot(e2[0,:], e2[1,:], "g")
    
    #apply U
    S = U.dot(S)
    e1 = U.dot(e1)
    e2 = U.dot(e2)
    plt.subplot(224)
    plt.title('Apply $U \Sigma V^{H}$', fontsize=18)
    plt.axis('equal')
    plt.plot(S[0,:], S[1,:])
    plt.plot(e1[0,:], e1[1,:], "g")
    plt.plot(e2[0,:], e2[1,:], "g")

    plt.show()

# Problem 3
def svd_approx(A, k):
    """Returns best rank k approximation to A with respect to the induced 2-norm.

    Inputs:
    A - np.ndarray of size mxn
    k - rank

    Return:
    Ahat - the best rank k approximation
    """
    U, s, Vh = la.svd(A, full_matrices = False)
    S = np.diag(s[:k])
    Ahat = U[:,:k].dot(S).dot(Vh[:k,:])
    return Ahat

# Problem 4
def lowest_rank_approx(A,e):
    """Returns the lowest rank approximation of A with error less than e
    with respect to the induced 2-norm.

    Inputs:
    A - np.ndarray of size mxn
    e - error

    Return:
    Ahat - the lowest rank approximation of A with error less than e.
    """
    U, s, Vh = la.svd(A, full_matrices = False)
    k = sum(s>e)

    S = np.diag(s[:k])

    Ahat = U[:,:k].dot(S).dot(Vh[:k,:])
    return Ahat

# Problem 5
def compress_image(filename,k):
    """Plot the original image found at 'filename' and the rank k approximation
    of the image found at 'filename.'

    filename - jpg image file path
    k - rank
    """
    color_pic = plt.imread(filename)[:,:,:].astype(float)

    color_pic = color_pic/255
    comp_pic = color_pic.copy()

    comp_pic[:,:,0] = svd_approx(comp_pic[:,:,0], k)
    comp_pic[:,:,1] = svd_approx(comp_pic[:,:,1], k)
    comp_pic[:,:,2] = svd_approx(comp_pic[:,:,2], k)

    comp_pic[comp_pic>1] = 1.
    comp_pic[comp_pic<0] = 0.


    plt.subplot(121)
    plt.title("Original Picture", fontsize=18)
    plt.axis("off")
    plt.imshow(color_pic)

    plt.subplot(122)
    plt.title("Compressed to rank " + str(k), fontsize=18)
    plt.axis("off")
    plt.imshow(comp_pic)
    plt.show()