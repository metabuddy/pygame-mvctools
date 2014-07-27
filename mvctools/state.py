
import pygame
from mvctools.model import BaseModel
from mvctools.controller import BaseController
from mvctools.view import BaseView


class NextStateException(Exception):
    pass

class TickContext(object):
    def __init__(self, state):
        self.state = state

    def __enter__(self):
        self.state.ticking = True

    def __exit__(self, error, value, traceback):
        self.state.ticking = False
        if error is NextStateException:
            return True
            

class BaseState(object):
    model_class = BaseModel
    controller_class = BaseController
    view_class = BaseView
    clock_class = pygame.time.Clock
    
    def __init__(self, control):
        self.control = control
        self.model = self.model_class(self)
        self.controller = self.controller_class(self, self.model)
        self.view = self.view_class(self, self.model)
        self.ticking = False

    def tick(self):
        mvc = self.controller, self.model, self.view
        with TickContext(self):
            return any(entity._update() for entity in mvc)
        return True

    def reload(self):
        self.controller._reload()
        self.model._reload()
        self.view._reload()

    def run(self):
        # Display fps
        if self.control.display_fps:
            string = self.control.window_title + "   FPS = {:3}"
        else:
            string = None
        clock = self.clock_class()
        while not self.tick():
            clock.tick(self.control.settings.fps)
            rate = int(clock.get_fps())
            if string and rate:
                caption = string.format(rate)
                pygame.display.set_caption(caption)
            

        
