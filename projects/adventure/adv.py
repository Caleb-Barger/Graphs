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
map_file = "maps/test_cross.txt"
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
r = player.current_room.id

# populate the stack and graph with starting room info
graph[r] = {k:'?' for k in player.current_room.get_exits()}

for k in graph[r].keys():
    s.push(k)

def add_way_back(d):
    if d == 'n':
        s.push('s')
    if d == 's':
        s.push('n')
    if d == 'e':
        s.push('w')
    if d == 'w':
        s.push('e')

# while the stack is not empty keep exploring
while s.size() > 0:
    direction = s.pop()
    # add this movement to the path
    traversal_path.append(direction)
    prev_room = player.current_room.id

    player.travel(direction) # move the player

    # ok now I need the new rooms id
    r = player.current_room.id

    # if the entry does not exist populate the graph
    if r not in graph:
        graph[r] = {k:'?' for k in player.current_room.get_exits()}

    # update the graph for both rooms
    graph[prev_room][direction] = r
   
    if direction == 'n':
        graph[r]['s'] = prev_room
    elif direction == 's':
        graph[r]['n'] = prev_room
    elif direction == 'e':
        graph[r]['w'] = prev_room
    else:
        graph[r]['e'] = prev_room

    # only push new direction onto the stack
    push_count = 0
    for d in player.current_room.get_exits():
        if graph[r][d] == '?':
            s.push(d)
            push_count += 1
            backtracking = False

    if push_count == 0 and not backtracking:
        backtracking = True
    
    if '?' not in graph[r].values() and not backtracking:
        s.pop()
        add_way_back(direction)
        add_way_back(direction)

    
    time.sleep(3)
    print(f"STACK - {s.stack}")
    print(f"graph - {graph}")
    print(f"ROOM - {player.current_room.id}")
    
    print("\n")

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
