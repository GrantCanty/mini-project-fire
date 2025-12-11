# loader.py
import subprocess
import re
from modeling.domain import hop
from modeling.problem_1 import state
from pathlib import Path


class EvacuationPlanner:
    def __init__(self, project_type='HTN', domain_file=None, problem_file=None, task_list=None, state_obj=None):
        self.project_type = project_type
        self.domain_file = domain_file
        self.problem_file = problem_file
        self.task_list = task_list
        self.state = state_obj or state

    def run_planner(self):
        if self.project_type.upper() == 'PDDL':
            return self._run_pddl_planner()
        else:
            return self._run_htn_planner()

    def _run_htn_planner(self):
        print(f'operators: {hop.get_operators()}')
        print(f'methods: {hop.get_methods()}')
        print(f'task_list: {self.task_list}')
        
        plan = hop.plan(
            self.state,
            self.task_list,
            hop.get_operators(),
            hop.get_methods(),
            verbose=0
        )
        return plan

    def _run_pddl_planner(self):
        plan_path = Path('sas_plan')
        
        """Call Fast Downward and retrieve plan"""
        result = subprocess.run(
            ['./downward/fast-downward.py', "--plan-file", str(plan_path), self.domain_file, self.problem_file, '--search', 'lazy_greedy([ff()], preferred=[ff()])'],
            capture_output=True, text=True
        )
        success = result.returncode == 0 and plan_path.exists()

        plan_text = None
        if success is not None:
            try:
                plan_text = plan_path.read_text()
                print(f'plan_text plan:\n{plan_text}')
                actions = []

                for raw in plan_text.splitlines():
                    line = raw.strip()

                    if line.startswith("(") and line.endswith(")"):
                        inside = line[1:-1].strip()
                        parts = inside.split()

                        actions.append(tuple(parts))
            except Exception as e:
                print(e)
        
        return actions

    def parse_plan(self, plan_output):
        """Return a uniform plan list usable by visualizer"""
        if self.project_type.upper() == 'PDDL':
            # parse PDDL plan output into tuples
            actions = []
            for line in plan_output.splitlines():
                match = re.match(r'\(([\w\-]+)(.*?)\)', line.lower())
                if match:
                    action_name = match.group(1)
                    params = tuple(match.group(2).split())
                    actions.append((action_name,) + params)
            return actions
        else:
            return plan_output

    def execute_plan(self, plan):
        """Step through plan and update the state"""
        for action in plan:
            print(f"Executing: {action}")
            if self.project_type.upper() != 'PDDL':
                # Apply HTN actions to state
                if action[0] == 'move_robot':
                    robot, from_loc, to_loc = action[1], action[2], action[3]
                    self.state.robots_pos[robot] = to_loc
                elif action[0] == 'pick_up_person':
                    robot, person, loc = action[1], action[2], action[3]
                    self.state.robot_has_person[robot] = True
                    self.state.persons[person]['carried'] = True
                    self.state.persons[person]['position'] = self.state.robots_pos[robot]
                elif action[0] == 'drop_person':
                    robot, person, loc = action[1], action[2], action[3]
                    self.state.robot_has_person[robot] = False
                    self.state.persons[person]['carried'] = False
                    self.state.persons[person]['position'] = loc
            
            else:
                steps = []
                print(f'pddl plan:\n{plan}')
                for action in plan:  # action is ("move", "robot1", "office_a", "office_b")
                    name = action[0]
                    params = action[1:]

                    steps.append({
                        "action": name,
                        "params": params
                    })

                return steps