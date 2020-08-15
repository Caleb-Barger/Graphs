from room import Room
from player import Player
from world import World

from util import Stack 

import random, time
from ast import literal_eval

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

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
# visited = set()
s = Stack()

# populate the graph with the first room
graph[player.current_room.id] = {k:'?' for k in player.current_room.get_exits()}

def op_dir(d):
    if d == 'n':
        dtt = 's'
    if d == 's':
        dtt = 'n'
    if d == 'e':
        dtt = 'w'
    if d == 'w':
        dtt = 'e'

    return dtt

# iterate through this graph entry and add question marks directions to the stack 
# but first add the way to get back from that particular direction
for k, v in graph[player.current_room.id].items():
    if v == '?':
        # first push oposite direction 
        # then push direction
        s.push(op_dir(k))
        s.push(k)

while s.size() > 0:
    print(s.stack)
    d = s.pop()

    prev_room = player.current_room.id
    player.travel(d)
    traversal_path.append(d)

    if player.current_room.id not in graph:
        graph[player.current_room.id] = {k:'?' for k in player.current_room.get_exits()}
    
    # sync up the rooms
    graph[prev_room][d] = player.current_room.id
    graph[player.current_room.id][op_dir(d)] = prev_room

    for k, v in graph[player.current_room.id].items():
        if v == '?':
            s.push(op_dir(k))
            s.push(k)

    finished = True
    for e in graph.keys():
        if '?' in graph[e].values():
            finished = False

    if finished:
        break
            

    


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
