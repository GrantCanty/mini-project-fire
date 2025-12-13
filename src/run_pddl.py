import loader
from modeling.problem_1 import task_list, state
from visualizer import EvacuationSimulation


project_type = 'PDDL'
load = loader.EvacuationPlanner(domain_file='/Users/cheoso/ai_projects/mini_fire_lab/src/modeling/evacuation-domain.pddl', problem_file='/Users/cheoso/ai_projects/mini_fire_lab/src/modeling/emergency-problem.pddl', project_type=project_type)

plan = load.run_planner()
print(f'plan: {plan}')
sim = EvacuationSimulation(state, project_type)
sim.run(plan)