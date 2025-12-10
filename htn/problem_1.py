from domain import hop
#from state import refresh_people_count

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

if __name__ == "__main__":
    #refresh_people_count(state) 
    print(f'state: {state}')

    people_list = [
        'person1', 'person2', 'person3', 'person4', 'person5',
        'person6', 'person7', 'person7', 'person9', 'person10'
    ]

    # split up the people into even and odd indexes
    robot_list_1 = people_list[0::2]
    robot_list_2 = people_list[1::2]

    # robots can run one by ony
    task_list = []
    for i, person in enumerate(state.persons):
        robot = 'robot1' if i % 2 == 0 else 'robot2'
        task_list.append(('evacuate_person_with_robot', robot, person))

    print("--- Starting Planning ---")
    
    print(hop.get_operators())
    print(hop.get_methods())
    
    plan = hop.plan(state, task_list, hop.get_operators(),hop.get_methods(),verbose=1)
    
    # 4. Display the results
    if plan:
        print("Success! Plan Found:")
        for step in plan:
            print(f"  {step}")
        print(f"Final State: Robot1 at {state.robots_pos['robot1']}")
        
    else:
        print("Failure! Could not find a plan.")