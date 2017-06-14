def answer(l):
    """
    Args:
        l(integer list)

    Description:
        Compute the largest number divisible by 3 that is 
        composed of digits taken from the input list l.
    """
    def largest(l_sub):
        """
        Args:
            l_sub(integer list) - the list of digits

        Returns:
            total(integer) - the largest possible number constructed from the given digits
        """
        
        order = sorted(l_sub, reverse = True)
        total = 0
        for i in order:
            total = total*10 + i
        
        return total
        
    #if the sum of the list is divisible by 3, then any number
    #composed of these digits is divisible by 3
    modsum = sum(l)%3
    if modsum == 0:
        return largest(l)
    

    #sort the digits into their residue class mod 3
    mod1 = []
    mod2 = []
    mod0 = []
    
    for i in l:
        k = i%3
        if k == 0:
            mod0.append(i)
        elif k == 1:
            mod1.append(i)
        else:
            mod2.append(i)

    len1 = len(mod1)
    len2 = len(mod2)
    mod1 = sorted(mod1) #sort so that remove the smallest 1 or 2 elements is easier
    mod2 = sorted(mod2)

    #removing the fewest number of digits
    #so that the remaining ones sum to a multiple of 3
    if modsum == 1:
        if len1 == 0:
            mod2 = mod2[2:] #remove the least two elements
        else:
            mod1 = mod[1:] #remove the least element
            
    else:
        if len2 == 0:
            mod1 = mod1[2:] #remove the least two elements
        else:
            mod2 = mod2[1:] #remove the least element
    
    return largest(mod1+mod2+mod0)