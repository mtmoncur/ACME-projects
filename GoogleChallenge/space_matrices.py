
'''
Disorderly Escape
=================
Oh no! You've managed to free the bunny prisoners and escape Commander Lambdas exploding space station, but her team of 
elite starfighters has flanked your ship. If you dont jump to hyperspace, and fast, youll be shot out of the sky!
Problem is, to avoid detection by galactic law enforcement, Commander Lambda planted her space station in the middle of a 
quasar quantum flux field. In order to make the jump to hyperspace, you need to know the configuration of celestial bodies 
in the quadrant you plan to jump through. In order to do *that*, you need to figure out how many configurations each quadrant 
could possibly have, so that you can pick the optimal quadrant through which youll make your jump. 
There's something important to note about quasar quantum flux fields' configurations: when drawn on a star grid, 
configurations are considered equivalent by grouping rather than by order. That is, for a given set of configurations, 
if you exchange the position of any two columns or any two rows some number of times, youll find that all of those 
configurations are equivalent in that way - in grouping, rather than order.
Write a function answer(w, h, s) that takes 3 integers and returns the number of unique, non-equivalent configurations that 
can be found on a star grid w blocks wide and h blocks tall where each celestial body has s possible states. Equivalency is 
defined as above: any two star grids with each celestial body in the same state where the actual order of the rows and 
columns do not matter (and can thus be freely swapped around). Star grid standardization means that the width and height 
of the grid will always be between 1 and 12, inclusive. And while there are a variety of celestial bodies in each grid, 
the number of states of those bodies is between 2 and 20, inclusive. 
The answer can be over 20 digits long, so return it as a decimal string.  The intermediate values can also be large, so you 
will likely need to use at least 64-bit integers.
For example, consider w=2, h=2, s=2. We have a 2x2 grid where each celestial body is either in state 0 (for instance, silent) 
or state 1 (for instance, noisy).  We can examine which grids are equivalent by swapping rows and columns.
00
00
In the above configuration, all celestial bodies are "silent" - that is, they have a state of 0 - so any swap of row or 
column would keep it in the same state.
00 00 01 10
01 10 00 00
1 celestial body is emitting noise - that is, has a state of 1 - so swapping rows and columns can put it in any of the 
4 positions.  All four of the above configurations are equivalent.
00 11
11 00
2 celestial bodies are emitting noise side-by-side.  Swapping columns leaves them unchanged, and swapping rows simply 
moves them between the top and bottom.  In both, the *groupings* are the same: one row with two bodies in state 0, one row 
with two bodies in state 1, and two columns with one of each state.
01 10
01 10
2 noisy celestial bodies adjacent vertically. This is symmetric to the side-by-side case, but it is different because 
there's no way to transpose the grid.
01 10
10 01
2 noisy celestial bodies diagonally.  Both have 2 rows and 2 columns that have one of each state, so they are equivalent 
to each other.
01 10 11 11
11 11 01 10
3 noisy celestial bodies, similar to the case where only one of four is noisy.
11
11
4 noisy celestial bodies.
There are 7 distinct, non-equivalent grids in total, so answer(2, 2, 2) would return 7.
Languages
=========
To provide a Python solution, edit solution.py
To provide a Java solution, edit solution.java
Test cases
==========
Inputs:
    (int) w = 2
    (int) h = 2
    (int) s = 2
Output:
    (string) "7"
Inputs:
    (int) w = 2
    (int) h = 3
    (int) s = 4
Output:
    (string) "430"
Use verify [file] to test your solution and see how it does. When you are finished editing your code, use submit [file] to submit your answer. If your solution passes the test cases, it will be removed from your home folder.
'''

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
