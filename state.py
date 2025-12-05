from pyhop import hop


# define initial state
state = hop.State('state0')

state.robots_pos = {'robot1': 'exit', 'robot2': 'exit'}

state.robot_has_person = {'robot1': False, 'robot2': False}

state.persons = {
    'person1': {'position': 'office_a', 'carried': False},
    'person2': {'position': 'office_a', 'carried': False},
    'person3': {'position': 'office_a', 'carried': False},
    'person4': {'position': 'office_c', 'carried': False},
    'person5': {'position': 'office_c', 'carried': False},
    'person6': {'position': 'room_1', 'carried': False},
    'person7': {'position': 'room_1', 'carried': False},
    'person8': {'position': 'room_3', 'carried': False},
    'person9': {'position': 'room_3', 'carried': False},
    'person10': {'position': 'hall', 'carried': False},
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
    for people in state.persons:
        for room in state.rooms:
            if state.persons[people]['position'] == room:
                state.rooms[room]['number_of_people'] += 1
                # print(state.rooms[room]['number_of_people'])

def move_robot(state, robot, from_loc, to_loc):
    # check if there is a connection between the locations and if the robot is in the from location
    if to_loc in state.connections[from_loc] and state.robots_pos[robot] == from_loc:
        # check if robot has person and if room is smokey
        if (state.robot_has_person[robot] == False and state.rooms[to_loc] )
        state.robots_pos[robot] = to_loc
        return True
    return False

def pick_up_person(state, robot, location):


def evacuate_person(state, person):
    # TODO: Decompose into subtasks
    # Example: find_robot -> go_to_person -> pick_up ->
    # go_to_exit -> drop_off
    pass