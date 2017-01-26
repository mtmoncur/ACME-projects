# image_segmentation.py
"""Volume 1A: Image Segmentation.
<Tyler>
<Blue>
<10/31/16>
"""
import numpy as np
from matplotlib import pyplot as plt
from scipy import linalg as la
from scipy.sparse import linalg as spla
from scipy import sparse


# Problem 1: Implement this function.
def laplacian(A):
    '''
    Compute the Laplacian matrix of the adjacency matrix A.
    Inputs:
        A (array): adjacency matrix for undirected weighted graph,
             shape (n,n)
    Returns:
        L (array): Laplacian matrix of A

    '''
    diagonal = np.sum(A, axis = 0)
    return np.diag(diagonal) - A

    raise NotImplementedError("Problem 1 Incomplete")

# Problem 2: Implement this function.
def n_components(A,tol=1e-8):
    '''
    Compute the number of connected components in a graph
    and its algebraic connectivity, given its adjacency matrix.
    Inputs:
        A -- adjacency matrix for undirected weighted graph,
             shape (n,n)
        tol -- tolerance value
    Returns:
        n_components -- the number of connected components
        lambda -- the algebraic connectivity
    '''
    L = laplacian(A)
    eigenvalues = np.real(la.eig(L)[0])


    zeros = eigenvalues<tol
    eigenvalues[zeros] = 0.0

    order = sorted(eigenvalues.tolist())
    n = sum(zeros)
    return n, order[1]

# Problem 3: Implement this function.
def adjacency(filename="dream.png", radius = 5.0, sigma_I = .02, sigma_d = 3.0):
    '''
    Compute the weighted adjacency matrix for
    the image given the radius. Do all computations with sparse matrices.
    Also, return an array giving the main diagonal of the degree matrix.

    Inputs:
        filename (string): filename of the image for which the adjacency matrix will be calculated
        radius (float): maximum distance where the weight isn't 0
        sigma_I (float): some constant to help define the weight
        sigma_d (float): some constant to help define the weight
    Returns:
        W (sparse array(csc)): the weighted adjacency matrix of img_brightness,
            in sparse form.
        D (array): 1D array representing the main diagonal of the degree matrix.
    '''
    def w(p1, pt2, d):
        exponent = np.abs(brt[p1]-brt[pt2])/sigma_I
        exponent += d/sigma_d
        return np.exp(-exponent)
        
    clr_pic, brt = getImage(filename)
    m,n = brt.shape
    brt = brt.flatten()

    W = sparse.lil_matrix((m*n,m*n))
    
    #build the rows, ignoring the diagonal and all entries below it
    for pt in range(m*n):
            near_pts, dist = getNeighbors(pt, radius, m, n)
            row = np.zeros_like(brt).astype(np.float64)

            row = w(pt, near_pts, dist)

            W[pt, near_pts] = row

    I = sparse.identity(m*n)

    #make the degree matrix
    d = W.sum(axis = 0)

    return W, d

