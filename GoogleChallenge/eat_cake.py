def answer(s):
    """
    Args:
        s(list) - a list of the colors

    Descriptions:
        Finds the smallest repeating pattern in the list.
        Uses divisors to find a list of possible answers first,
        then checks them.
    """

    def divisors(n):
        """
        Args:
            n(int)

        Description:
            Returns the divisors of n
        """
        divisors = []
        for i in xrange(1,n+1):
            if n%i == 0:
                divisors.append(i)
        return divisors
    
    n = len(s)
    d = divisors(n)
    
    pieces = 0
    for i in d:
        segment = s[:i]
        #preliminary check
        if s[-1] == segment[-1]:
            #check if list is composed of the repeating pattern
            if s == segment*(n/i):
                pieces = n/i    
                break
    
    print pieces