# dimensions is a list of dimensions: ['country', 'usertype', 'useragent']
# values is a dictionary of lists, describing the possible values for each dimension,
# like so: {'country': ['SE', 'DE', 'IT'], 'useragent': ['*'], 'usertype': ['anon']}
#
# returns a list of list of strings that describe the column qualifiers to fetch.
def enumerate_cells(dimensions, values, target=[]):
    if dimensions == []:
        # base case.
        return target

    newtarget = []
    if target == []:
        # first time around.
        for value in values[dimensions[0]]:
            newtarget.append([value])
    else:
        for t in target:
            for value in values[dimensions[0]]:
                newtarget.append(t + [value])

    return enumerate_cells(dimensions[1:], values, newtarget)


if __name__ == "__main__":
    print map(lambda l: '-'.join(l), enumerate_cells(['country', 'usertype', 'useragent'],
                                                     {'country': ['SE', 'DE', 'IT'], 'usertype': ['anon', 'user'], 'useragent': ['*']}))
    
    # should print this:
    # ['SE-anon-*', 'SE-user-*', 'DE-anon-*', 'DE-user-*', 'IT-anon-*', 'IT-user-*']