# Problem 4: Implement this function.
def segment(filename="dream.png"):
    '''
    Compute and return the two segments of the image as described in the text.
    Compute L, the laplacian matrix. Then compute D^(-1/2)LD^(-1/2),and find
    the eigenvector corresponding to the second smallest eigenvalue.
    Use this eigenvector to calculate a mask that will be usedto extract
    the segments of the image.
    Inputs:
        filename (string): filename of the image to be segmented
    Returns:
        seg1 (array): an array the same size as img_brightness, but with 0's
                for each pixel not included in the positive
                segment (which corresponds to the positive
                entries of the computed eigenvector)
        seg2 (array): an array the same size as img_brightness, but with 0's
                for each pixel not included in the negative
                segment.
    '''
    W, d = adjacency(filename)


    clr_pic, brt = getImage(filename)
    clr_pic = clr_pic[:,:,:3]

    m,n = brt.shape

    dnew = 1/np.sqrt(d)
    Dnew = sparse.spdiags(dnew, 0, m*n, m*n)

    D = sparse.spdiags(d, 0, m*n, m*n)
    L = D - W

    A = Dnew.dot(L.dot(Dnew))

    lambdas, vect = spla.eigsh(A, k=6, which='SM')
    ind = np.argmin(lambdas)
    lambdas[ind] = np.max(lambdas)
    ind = np.argmin(lambdas)
    eig_v = vect[:,ind]

    eig_v = eig_v.reshape((m, n))

    pos = eig_v > 0

    clr_pos = np.zeros_like(clr_pic)
    clr_neg = np.zeros_like(clr_pic)

    clr_pos[:,:,0] = clr_pic[:,:,0]*pos
    clr_pos[:,:,1] = clr_pic[:,:,1]*pos
    clr_pos[:,:,2] = clr_pic[:,:,2]*pos

    clr_neg[:,:,0] = clr_pic[:,:,0]*~pos
    clr_neg[:,:,1] = clr_pic[:,:,1]*~pos
    clr_neg[:,:,2] = clr_pic[:,:,2]*~pos

    displayPosNeg(clr_pic, brt*pos, brt*(~pos))
    displayPosNeg(clr_pic, clr_pos, clr_neg)

    return brt*pos, brt*(~pos)

# Helper function used to convert the image into the correct format.
def getImage(filename='dream.png'):
    '''
    Reads an image and converts the image to a 2-D array of brightness
    values.

    Inputs:
        filename (str): filename of the image to be transformed.
    Returns:
        img_color (array): the image in array form
        img_brightness (array): the image array converted to an array of
            brightness values.
    '''
    img_color = plt.imread(filename)
    img_brightness = (img_color[:,:,0]+img_color[:,:,1]+img_color[:,:,2])/3.0
    return img_color,img_brightness

# Helper function for computing the adjacency matrix of an image
def getNeighbors(index, radius, height, width):
    '''
    Calculate the indices and distances of pixels within radius
    of the pixel at index, where the pixels are in a (height, width) shaped
    array. The returned indices are with respect to the flattened version of the
    array. This is a helper function for adjacency.

    Inputs:
        index (int): denotes the index in the flattened array of the pixel we are
                looking at
        radius (float): radius of the circular region centered at pixel (row, col)
        height, width (int,int): the height and width of the original image, in pixels
    Returns:
        indices (int): a flat array of indices of pixels that are within distance r
                   of the pixel at (row, col)
        distances (int): a flat array giving the respective distances from these
                     pixels to the center pixel.
    '''
    # Find appropriate row, column in unflattened image for flattened index
    row, col = index/width, index%width
    # Cast radius to an int (so we can use arange)
    r = int(radius)
    # Make a square grid of side length 2*r centered at index
    # (This is the sup-norm)
    x = np.arange(max(col - r, 0), min(col + r+1, width))
    y = np.arange(max(row - r, 0), min(row + r+1, height))
    X, Y = np.meshgrid(x, y)
    # Narrows down the desired indices using Euclidean norm
    # (i.e. cutting off corners of square to make circle)
    R = np.sqrt(((X-np.float(col))**2+(Y-np.float(row))**2))
    mask = (R<radius)
    # Return the indices of flattened array and corresponding distances
    return (X[mask] + Y[mask]*width, R[mask])

# Helper function used to display the images.
def displayPosNeg(img_color,pos,neg):
    '''
    Displays the original image along with the positive and negative
    segments of the image.

    Inputs:
        img_color (array): Original image
        pos (array): Positive segment of the original image
        neg (array): Negative segment of the original image
    Returns:
        Plots the original image along with the positive and negative
            segmentations.
    '''
    plt.subplot(131)
    plt.imshow(neg)
    plt.subplot(132)
    plt.imshow(pos)
    plt.subplot(133)
    plt.imshow(img_color)
    plt.show()