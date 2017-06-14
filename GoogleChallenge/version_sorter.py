def answer(l):
    """
	Args:
		l(list) - a list of strigns of versions in the form x.x.x
		where x is a number

	Description:
		Sorts the versions form oldest to newest.
    """
    dct = {}

    #fill dct with each version in split form
    #so the its items are lists of integers
    for i, version in enumerate(l):
        dct[version] = map(int, l[i].split("."))
        
    version_order = sorted(dct, key = lambda x:dct[x])
    
    return version_order