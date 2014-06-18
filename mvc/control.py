import pygame, sys
from mvc.gamedata import BaseGamedata
from mvc.state import BaseState
from mvc.settings import BaseSettings

class BaseControl:

    settings_class = BaseSettings
    game_data_class = BaseGamedata
    first_state_type = None
    
    def __init__(self):
        self.next_state_type = self.first_state_type
        self.settings = BaseSettings()
        self.current_state = None
        self.state_stack = []

    def load_next_state(self):
        if self.next_state_type:
            self.current_state = self.next_state_type(self)
            self.next_state_type = None
        elif self.state_stack:
            self.current_state = self.pop_state()
        else:
            self.current_state = None
        return self.current_state
        
    def run(self):
        while self.load_next_state():
            try:
                self.current_state.run()
            except SystemExit:
                break
        self.safe_exit()     

    def register_next_state_type(self, state_type):
        self.next_state_type = state_type

    def push_current_state(self):
        self.state_stack.append(self.current_state)

    def pop_state(self):
        try:
            return self.state_stack.pop()
        except IndexError:
            return None

    def get_fps(self):
        return self.settings.get_fps()

    @staticmethod
    def safe_exit():
        pygame.quit()
        

