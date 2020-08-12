"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)
        else:
            raise IndexError("Invlaid vertex check your args")

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        return self.vertices[vertex_id]

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        # create an empty Queue
        q = Queue()

        # add the starting vertex id
        q.enqueue(starting_vertex)

        # create set for visited verts
        visited = set()

        # while queue is not empty
        while q.size() > 0:
            # deqeue vert
            v = q.dequeue()
            # if it has not been visited
            if v not in visited:
                # visit it
                print(v)
                # mark as visited
                visited.add(v)
                # add all neighbors to the queue
                for n in self.get_neighbors(v):
                    q.enqueue(n)

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        # create an empty Stack
        s = Stack()

        # add the starting vertex
        s.push(starting_vertex)

        # create set for visited verts
        visited = set()

        # while the stack is not empty
        while s.size() > 0:
            # pop vert
            v = s.pop()
            # if vert not visited
            if v not in visited:
                # visit it
                print(v)
                # mark it as visited
                visited.add(v)
                # add all neighbors to the stack
                for n in self.get_neighbors(v):
                    s.push(n)

    def _dftr_helper(self, v, visited):
        
        # mark current node as visited
        # and print it
        visited[v] = True
        print(v, end=' ')

        # iterate through all v's neighbors
        for i in self.vertices[v]:
            if visited[i] == False:
                self._dftr_helper(i, visited)

    def dft_recursive(self, v):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """

        # mark all verticies as not visited
        visited = [False] * (max(self.vertices) + 1)

        # delegate the work to helper
        self._dftr_helper(v, visited)




    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        # make a queue
        q = Queue()

        # add a tuple of starting vertex
        q.enqueue([starting_vertex])

        # make an empty set (visited)
        visited = set()

        # while the queue is not empty
        while q.size() > 0:

            # deqeue path
            path = q.dequeue()

            # if that path has not been visited
            if set(path) not in visited:

                # if last item is destination
                if path[-1] == destination_vertex:

                    # return that path
                    return path

                # otherwise add it to the visited paths
                visited.add(set(path))

                # enqueue path's neighbors
                for n in self.get_neighbors(path[-1]):
                    temp_path = path[:]
                    temp_path.append(n)
                    q.enqueue(temp_path)


    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        # make a Stack
        s = Stack()

        # add the starting path
        s.push([starting_vertex])

        # make empty set
        visited = set()

        # while the stack is not empty
        while s.size() > 0:

            # pop path
            path = s.pop()

            # if the path has not been visited
            if path not in visited:

                # if the last vert is the destenation
                if path[-1] == destination_vertex:

                    # return that path
                    return path

                # otherwise add path to visited paths
                visited.add(path)    

                # push this path's neighbors
                for n in self.get_neighbors(path[-1]):
                    temp_path = path[:]
                    temp_path.append(n)
                    s.push(temp_path)



    def dfs_recursive(self, starting_vertex, destination_vertex, visited=None, path=None):
        if visited is None:
            visited = set()

        if path is None:
            path = []

        visited.add(starting_vertex)

        path = path + [starting_vertex]

        if starting_vertex == destination_vertex:
            return path

        for n in self.get_neighbors(starting_vertex):
            if n not in visited:
                new_path = self.dfs_recursive(n, destination_vertex, visited, path)
                if new_path is None:
                    return new_path

        return None
        



if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    graph.dft(1)
    graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print(graph.dfs(1, 6))
    print(graph.dfs_recursive(1, 6))
