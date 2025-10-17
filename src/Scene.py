"""Scene.py

Created on 2025-10-16



"""
__author__ = "carras_a"
__version__ = "1.0"


from .GameObject import GameObject


class Scene:
    def __init__(self):
        self.renderable_objects = []
        pass

    def render(self, screen):
        for object in self.renderable_objects:
            object.render(screen)
        pass

    def update(self):
        # Uninstance all objects that get killed and collect return states
        for object in self.renderable_objects:
            if object.is_dead:
                self.remove_object(object)
            else:
                return_state = object.update()
                if return_state is not None and return_state in ["EXIT", "SETTINGS", "MAIN_MENU", "PLAY_PONG", "PLAY_BRICK", "PLAY_BRICK_GAME"]:
                    return return_state
        return None

    def add_object(self, object):
        # Accept any object that implements a render(screen) method (duck typing),
        # avoiding the need to import GameObject which caused errors.
        if hasattr(object, "render") and callable(getattr(object, "render")):
            self.renderable_objects.append(object)
        return

    def remove_object(self, object):
        if object in self.renderable_objects:
            self.renderable_objects.remove(object)
        pass
