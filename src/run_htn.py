import loader
from modeling.problem_1 import task_list, state
from visualizer import EvacuationSimulation


project_type = 'HTN'
load = loader.EvacuationPlanner(task_list=task_list, state_obj=state, project_type= project_type)

plan = load.run_planner()

sim = EvacuationSimulation(state, project_type)
sim.run(plan)