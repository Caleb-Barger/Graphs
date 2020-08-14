from room import Room
from player import Player
from world import World


from util import Stack 

import random, time
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
graph = {}

# initalize a stack and the first room
s = Stack()
current_room = player.current_room.id

# populate the stack and graph with starting room info
graph[current_room] = {k:'?' for k in player.current_room.get_exits()}

for k in graph[current_room].keys():
    s.push(k)

def link_rooms(prev_room, current_room, d):
    graph[prev_room][d] = current_room

    if d == 'n':
        dtc = 's' # direction to connect
    elif d == 's':
        dtc = 'n'
    elif d == 'e':
        dtc = 'w'
    elif d == 'w':
        dtc = 'e'

    graph[current_room][dtc] = prev_room

while s.size() > 0:
    d = s.pop()

    if graph[current_room][d] == '?':

        # ok just called explore with North and room 0
        prev_room = current_room # store refrence to the prev room

        player.travel(d) # move player
        
        traversal_path.append(d) # add the step to path
        
        current_room = player.current_room.id # assign new current_room
        
        # if the current room does not have an entry in the graph build one
        if current_room not in graph:
            graph[current_room] = {k:'?' for k in player.current_room.get_exits()}

        link_rooms(prev_room, current_room, d) # updates the graph

        # look at new rooms neighbors
        for k in graph[current_room].keys():
            s.push(k)

#    print(traversal_path)
    print(s.stack)



# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#  cmds = input("-> ").lower().split(" ")
#  if cmds[0] in ["n", "s", "e", "w"]:
#      player.travel(cmds[0], True)
#  elif cmds[0] == "q":
#      break
#  else:
#      print("I did not understand that command.")
