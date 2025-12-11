from modeling.domain import hop
#from state import refresh_people_count

state = hop.State('state0')

state.robots_pos = {'robot1': 'exit', 'robot2': 'exit'}

state.robot_has_person = {'robot1': False, 'robot2': False}

state.persons = {
    'p1': {'position': 'office-a', 'carried': False},
    'p2': {'position': 'office-a', 'carried': False},
    'p3': {'position': 'office-a', 'carried': False},
    'p4': {'position': 'office-c', 'carried': False},
    'p5': {'position': 'office-c', 'carried': False},
    'p6': {'position': 'room-1', 'carried': False},
    'p7': {'position': 'room-1', 'carried': False},
    'p8': {'position': 'room-3', 'carried': False},
    'p9': {'position': 'room-3', 'carried': False},
    'p10': {'position': 'hall', 'carried': False},
}

state.rooms = {
    'office-a': {'smokey': False, 'number_of_people': 0}, 
    'office-b': {'smokey': True, 'number_of_people': 0}, 
    'office-c': {'smokey': False, 'number_of_people': 0}, 
    'corridor-1': {'smokey': False, 'number_of_people': 0}, 
    'corridor-2': {'smokey': False, 'number_of_people': 0}, 
    'room-1': {'smokey': False, 'number_of_people': 0}, 
    'room-2': {'smokey': True, 'number_of_people': 0}, 
    'room-3': {'smokey': False, 'number_of_people': 0}, 
    'hall': {'smokey': False, 'number_of_people': 0}, 
    'reception': {'smokey': False, 'number_of_people': 0}, 
    'exit': {'smokey': False, 'number_of_people': 0}, 
    'stairs-left': {'smokey': False, 'number_of_people': 0},
    'stairs-right': {'smokey': False, 'number_of_people': 0}
}

state.connections = {
    'office-a': ['stairs-left', 'office-b'],
    'office-b': ['office-a', 'corridor-2'],
    'office-c': ['corridor-2'],
    'corridor-1': ['room-2', 'stairs-right', 'room-3'],
    'corridor-2': ['stairs-right', 'office-b', 'office-c'],
    'room-1': ['stairs-left', 'room-2'],
    'room-2': ['room-1', 'corridor-1'],
    'room-3': ['corridor-1'],
    'hall': ['stairs-left', 'reception'],
    'reception': ['hall', 'stairs-right', 'exit'],
    'exit': ['reception'],
    'stairs-left': ['hall', 'room-1', 'office-a'],
    'stairs-right': ['reception', 'corridor-1', 'corridor-2']
}

'''if __name__ == "__main__":
    #refresh_people_count(state) 
    print(f'state: {state}')'''

people_list = [
    'p1', 'p2', 'p3', 'p4', 'p5',
    'p6', 'p7', 'p8', 'p9', 'p10'
]

# split up the people into even and odd indexes
robot_list_1 = people_list[0::2]
robot_list_2 = people_list[1::2]

# robots can run one by ony
task_list = []
for i, person in enumerate(state.persons):
    robot = 'robot1' if i % 2 == 0 else 'robot2'
    task_list.append(('evacuate_person_with_robot', robot, person))

'''print("--- Starting Planning ---")

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
    print("Failure! Could not find a plan.")'''