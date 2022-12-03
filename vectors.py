def zeros(l: list[int]) -> bool:
    """Checks if vector is all zeros

    Parameters: 
        l: vector to check

    Returns:
        bool: A bool indicating if the list is all 0s
    """
    # list comprehension returns list of bools, check if all are true
    return all(v == 0 for v in l)

def lessThanEqual(arr1: list[int], arr2: list[int]) -> bool:
    """Checks if all elements in arr1 are less than or equal to arr2 in same index position

    Parameters: 
        arr1: vector to check each element less than or equal
        arr2: vector to compare to

    Returns:
        bool: A bool indicating if each element in arr1 is less than or equal to arr2 in the same position.
    """
    # iterates through both arrays at same time. If any element in arr1 is greater than arr2 counterpart, returns False
    for (i,j) in zip(arr1, arr2):
        if i > j:
            return False
    return True

def addVector(l1: list, l2: list, inplace=True) -> list:
    """Adds each element in l1 to l2. If inplace, l1 is mutated. Else, returns a new array.

    Parameters: 
        l1: vector to add
        l2: vector to add
        inplace: determines if vector is returned or l1 is mutated

    Returns:
        if not inplace:
            list: list with sum of each element in each position.
    """
    if inplace:
        # iterates through l1 and l2 at same time
        for i, (x,y) in enumerate(zip(l1,l2)):
            l1[i] = x+y
    else:
        # list comprehension to return an array with sums
        return [x+y for x,y in zip(l1,l2)]

def addMatrix(m1: list[list[int]], m2: list[list[int]], inplace=True) -> list[list[int]]:
    """Adds each element in m1 to element in same position in m2. If inplace, l1 is mutated. Else, returns a new array.

    Parameters: 
        l1: 2-D matrix to add
        l2: 2-D matrix to add
        inplace: determines if new matrix is returned or m1 is mutated

    Returns:
        if not inplace:
            list[list[int]]: mutex with sum of each element in each position.
    """
    if inplace:
        # iterates through l1 and l2 at same time
        for l1,l2 in zip(m1,m2):
            subtractVector(l1, l2)
    else:
        # list comprehension to return an array with arrays of sums
        return [addVector(row1, row2, inplace=False) for row1, row2 in zip(m1,m2)]

def subtractVector(l1: list, l2: list, inplace=True) -> list:
    """Subtracts each element in l1 to l2. If inplace, l1 is mutated. Else, returns a new array.

    Parameters: 
        l1: The minuend vector
        l2: The subtrahend vector
        inplace: determines if new vector is returned or l1 is mutated

    Returns:
        if not inplace:
            list: list with difference of each element in each position.
    """
    if inplace:
        # iterates through l1 and l2 at same time
        for i, (x,y) in enumerate(zip(l1,l2)):
            l1[i] = x-y
    else:
        # list comprehension to return an array with arrays of differences
        return [x-y for x,y in zip(l1,l2)]

def subtractMatrix(m1: list[list[int]], m2: list[list[int]], inplace=True) -> list:
    """Subtract each element in m1 to element in same position in m2. If inplace, l1 is mutated. Else, returns a new array.

    Parameters: 
        l1: The minuend 2-D matrix 
        l2: The subtrahend 2-D matrix
        inplace: determines if new matrix is returned or m1 is mutated

    Returns:
        if not inplace:
            list[list[int]]: mutex with difference of each element in each position.
    """
    if inplace:
        # iterates through l1 and l2 at same time
        for l1,l2 in zip(m1,m2):
            subtractVector(l1, l2)
    else:
        # list comprehension to return an array with arrays of differences
        return [subtractVector(row1, row2, inplace=False) for row1, row2 in zip(m1,m2)]
