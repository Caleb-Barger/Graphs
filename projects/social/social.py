import random

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)


class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.reset()

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("warning: friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        create a new user with a sequential integer id
        """
        self.last_id += 1  # automatically increment the id to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def reset(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}
    
    def populate_graph(self, num_users, avg_friendships):
        """
        takes a number of users and an average number of friendships
        as arguments

        creates that number of users and a randomly distributed friendships
        between those users.

        the number of users must be greater than the average number of friendships.
        """
        # reset graph
        self.reset()
        
        # add users
        for i in range(num_users):
            self.add_user(f"user {i}")

         # create friendships
        possible_friendships = []
        
        for user_id in self.users:
            for friend_id in range(user_id + 1, self.last_id + 1):
                possible_friendships.append((user_id, friend_id))
        
        random.shuffle(possible_friendships)

        for i in range(num_users * avg_friendships // 2):
            friendships = possible_friendships[i]
            self.add_friendship(friendships[0], friendships[1])

    def get_neighbors(v):
        return self.friendships[v] # i think this is all this needs to do?

    def get_all_social_paths(self, user_id):
        """
        takes a user's user_id as an argument

        returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        the key is the friend's id and the value is the path.
        """
        visited = {}  # note that this is a dictionary, not a set

        # initalize a queue
        q = Queue()
        # start quqeue with the inital user 
        q.enqueue([user_id])
        # while the queue is not empty
        while q.size() > 0:
            # deque from queue and store as path
            path = q.dequeue()
            # grab the last person from path
            v = path[-1]
            # if that person is not in the visted path
            if v not in visited:
                # add that person to the visited dict
                visited[v] = path

                # iterate over the persons neighbors
                for neighbor in self.friendships[v]:
                    # make a copy of the current path
                    path_copy = list(path)
                    # add the neighbor to the end of the copied path
                    path_copy.append(neighbor)
                    # add the copied path to the queue
                    q.enqueue(path_copy)


        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)

