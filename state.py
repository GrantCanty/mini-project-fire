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
    'room_2': ['room_1', 'corridor_1'],
    'room_3': ['corridor_1'],
    'hall': ['stairs_1', 'reception'],
    'reception': ['hall', 'stairs_2'],
    'exit': ['reception'],
    'stairs_1': ['hall', 'room_1', 'office_a'],
    'stairs_2': ['reception', 'corridor_1', 'corridor_2']
}

def refresh_people_count(state):
    for room in state.rooms:
        state.rooms[room]['number_of_people'] = 0
    
    for people in state.persons:
        person_data = state.persons[people]
        if not person_data['carried']:
            room = person_data['position']
            state.rooms[room]['number_of_people'] += 1

def move_robot(state, robot, from_loc, to_loc):
    refresh_people_count(state)

    # check if there is a connection between the locations and if the robot is in the from location
    if to_loc in state.connections[from_loc] and state.robots_pos[robot] == from_loc:
        # check if room is not smokey or if robot is not carrying and the room is smokey
        if state.rooms[to_loc]['smokey'] == False or (state.robot_has_person[robot] == False and state.rooms[to_loc]['smokey'] == True ):
            state.robots_pos[robot] = to_loc

            # Find the person whose position is the robot's name (i.e., the person being carried)
            if state.robot_has_person[robot]:
                carried_person_name = None
                
                # Iterate to find who is being carried by this specific robot
                for person_name, person_data in state.persons.items():
                    if person_data['position'] == robot and person_data['carried'] == True:
                        carried_person_name = person_name
                        break
                
                # If found, update the person's 'position' to the robot's new location
                if carried_person_name:
                    state.persons[carried_person_name]['position'] = to_loc
        return state
    return False

def pick_up_person(state, robot, person, location):
    refresh_people_count(state)
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
        return state
    return False

def drop_person(state, robot, person, location):
    refresh_people_count(state)
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
        return state
    return False

def find_available_robot(state):
    avails = [robot for robot, is_carrying in state.robot_has_person.items() if is_carrying == False]
    if len(avails) > 0:
        return avails[0]
    return None

import collections

def find_path(connections, start_loc, goal_loc):
    if start_loc == goal_loc:
        return [start_loc]
    
    # pop from deque
    queue = collections.deque([start_loc])
    
    # shortest path history
    predecessors = {start_loc: None} 
    
    # track visited rooms
    visited = {start_loc}
    path_found = False

    while queue:
        current_loc = queue.popleft()

        # all neighbors of the current location
        for neighbor in connections.get(current_loc, []):
            if neighbor not in visited:
                # path history
                predecessors[neighbor] = current_loc
                visited.add(neighbor)
                queue.append(neighbor)

                # goal state
                if neighbor == goal_loc:
                    path_found = True
                    break
        
        if path_found:
            break

    if not path_found:
        return None

    path = []
    step = goal_loc
    
    # get path
    while step is not None:
        path.append(step)
        step = predecessors.get(step)
        
    # path is constructed backwards. needs to be reversed
    path.reverse()
    
    return path

def travel(state, start, end, robot):
    path = find_path(state.connections, start, end)
    for i in range(len(path) -1):
        move_robot(state, robot, path[i], path[i+1])


hop.declare_operators(travel, pick_up_person, drop_person)


def evacuate_person(state, person):
    selected_robot = find_available_robot(state)

