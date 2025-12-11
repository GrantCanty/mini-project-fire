# visualizer.py
import pygame
import time
#from modeling.domain import refresh_people_count

class EvacuationSimulation:
    def __init__(self, state, project_type, width=1200, height=800):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.state = state
        self.project_type = project_type

        # Room positions (x, y, width, height) example
        self.room_positions = {
            'office-a':     (100, 100, 100, 100),
            'office-b':     (250, 100, 100, 100),
            'corridor-2':   (500, 100, 100, 100),
            'office-c':     (650, 100, 100, 100),
            'room-1':       (100, 250, 100, 100),
            'room-2':       (250, 250, 100, 100),
            'corridor-1':   (500, 250, 100, 100),
            'room-3':       (650, 250, 100, 100),
            'hall':         (100, 400, 250, 100),
            'reception':    (500, 400, 100, 100),
            'exit':         (650, 400, 100, 100),
            'stairs-left':     (25, 100, 50, 400),
            'stairs-right':     (400, 100, 50, 400),
        }

    def draw_building(self):
        for room, rect in self.room_positions.items():
            color = (0, 255, 0) if not self.state.rooms.get(room, {}).get('smokey', False) else (255, 0, 0)
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, (0,0,0), rect, 2)  # room border
            # Room name
            font = pygame.font.Font(None, 24)
            text = font.render(room, True, (0,0,0))
            self.screen.blit(text, (rect[0]+5, rect[1]+5))

    def draw_entities(self):
        # Robots
        for robot, loc in self.state.robots_pos.items():
            rect = self.room_positions.get(loc)
            if rect:
                pygame.draw.circle(self.screen, (0,0,255), (rect[0]+rect[2]//2, rect[1]+rect[3]//2), 15)
        # People
        for person, pdata in self.state.persons.items():
            loc = pdata['position']
            rect = self.room_positions.get(loc)
            if rect:
                pygame.draw.circle(self.screen, (255,255,0), (rect[0]+rect[2]//2 + 10, rect[1]+rect[3]//2 + 10), 10)

    def animate_actionHTN(self, action):
        # Only handle move_robot for now
        if action[0] == 'move_robot':
            robot, from_loc, to_loc = action[1], action[2], action[3]
            print(f"{robot} moves from {from_loc} to {to_loc}")
            self.state.robots_pos[robot] = to_loc
            if self.state.robot_has_person:
                for person in self.state.persons:
                    if self.state.persons[person]['carried'] and self.state.persons[person]['position'] == from_loc:
                        self.state.persons[person]['position'] = self.state.robots_pos[robot]
            #refresh_people_count(self.state)
            print(f"{robot} moves from {from_loc} to {to_loc}")
        elif action[0] == 'pick_up_person':
            robot, person, loc = action[1], action[2], action[3]
            self.state.robot_has_person[robot] = True
            self.state.persons[person]['carried'] = True
            self.state.persons[person]['position'] = self.state.robots_pos[robot]
            #refresh_people_count(self.state)
            print(f"{robot} picks up {person}")
        elif action[0] == 'drop_person':
            robot, person, loc = action[1], action[2], action[3]
            self.state.robot_has_person[robot] = False
            self.state.persons[person]['carried'] = False
            self.state.persons[person]['position'] = loc
            #refresh_people_count(self.state)
            print(f"{robot} drops {person}")


    def animate_actionPDDL(self, action):
        if action[0] == 'move-robot-loaded':
            robot, person, from_loc, to_loc = action[1], action[2], action[3], action[4]
            self.state.robots_pos[robot] = to_loc
            self.state.persons[person]['position'] = to_loc
            #self.state.cal
            print(f"{robot} moves from {from_loc} to {to_loc}")
        elif action[0] == 'move-robot-empty':
            robot, from_loc, to_loc = action[1], action[2], action[3]
            self.state.robots_pos[robot] = to_loc
            print(f"{robot} moves from {from_loc} to {to_loc}")
        elif action[0] == 'pick-up':
            robot, person, loc = action[1], action[2], action[3]
            self.state.robot_has_person[robot] = True
            self.state.persons[person]['carried'] = True
            self.state.persons[person]['position'] = self.state.robots_pos[robot]
            print(f"{robot} picks up {person}")
        elif action[0] == 'drop-at-exit':
            robot, person, loc = action[1], action[2], action[3]
            self.state.robot_has_person[robot] = False
            self.state.persons[person]['carried'] = False
            self.state.persons[person]['position'] = loc
            print(f"{robot} drops {person}")
        

    def run(self, plan):
        running = True
        action_index = 0
        while running and action_index < len(plan):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            self.screen.fill((255, 255, 255))
            self.draw_building()
            self.draw_entities()
            if self.project_type.upper() == 'HTN':
                self.animate_actionHTN(plan[action_index])
            else:
                self.animate_actionPDDL(plan[action_index])
            action_index += 1
            pygame.display.flip()
            self.clock.tick(2)  # 2 actions/sec
            time.sleep(0.5)

        pygame.quit()
