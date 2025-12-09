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
    'stairs_1': {'smokey': False, 'number_of_people': 0},
    'stairs_2': {'smokey': False, 'number_of_people': 0}
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
    'reception': ['hall', 'stairs_2', 'exit'],
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
    print('in move_robot')

    # check if there is a connection between the locations and if the robot is in the from location
    if to_loc in state.connections[from_loc] and state.robots_pos[robot] == from_loc:
        # check if room is not smokey or if robot is not carrying and the room is smokey
        if state.rooms[to_loc]['smokey'] == False or (state.robot_has_person[robot] == False and state.rooms[to_loc]['smokey'] == True ):
            #state.robots_pos[robot] = to_loc

            # Find the person whose position is the robot's name (i.e., the person being carried)
            if state.robot_has_person[robot]:
                carried_person_name = None
                
                # Iterate to find who is being carried by this specific robot
                print(f'robot position: {state.robots_pos[robot]}')
                for person_name, person_data in state.persons.items():
                    print(person_name, person_data)
                    if person_data['position'] == state.robots_pos[robot] and person_data['carried'] == True:
                        carried_person_name = person_name
                        print(f'setting carried person name: {carried_person_name}')
                        break
                
                # If found, update the person's 'position' to the robot's new location
                if carried_person_name:
                    print(f'carried_person_name: {carried_person_name}')
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

    print('in drop person function')
    print(f'is person carried: {state.persons[person]["carried"] == True}')
    print(f'does robot_position == person_position: {state.robots_pos[robot] == state.persons[person]["position"]}')
    print(f'robot position {state.robots_pos[robot]} person position: {state.persons[person]["position"]}')
    print(f'does robot have person: {state.robot_has_person[robot] == True}')
    print(f'does robot_position == location: {state.robots_pos[robot] == location}')
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
    print(f'conns: {connections}')
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
        print(f'returning remaining path: {remaining_path}')
        return []
    print(f'returning false')
    return False

def travel_one_step(state, robot, remaining_path):
    """Method 2: Recursive Step - Executes one move and queues the rest of the path."""
    print('entered travel_one_step')
    if remaining_path:

        print(f'len of remaining path: {len(remaining_path)}')
        current_loc = state.robots_pos[robot]
        next_loc = remaining_path[0]
        
        print(f'current location: {current_loc}\nnext location: {next_loc}\n')
        
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
    print(f'travel_wrapper: {start_loc} -> {end_loc}')
    """
    Wrapper method that calculates the full path once and kicks off the recursion.
    """
    # 1. Check if we're already there
    if start_loc == end_loc:
        return []
        
    # 2. Calculate the path steps
    path_steps = find_path(state.connections, start_loc, end_loc)
    print(f'path_steps: {path_steps}')

    if path_steps is None:
        print(f"Error: No path found from {start_loc} to {end_loc}.")
        return False 
    if len(path_steps) < 1:
        print('Error: Path length empty')
        return False
    
    path_steps = path_steps[1:]

    # 3. Initialize recursion by calling the 'travel' task with the list of steps
    return [('travel', robot, path_steps)]

hop.declare_methods('travel_to', travel_wrapper)




def evacuate_person(state, person):
    selected_robot = find_available_robot(state)

    if selected_robot is not None:
        person_loc = state.persons[person]['position']
        robot_loc = state.robots_pos[selected_robot]
        exit_loc = 'exit'

        print(f'after robot: {person_loc, robot_loc, exit_loc}')
        
        return [
            ('travel_to', selected_robot, robot_loc, person_loc),
            ('pick_up_person', selected_robot, person, person_loc),
            ('travel_to', selected_robot, person_loc, exit_loc),
            ('drop_person', selected_robot, person, exit_loc)
        ]
    return False

hop.declare_methods('evacuate_person', evacuate_person)


if __name__ == "__main__":
    refresh_people_count(state) 
    
    # 2. Define the main goal task
    # Example: Rescue person1.
    task_list = [
        ('evacuate_person', 'person1'),
        ('evacuate_person', 'person2'),
        ('evacuate_person', 'person3'),
        ('evacuate_person', 'person4'),
        ('evacuate_person', 'person5'),
        ('evacuate_person', 'person6'),
        ('evacuate_person', 'person7'),
        ('evacuate_person', 'person8'),
        ('evacuate_person', 'person9'),
        ('evacuate_person', 'person10')
        ]

    print("--- Starting Planning ---")
    plan = hop.plan(state, task_list, hop.get_operators(),hop.get_methods(),verbose=1)
    
    # 4. Display the results
    if plan:
        print("Success! Plan Found:")
        for step in plan:
            print(f"  {step}")
        print(f"Final State: Robot1 at {state.robots_pos['robot1']}")
        
    else:
        print("Failure! Could not find a plan.")