from pyhop import hop
# from . import problem_1

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
            #state.robots_pos[robot] = to_loc

            # Find the person whose position is the robot's name (i.e., the person being carried)
            if state.robot_has_person[robot]:
                carried_person_name = None
                
                # Iterate to find who is being carried by this specific robot
                for person_name, person_data in state.persons.items():
                    if person_data['position'] == state.robots_pos[robot] and person_data['carried'] == True:
                        carried_person_name = person_name
                        break
                
                # If found, update the person's 'position' to the robot's new location
                if carried_person_name:
                    state.persons[carried_person_name]['position'] = to_loc
            state.robots_pos[robot] = to_loc
            return state
    return False

def pick_up_person(state, robot, person, location):
    refresh_people_count(state)
    # check the person is not carried, if the position of the robot and person match, 
    # if the robot is not carrying anyone, and if the robot is in the given location
    if state.persons[person]['carried'] == False \
    and state.robots_pos[robot] == state.persons[person]['position'] \
    and state.robot_has_person[robot] == False \
    and state.robots_pos[robot] == location:
        state.persons[person]['carried'] = True
        state.robot_has_person[robot] = True
        return state
    return False

def drop_person(state, robot, person, location):
    refresh_people_count(state)
    # check if the person is carried, if the position of the robot and person match,
    # if the robot is carrying someone, and if the robot is in the given location
    if state.persons[person]['carried'] == True \
    and state.robots_pos[robot] == state.persons[person]['position'] \
    and state.robot_has_person[robot] == True \
    and state.robots_pos[robot] == location:
        state.persons[person]['carried'] = False
        state.robot_has_person[robot] = False
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

hop.declare_operators(move_robot, pick_up_person, drop_person)

def travel_at_destination(state, robot, remaining_path):
    """Method 1: Base Case - Stops the recursion when the path is empty."""
    if not remaining_path:
        return []
    return False

def travel_one_step(state, robot, remaining_path):
    """Method 2: Recursive Step - Executes one move and queues the rest of the path."""
    if remaining_path:

        current_loc = state.robots_pos[robot]
        next_loc = remaining_path[0]
        
        # The remaining path for the next recursive call
        new_remaining_path = remaining_path[1:]
        
        return [
            # 1. Execute the primitive move
            ('move_robot', robot, current_loc, next_loc),
            
            # 2. Recurse: Call the 'travel' task again with the remaining steps
            ('travel', robot, new_remaining_path)
        ]
    return False

hop.declare_methods('travel', travel_at_destination, travel_one_step)

def travel_wrapper(state, robot, start_loc, end_loc):
    """
    Wrapper method that calculates the full path once and kicks off the recursion.
    """
    # 1. Check if we're already there
    if start_loc == end_loc:
        return []
        
    # 2. Calculate the path steps
    # check if the robot is carrying someone or not
    if state.robot_has_person[robot] == False:
        path_steps = find_path(state.connections, start_loc, end_loc)
    else:
        # if the robot is carrying someone, filter rooms that are not smokey
        # then filter connections by available rooms
        avail_rooms = [room for room in state.rooms if state.rooms[room]['smokey'] == False]
        avail_conns = {conn: val for conn, val in state.connections.items() if conn in avail_rooms}
        path_steps = find_path(avail_conns, start_loc, end_loc)

    if path_steps is None:
        return False 
    if len(path_steps) < 1:
        return False
    
    # remove current location from path
    path_steps = path_steps[1:]

    # 3. Initialize recursion by calling the 'travel' task with the list of steps
    return [('travel', robot, path_steps)]

hop.declare_methods('travel_to', travel_wrapper)

def evacuate_person_with_robot(state, robot, person):
    print('entered evacuate with robot')
    # selected_robot = find_available_robot(state)
    person_loc = state.persons[person]['position']
    robot_loc = state.robots_pos[robot]
    exit_loc = 'exit'
        
    return [
        ('travel_to', robot, robot_loc, person_loc),
        ('pick_up_person', robot, person, person_loc),
        ('travel_to', robot, person_loc, exit_loc),
        ('drop_person', robot, person, exit_loc)
    ]

hop.declare_methods('evacuate_person_with_robot', evacuate_person_with_robot)

def robot_mission_method(state, robot, persons):
    print('entered robot mission')
    if not persons:
        return []

    person = persons[0]
    rest = persons[1:]

    return [
        ('evacuate_person_with_robot', robot, person),
        ('robot_mission', robot, rest)
    ]

hop.declare_methods('robot_mission', robot_mission_method)