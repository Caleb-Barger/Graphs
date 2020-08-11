class Parent:
    def __init__ (self, v, d):
        self.v = v
        self.distance = d

def earliest_ancestor(ancestors, v, parents=None, distance=1):
    # initalize parents if there is no list
    if parents is None:
        parents = []

    # iterate over each edge in the ancestors
    for edge in ancestors:
        # if v is found in edge[1]
        if edge[1] == v:
            # instantaite a new parent and add it to parents
            parent_ref = Parent(edge[0], distance)
            parents.append(parent_ref)
            # increment distance
            distance += 1
            # call self with new v
            return earliest_ancestor(ancestors, parent_ref.v, parents, distance)
    # if no parent was found return None
    # return None
    
    if len(parents) == 0:
        return -1
    
    values = [p.distance for p in parents]
    greatest_distance = max(values)
    
    contenders = []
    
    for p in parents:
        if p.distance == greatest_distance:
            contenders.append(p)
            
    r = max([p.v for p in contenders])
    
    return r

test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]
earliest_ancestor(test_ancestors, 6)