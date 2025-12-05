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
        state.persons[people]['number_of_people'] = 0
    
    for people in state.persons:
        for room in state.rooms:
            if state.persons[people]['position'] == room and state.persons[people]['carried'] == False:
                state.rooms[room]['number_of_people'] += 1
                # print(state.rooms[room]['number_of_people'])

def move_robot(state, robot, person, from_loc, to_loc):
    # check if there is a connection between the locations and if the robot is in the from location
    if to_loc in state.connections[from_loc] and state.robots_pos[robot] == from_loc:
        # check if room is not smokey or if robot is not carrying and the room is smokey
        if state.rooms[to_loc]['smokey'] == False or (state.robot_has_person[robot] == False and state.rooms[to_loc]['smokey'] == True ):
            state.robots_pos[robot] = to_loc
            #if state.robot_has_person[robot] == True:
            #    state.persons[person]['position'] = to_loc
        return True
    return False

def pick_up_person(state, robot, person, location):
    # check the person is not carried, if the position of the robot and person match, 
    # if the robot is not carrying anyone, and if the robot is in the given location
    if state.persons[person]['carried'] == False \
    and state.robots_pos[robot] == state.persons[person]['position'] \
    and state.robot_has_person[robot] == False \
    and state.robot_pos[robot] == location:
        state.persons[person]['carried'] = True
        state.robot_has_person[robot] = True
        state.robot_pos[robot] = location
        state.persons[person]['position'] = location
        return True
    return False
    pass

def drop_person(state, robot, person, location):
    # check if the person is carried, if the position of the robot and person match,
    # if the robot is carrying someone, and if the robot is in the given location
    if state.persons[person]['carried'] == True \
    and state.robots_pos[robot] == state.persons[person]['position'] \
    and state.robot_has_person[robot] == True \
    and state.robot_pos[robot] == location:
        state.persons[person]['carried'] = False
        state.robot_has_person[robot] = False
        state.robot_pos[robot] = location
        state.persons[person]['position'] = location
        return True
    return False

def evacuate_person(state, person):
    # TODO: Decompose into subtasks
    # Example: find_robot -> go_to_person -> pick_up ->
    # go_to_exit -> drop_off
    pass