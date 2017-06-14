stored = {}
for i in range(2, 20):
    min_bricks = i*(i+1)/2
    stored[(min_bricks, i)] = 1

def stairs(b, st):
    """
    Args:
        b(int) - the number of bricks to work with
        st(int) - the number of steps in the staircase

    Description:
        Find the number of ways to build a suitable
        staircase that has b bricks and st steps.
        Uses top-down dynamic programming.
    """
    if b < (st*(st+1))/2:
        return 0
    
    elif st == 1:
        return 1
    
    elif st == 2:
        return (b-1)/2

    elif (b,st) in stored:
        return stored[(b,st)]
    
    else:
        total = 0
        total += stairs(b-st, st) + stairs(b-st,st-1)
        stored[(b, st)] = total
        return total

def answer(n):
    """
    Args:
        n(int) - the number of bricks to work with

    Description:
        Find the number of ways to build a suitable
        staircase that has n base bricks. Uses top-down
        dynamic programming.
    """
    total = 0
    for i in range(2,20):
        total += stairs(n, i)
    return total