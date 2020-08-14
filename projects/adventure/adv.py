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
map_file = "maps/test_loop_fork.txt"
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

visited = set()
s = Stack()

for d in player.current_room.get_exits():
    s.push(d)

visited.add(player.current_room.id)

graph[player.current_room.id] = {k:'?' for k in player.current_room.get_exits()}

while s.size() > 0:
    print(s.stack)
    print(player.current_room.id)
    print()
    time.sleep(.4)
    # print(graph)

    d = s.pop()

    prev_room = player.current_room.id
    player.travel(d) 
    traversal_path.append(d)

    # if this entry is not already in graph make an entry
    if player.current_room.id not in graph:
        graph[player.current_room.id] = {k:'?' for k in player.current_room.get_exits()}

    # update the graph
    graph[prev_room][d] = player.current_room.id

    if d == 'n':
        dta = 's'
    if d == 's':
        dta = 'n'
    if d == 'e':
        dta = 'w'
    if d == 'w':
        dta = 'e'

    graph[player.current_room.id][dta] = prev_room

    if player.current_room.id not in visited:
        held_item = None
        
        for k, v in graph[player.current_room.id].items():
            # if v == '?':
            #     s.push(k)
            if v == '?':
                held_item = k
            else:
                s.push(k)


        # for e in player.current_room.get_exits():
        #     # if e == d or e == 'e' and d == 'w' or e == 'w' and d == 'e':
        #     #     held_item = e
        #     if e == d:
        #         held_item = e
        #     else:
        #         s.push(e)

        if held_item:
            s.push(held_item)

        
        # if s.stack[-2] == 's' or s.stack[-2] == 'n' and s.stack[-1] != 's' and s.size() > 1:
        #     s.stack[-1], s.stack[-2] = s.stack[-2], s.stack[-1]
        
        



        visited.add(player.current_room.id)

    elif '?' in graph[player.current_room.id].values():
        for k, v in graph[player.current_room.id].items():
            if v == '?':
                s.push(k)

    # check if and '?' exist in the entire graph
    else:
        should_be_empty = []
        for k in graph.keys():
            if '?' in graph[k].values():
                should_be_empty.append(1)
        
        if len(should_be_empty) == 0:
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
