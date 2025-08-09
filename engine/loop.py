import time


class Scene:
    """Base class for game scenes."""

    def __init__(self, game=None):
        self.game = game

    def handle_input(self, events):
        """Process input events."""
        return None

    def update(self, dt):
        """Update scene state."""
        return None

    def render(self, renderer):
        """Render scene using the provided renderer."""
        return None


class Game:
    """Core game application managing the main loop and scenes."""

    def __init__(self, renderer, input_handler, start_scene, fps=60):
        self.renderer = renderer
        self.input = input_handler
        self.scene = start_scene
        self.scene.game = self
        self.fps = fps
        self.running = False

    def change_scene(self, scene):
        self.scene = scene
        self.scene.game = self

    def stop(self):
        self.running = False

    def run(self):
        self.running = True
        dt = 0.0
        while self.running:
            start = time.time()
            events = self.input.get_events()
            self.scene.handle_input(events)
            self.scene.update(dt)
            self.renderer.begin()
            self.scene.render(self.renderer)
            self.renderer.end()
            dt = time.time() - start
            delay = max(1.0 / self.fps - dt, 0)
            if delay:
                time.sleep(delay)
                dt += delay
