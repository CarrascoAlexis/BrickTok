"""Scene.py

Created on 2025-10-16

Scene base class.
Contains renderable objects and handles their rendering and updating.

"""
__author__ = "carras_a"
__version__ = "1.0"


from .GameObject import GameObject


class Scene:
    def __init__(self):
        """Initialize the scene with an empty list of renderable objects."""
        self.renderable_objects = []
        self.returnable_states = ["EXIT",
                                  "SETTINGS",
                                  "MAIN_MENU",
                                  "PLAY_PONG",
                                  "PLAY_BRICK",
                                  "PLAY_BRICK_GAME",
                                  "START_PONG"]
        pass

    def render(self, screen):
        """Render all objects in the scene."""
        for object in self.renderable_objects:
            # Check if object is a GameObject
            if isinstance(object, GameObject):
                object.render(screen)
        pass

    def update(self):
        """Update all objects in the scene.
        If any object returns a state change, propagate it up.
        """
        for object in self.renderable_objects:
            if object.is_dead:
                # Remove dead objects (Usefull for bricks that are destroyed)
                self.remove_object(object)
            else:
                return_state = object.update()
                if return_state in self.returnable_states:
                    return return_state
        return None

    def add_object(self, object):
        """Add object to scene if it is a GameObject."""
        if isinstance(object, GameObject):
            self.renderable_objects.append(object)
        return

    def remove_object(self, object):
        """Remove object from scene and delete it to free memory."""
        if object in self.renderable_objects:
            self.renderable_objects.remove(object)
            del object
        pass

    def handle_event(self, event):
        """Handle incoming events by forwarding them to child objects."""
        for object in self.renderable_objects:
            # Check if object is a GameObject
            if isinstance(object, GameObject):
                object.handle_event(event)
