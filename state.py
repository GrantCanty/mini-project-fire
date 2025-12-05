from pyhop import hop


# define initial state
state = hop.State('state0')

state.robots_pos = {'robot1': 'exit', 'robot2': 'exit'}
state.people_pos = {
    'person1': 'office_a', 
    'person2': 'office_a', 
    'person3': 'office_a', 
    'person4': 'office_c', 
    'person5': 'office_c', 
    'person6': 'room_1', 
    'person7': 'room_1',
    'person8': 'room_3',
    'person9': 'room_3',
    'person10': 'hall'
}

state.rooms = {
    'office_a': {'smokey': False, 'number_of_people': 0}, 
    'office_b': {'smokey': True, 'number_of_people': 0}, 
    'office_c': {'smokey': False, 'number_of_people': 0}, 
    'corridor_1': {'smokey': False, 'number_of_people': 0}, 
    'corridor_2': {'smokey': False, 'number_of_people': 0}, 
    'room_1': {'smokey': False, 'number_of_people': 0}, 
    'room_2': {'smokey': True, 'number_of_people': 0}, 
    'room_3': {'smokey': False, 'number_of_people': 0}, 
    'hall': {'smokey': False, 'number_of_people': 0}, 
    'reception': {'smokey': False, 'number_of_people': 0}, 
    'exit': {'smokey': False, 'number_of_people': 0}, 
    'stairs1': {'smokey': False, 'number_of_people': 0},
    'stairs2': {'smokey': False, 'number_of_people': 0}
}

state.connections = {
    'office_a': ['stairs_1', 'office_b'],
    'office_b': ['office_a', 'corridor_2'],
    'office_c': ['corridor_2'],
    'corridor_1': ['room_2', 'stairs_2', 'room_3'],
    'corridor_2': ['stairs_2', 'office_b', 'office_c'],
    'room_1': ['stairs_1', 'room_2'],
    'room_2': ['room1', 'corridor_1'],
    'room_3': ['corridor_1'],
    'hall': ['stairs_1', 'reception'],
    'reception': ['hall', 'stairs_2'],
    'exit': ['reception'],
    'stairs_1': ['hall', 'room_1', 'office_a'],
    'stairs_2': ['reception', 'corridor_1', 'corridor_2']
}

def refresh_people_count(state):
    for people in state.people_pos:
        for room in state.rooms:
            if state.people_pos[people] == room:
                state.rooms[room]['number_of_people'] += 1
                # print(state.rooms[room]['number_of_people'])

def move_robot(state, robot, from_loc, to_loc):
    if to_loc in state.connections[from_loc] and state.robots_pos[robot] == from_loc:
        state.robots_pos[robot] = to_loc
        return True
    return False

def evacuate_person(state, person):
    # TODO: Decompose into subtasks
    # Example: find_robot -> go_to_person -> pick_up ->
    # go_to_exit -> drop_off
    pass