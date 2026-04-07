class Scene:
   
    def __init__(self, manager):
        self.manager = manager
        self.game = manager.game
        self.screen = manager.screen

    def enter(self):
        pass

    def exit(self):
        pass

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def render(self):
        pass


class SceneManager:

    def __init__(self, game, screen):
        self.game = game
        self.screen = screen
        self.scenes = {}
        self.current_scene = None

    def add(self, name, scene_cls):
        self.scenes[name] = scene_cls(self)

    def switch(self, name):
        if self.current_scene:
            self.current_scene.exit()
        self.current_scene = self.scenes.get(name)
        if self.current_scene:
            self.current_scene.enter()
