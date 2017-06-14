import fractions as fr
import math

def partitions(n):
	# base case of recursion: zero is the sum of the empty list
	if n == 0:
		yield []
		return
		
	# modify partitions of n-1 to form partitions of n
	for p in partitions(n-1):
		yield [1] + p
		if p and (len(p) < 2 or p[1] > p[0]):
			yield [p[0] + 1] + p[1:]

def c_i(j, k, s):
	total = 0
	for i in range(len(k)):
		total += fr.gcd(i+1,j)*k[i]
	return s**total

def change_part(ar,k):
	k = [0]*len(k)
	for i in ar:
		k[i-1] += 1
	return k

def Z_maker(n):
	k = [0]*n
	coef = {}
	for i in partitions(n):
		k = change_part(i,k)
		denom = 1
		for j in range(1,n+1):
			denom *= j**k[j-1]*fact[k[j-1]]
		coef[tuple(i)] = fact[n]/denom
	return coef

def Z_func(h, k, s):
	c = [c_i(i+1, k, s) for i in range(h)]
	total = 0
	for i in myZ.keys():
		term = 1
		for xi in i:
			term *= c[xi-1]
		total += term*myZ[i]
	return total/fact[h]

def answer(w, h, s):
	"""
	Args:
		w(int) - width of matrix
		h(int) - height of matrix
		s(int) - number of possible entries

	Description:
		Returns the number of distinct matrices given w, h, s, 
		and that two matrices are equivalent if one changed be
		created from the other by a permutation of rows and
		columns. Method used here is described at
		http://oeis.org/A005748/a005748.pdf
	"""

	w,h = sorted([w,h])
	global fact, myZ
	fact = {}
	for i in range(h+1):
		fact[i] = math.factorial(i)
	myZ = Z_maker(h)
	
	total = 0
	k = [0]*w
	for i in partitions(w):
		k = change_part(i,k)
		denom = 1
		for j in range(w):
			denom *= fact[k[j]]*(j+1)**k[j]
		numer = fact[w]*Z_func(h, k, s)
		total += numer/denom
	ans = str(total/fact[w])
	if ans[-1] == 'L':
		ans = ans[:-1]
	return ans