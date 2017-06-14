from itertools import combinations

def answer(num_buns, num_required):
	"""
	Args:
		num_buns(int) - number of bunnies
		num_required(int) -  number of bunnies required to unlock any door

	Description:
		Finds the keys distribution that shows which bunnies needs
		which keys to meet the criteria. Using combinations iterator
		to solve.
	"""
    key_dist_list = [[] for i in range(num_buns)]

    #below, each bun_list shows which bunnies need to have the key numbered as key_num
    for key_num, bun_list in enumerate(combinations(range(num_buns),num_buns - num_required+1)):
        for bun in bun_list:
            key_dist_list[bun].append(key_num)

    return key_dist_list