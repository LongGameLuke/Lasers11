# Base scene class and scene manager for the UI state machine


class Scene:
    """Base class for all UI scenes. Subclasses override lifecycle methods."""

    def __init__(self, manager):
        self.manager = manager
        self.game = manager.game
        self.screen = manager.screen

    def enter(self):
        """Called when the scene becomes active."""
        pass

    def exit(self):
        """Called when the scene is switched away from."""
        pass

    def handle_events(self, events):
        """Process pygame events for this scene."""
        pass

    def update(self):
        """Update scene logic each frame."""
        pass

    def render(self):
        """Draw the scene to the screen."""
        pass


class SceneManager:
    """Manages scene registration and transitions between scenes."""

    def __init__(self, game, screen):
        self.game = game
        self.screen = screen
        self.scenes = {}
        self.current_scene = None

    def add(self, name, scene_cls):
        """Register a scene class under a name, instantiating it immediately."""
        self.scenes[name] = scene_cls(self)

    def switch(self, name):
        if self.current_scene:
            self.current_scene.exit()
        self.current_scene = self.scenes.get(name)
        if self.current_scene:
            self.current_scene.enter()
